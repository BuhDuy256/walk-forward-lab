#!/usr/bin/env python3
"""
reqcheck.py - checks docs/02-requirements against its writing rules.

Usage:
    python3 tools/reqcheck.py              # same as: check
    python3 tools/reqcheck.py check        # full check, exit code 1 if any ERROR
    python3 tools/reqcheck.py impact <ID>  # show everything above and below <ID>

What it checks (mechanical rules only; meaning is checked by a human or an AI):
    - every ID is unique, and no ID number was skipped (deleted instead of withdrawn)
    - every item has its required fields
    - every link points to a file and heading that exist
    - no active item points to a withdrawn item
    - index tables match the items in the file
    - coverage: actor -> problem -> use case -> requirement, no gaps
    - warnings: vague words, EARS shape, more than one "shall", product/tech names

No third-party packages. Python 3.8+.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_DIR = ROOT / "docs" / "02-requirements"
FILES = ["01-actors.md", "02-problems.md", "03-use-cases.md", "04-spec.md"]

ID_RE = r"(?:FR-[A-Z]{2}|NFR|CON|DR|UC|A|P)-\d{2}"
HEADING_RE = re.compile(rf"^(#{{3,4}}) ({ID_RE})\s*$")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
ID_LINK_RE = re.compile(rf"\[({ID_RE})\]\(")
FIELD_RE = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$")

REQUIRED = {
    "A": ["Type"],
    "P": ["Problem", "Affects", "Impact", "A good solution would"],
    "UC": ["Level", "Primary actor", "Supporting actors", "Solves", "Trigger",
           "Preconditions", "Success guarantee", "Minimal guarantee", "Main success scenario"],
    "FR": ["Statement", "Why", "Traces to", "Verified by"],
    "DR": ["Statement", "Why", "Traces to", "Verified by"],
    "CON": ["Statement", "Why", "Traces to", "Verified by"],
    "NFR": ["Source", "Stimulus", "Environment", "Artifact", "Response",
            "Response measure", "Traces to", "Verified by"],
}
# Fields that hold the "points up" links of each type.
UP_FIELDS = {
    "A": [],
    "P": ["Affects"],
    "UC": ["Primary actor", "Supporting actors", "Solves"],
    "FR": ["Traces to"], "DR": ["Traces to"], "NFR": ["Traces to"], "CON": ["Traces to"],
}
VAGUE = ["fast", "quickly", "easy", "easily", "flexible", "user-friendly", "etc",
         "and/or", "simple", "efficient", "robust", "as soon as possible", "appropriate",
         "some", "several", "many"]
# Product / technology names that must only appear as examples ("e.g.", "such as").
HARD_NAMES = ["Binance", "OKX", "Bybit", "Coinbase", "Bitcoin", "BTC", "Ethereum",
              "Spring", "PostgreSQL", "Postgres", "MySQL", "Kafka", "RabbitMQ", "Redis",
              "WebSocket", "React", "Vue", "BERT"]
EARS_STARTS = ("The ", "When ", "While ", "If ", "Where ")


def id_type(item_id):
    return item_id.split("-")[0] if not item_id.startswith("FR-") else "FR"


def id_prefix(item_id):
    return item_id.rsplit("-", 1)[0]


def id_num(item_id):
    return int(item_id.rsplit("-", 1)[1])


def slug(text):
    """GitHub-style heading anchor."""
    s = text.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


class Item:
    def __init__(self, item_id, file, line):
        self.id = item_id
        self.file = file
        self.line = line
        self.body = []
        self.name = None
        self.fields = {}

    @property
    def type(self):
        return id_type(self.id)

    @property
    def withdrawn(self):
        return self.fields.get("Status", "").lower().startswith("withdrawn")

    def text(self):
        return "\n".join(self.body)

    def links(self):
        return ID_LINK_RE.findall(self.text())

    def up_links(self):
        out = []
        for f in UP_FIELDS[self.type]:
            out += ID_LINK_RE.findall(self.fields.get(f, ""))
        return out


def parse_fields(lines):
    fields, cur = {}, None
    for ln in lines:
        m = FIELD_RE.match(ln)
        if m:
            cur = m.group(1)
            fields[cur] = m.group(2)
        elif cur and (ln.startswith(" ") or ln.startswith("\t")):
            fields[cur] += "\n" + ln
        elif ln.strip() and not ln.startswith(" "):
            cur = None
    return fields


def load():
    items, docs = {}, {}
    dupes = []
    for fname in FILES:
        path = REQ_DIR / fname
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        docs[fname] = lines
        cur = None
        for i, ln in enumerate(lines, 1):
            m = HEADING_RE.match(ln)
            if m:
                cur = Item(m.group(2), fname, i)
                if cur.id in items:
                    dupes.append((cur.id, items[cur.id], cur))
                items[cur.id] = cur
                continue
            if ln.startswith("#") or ln.strip() == "---":
                cur = None
                continue
            if cur is not None:
                cur.body.append(ln)
        for it in items.values():
            if it.file == fname and not it.fields:
                it.fields = parse_fields(it.body)
                for b in it.body:
                    mb = re.match(r"^\*\*(.+)\*\*\s*$", b.strip())
                    if mb:
                        it.name = mb.group(1)
                        break
    return items, docs, dupes


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"ERROR   {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"WARN    {where}: {msg}")


def loc(it):
    return f"{it.file}:{it.line} {it.id}"


def check_ids(items, dupes, r):
    for d, a, b in dupes:
        r.err(f"{b.file}:{b.line} {d}", f"duplicate ID (first at {a.file}:{a.line})")
    by_prefix = defaultdict(list)
    for it in items.values():
        by_prefix[id_prefix(it.id)].append(id_num(it.id))
    for p, nums in by_prefix.items():
        missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
        for n in missing:
            r.warn(f"{p}-{n:02d}", "ID number is missing. Was an item deleted instead of withdrawn?")


def check_fields(items, r):
    for it in items.values():
        if it.withdrawn:
            if "Replaced by" not in it.fields.get("Status", "") and "Reason" not in it.fields.get("Status", ""):
                r.warn(loc(it), "withdrawn item should give a reason or 'Replaced by'")
            continue
        for f in REQUIRED[it.type]:
            if f not in it.fields or not it.fields[f].strip():
                r.err(loc(it), f"missing field '{f}'")
        if it.type in ("A", "P", "UC", "NFR") and not it.name:
            r.err(loc(it), "missing bold name line")


def check_links(items, docs, r):
    anchors = {}
    for fname in list(docs.keys()):
        anchors[fname] = {slug(m.group(1)) for ln in docs[fname]
                          for m in [re.match(r"^#+ (.+)$", ln)] if m}
    for fname, lines in docs.items():
        for i, ln in enumerate(lines, 1):
            for _, target in LINK_RE.findall(ln):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                path_part, _, anchor = target.partition("#")
                tpath = (REQ_DIR / path_part).resolve() if path_part else (REQ_DIR / fname)
                if not tpath.exists():
                    r.err(f"{fname}:{i}", f"link to missing file '{target}'")
                    continue
                if anchor and tpath.suffix == ".md":
                    rel = tpath.name if tpath.parent == REQ_DIR else None
                    known = anchors.get(rel) if rel else {
                        slug(m.group(1)) for l2 in tpath.read_text(encoding="utf-8").splitlines()
                        for m in [re.match(r"^#+ (.+)$", l2)] if m}
                    if anchor not in known:
                        r.err(f"{fname}:{i}", f"link to missing heading '{target}'")


def check_refs(items, r):
    for it in items.values():
        if it.withdrawn:
            continue
        for ref in set(it.links()):
            if ref not in items:
                r.err(loc(it), f"points to unknown ID {ref}")
            elif items[ref].withdrawn:
                r.err(loc(it), f"points to withdrawn item {ref}")


def check_index(items, docs, r):
    for fname in ("01-actors.md", "02-problems.md", "03-use-cases.md"):
        if fname not in docs:
            continue
        rows = {}
        for i, ln in enumerate(docs[fname], 1):
            m = re.match(rf"^\| \[({ID_RE})\]\(#[^)]+\) \| ([^|]+?) \|", ln)
            if m:
                rows[m.group(1)] = (m.group(2).strip(), i)
        body = {k: v for k, v in items.items() if v.file == fname}
        for k in body.keys() - rows.keys():
            r.err(f"{fname} index", f"{k} is in the body but not in the index table")
        for k in rows.keys() - body.keys():
            r.err(f"{fname}:{rows[k][1]}", f"{k} is in the index table but has no item")
        for k in body.keys() & rows.keys():
            name = body[k].name or ""
            iname = rows[k][0].replace("~~", "").strip()
            if body[k].withdrawn:
                continue
            if name and iname != name:
                r.err(f"{fname}:{rows[k][1]}", f"{k} index name '{iname}' != item name '{name}'")
    if "04-spec.md" in docs:
        text = "\n".join(docs["04-spec.md"])
        ranges = re.findall(rf"\[({ID_RE})\]\(#[^)]+\)\s*[–-]\s*\[({ID_RE})\]\(#[^)]+\)", text)
        covered = set()
        spec_items = [v for v in items.values() if v.file == "04-spec.md"]
        for start, end in ranges:
            p = id_prefix(start)
            covered.add(p)
            nums = [id_num(v.id) for v in spec_items if id_prefix(v.id) == p]
            if not nums:
                continue
            if id_num(start) != min(nums) or id_num(end) != max(nums):
                r.err("04-spec.md index", f"range {start} – {end} does not match items "
                                          f"{p}-{min(nums):02d} – {p}-{max(nums):02d}")
        for p in {id_prefix(v.id) for v in spec_items} - covered:
            r.err("04-spec.md index", f"no index range for {p}-xx")


def check_coverage(items, r):
    active = {k: v for k, v in items.items() if not v.withdrawn}
    up_targets = defaultdict(set)  # target id -> set of items pointing up to it
    for it in active.values():
        for ref in it.up_links():
            up_targets[ref].add(it.id)

    for it in active.values():
        t = it.type
        ups = it.up_links()
        if t == "P" and not any(id_type(x) == "A" for x in ups):
            r.err(loc(it), "problem has no actor in 'Affects'")
        if t == "UC":
            if not any(id_type(x) == "P" for x in ups):
                r.err(loc(it), "use case solves no problem")
            if not any(id_type(x) == "A" for x in ups):
                r.err(loc(it), "use case has no actor")
        if t == "FR" and not any(id_type(x) == "UC" for x in ups):
            r.err(loc(it), "FR does not trace to a use case")
        if t == "DR" and not any(id_type(x) == "P" for x in ups):
            r.err(loc(it), "DR does not trace to a problem")
        if t == "NFR" and not any(id_type(x) in ("P", "UC") for x in ups):
            r.err(loc(it), "NFR does not trace to a problem or use case")

        users = up_targets.get(it.id, set())
        if t == "A" and not users:
            r.err(loc(it), "actor is not used by any problem or use case")
        if t == "P" and not any(id_type(u) in ("UC", "DR", "NFR") for u in users):
            r.err(loc(it), "problem is not covered by any use case, DR or NFR")
        if t == "UC" and not any(id_type(u) == "FR" for u in users):
            r.err(loc(it), "use case is not covered by any FR")


def check_wording(items, r):
    for it in items.values():
        if it.withdrawn:
            continue
        if it.type in ("FR", "DR", "CON"):
            st = it.fields.get("Statement", "")
            if "shall" not in st:
                r.err(loc(it), "statement has no 'shall'")
            if st.count("shall") > 1:
                r.warn(loc(it), "more than one 'shall'. Is it singular?")
            if it.type == "FR":
                if not st.startswith(EARS_STARTS):
                    r.warn(loc(it), "statement does not start with an EARS keyword")
                if st.startswith("If ") and "then" not in st:
                    r.warn(loc(it), "'If' statement has no 'then' (EARS unwanted-behaviour pattern)")
            for w in VAGUE:
                if re.search(rf"(?<![\w-]){re.escape(w)}(?![\w-])", st, re.I):
                    r.warn(loc(it), f"vague word '{w}' in statement")
        for ln in it.body:
            for name in HARD_NAMES:
                if re.search(rf"\b{re.escape(name)}\b", ln) and not re.search(
                        r"e\.g\.|such as|for example|example", ln, re.I):
                    r.warn(loc(it), f"'{name}' used outside an example. Is this hard-fit?")


def cmd_check():
    items, docs, dupes = load()
    if not docs:
        print(f"No requirement files found in {REQ_DIR}")
        return 1
    r = Report()
    check_ids(items, dupes, r)
    check_fields(items, r)
    check_links(items, docs, r)
    check_refs(items, r)
    check_index(items, docs, r)
    check_coverage(items, r)
    check_wording(items, r)

    counts = defaultdict(int)
    for it in items.values():
        counts[("withdrawn " if it.withdrawn else "") + it.type] += 1
    summary = ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    print(f"reqcheck: {len(items)} items ({summary})")
    for line in r.errors + r.warnings:
        print(line)
    print(f"\n{len(r.errors)} error(s), {len(r.warnings)} warning(s)")
    return 1 if r.errors else 0


def cmd_impact(target):
    items, _, _ = load()
    if target not in items:
        print(f"Unknown ID: {target}")
        return 1
    down = defaultdict(set)       # trace links only (Affects / Solves / actors / Traces to)
    mentions = defaultdict(set)   # any other link inside an item body
    for it in items.values():
        ups = set(it.up_links())
        for ref in ups:
            down[ref].add(it.id)
        for ref in set(it.links()) - ups:
            mentions[ref].add(it.id)

    def label(i):
        it = items.get(i)
        if not it:
            return f"{i} (unknown)"
        tag = " [WITHDRAWN]" if it.withdrawn else ""
        name = it.name or it.fields.get("Statement", "").split("\n")[0]
        if len(name) > 70:
            name = name[:67] + "..."
        return f"{i} {name}{tag}".rstrip() + f"  ({it.file}:{it.line})"

    print(f"Impact of {label(target)}\n")

    print("ABOVE (what it traces to; check it still fits):")
    seen = set()

    def walk_up(i, depth):
        for ref in sorted(set(items[i].up_links())):
            if ref in seen or ref not in items or ref == i:
                continue
            seen.add(ref)
            print("  " * depth + "- " + label(ref))
            walk_up(ref, depth + 1)
    walk_up(target, 1)
    if not seen:
        print("  (nothing)")

    print("\nBELOW (what traces to it; may need to change):")
    seen2 = set()

    def walk_down(i, depth):
        for ref in sorted(down.get(i, [])):
            if ref in seen2 or ref == i:
                continue
            seen2.add(ref)
            print("  " * depth + "- " + label(ref))
            walk_down(ref, depth + 1)
    walk_down(target, 1)
    if not seen2:
        print("  (nothing)")

    print("\nMENTIONED BY (other links to it, e.g. 'used by', 'continue with'):")
    m = sorted(mentions.get(target, []))
    for ref in m:
        print("  - " + label(ref))
    if not m:
        print("  (nothing)")

    print("\nOUTSIDE docs/02-requirements (code, tests, ADRs, journal, glossary):")
    patterns = {target, target.replace("-", "_")}
    hits = 0
    skip_dirs = {".git", "node_modules", "target", "build", ".idea", ".gradle"}
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(s in p.parts for s in skip_dirs):
            continue
        if REQ_DIR in p.parents or p.suffix not in (".md", ".java", ".ts", ".tsx", ".js",
                                                    ".py", ".kt", ".yml", ".yaml", ".txt"):
            continue
        try:
            for n, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if any(re.search(rf"\b{re.escape(x)}\b", ln) for x in patterns):
                    print(f"  - {p.relative_to(ROOT)}:{n}: {ln.strip()[:100]}")
                    hits += 1
        except (UnicodeDecodeError, OSError):
            continue
    if not hits:
        print("  (nothing)")
    return 0


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    if len(argv) <= 1 or argv[1] == "check":
        return cmd_check()
    if argv[1] == "impact" and len(argv) == 3:
        return cmd_impact(argv[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
