# Glossary

## Market data

**Exchange**
A place where people buy and sell coins (such as Binance). It also publishes prices.

![Binance Exchange](../images/binance_exchange.png)

**Currency Pair**
The two things being traded. "BTC/USDT" means buying or selling Bitcoin with USDT (a coin that stays close to 1 US dollar).

![Currency Pair](../images/currency_pair.png)

**Candle**
Prices change every second, which is too much data to read. A candle sums up one time period in five numbers: **Open** (first price), **High**, **Low**, **Close** (last price) and **Volume** (how much was traded).

![Candlestick Patterns](../images/candlestick_patterns.png)

**Timeframe**
The length of one candle: 1 minute, 5 minutes, 1 hour, 1 day… Short timeframes show detail. Long timeframes show the big direction.

![Timeframe](../images/timeframe.png)

**Historical data / Live data**
Historical data is old candles, used for testing. Live data is the price right now, sent as it changes.

![Historical Data and Live Data](../images/historical_vs_live.png)

## Strategies

**Indicator**
Raw prices are noisy. An indicator is a number calculated from past prices to make a pattern easier to see. Example: an average price.

![Trading Indicators](../images/trading_indicators.png)

**Signal**
The output of a strategy at one moment: **BUY**, **SELL** or **HOLD** (do nothing).

![Signal](../images/signal.png)

**Strategy**
A rule that turns indicators into signals. Example: "If the price goes above its 20-candle average, BUY."

![Strategy](../images/strategy.png)

**Parameter**
A setting inside a strategy, such as "20" in "20-candle average". The same strategy with different parameters can give very different results.

![Parameter](../images/parameter.png)

**Composite strategy**
One strategy alone often fails when the market changes. A composite strategy combines several strategies into one, with a rule for what to do when they disagree (for example, a vote).

![Composite Strategy](../images/composite_strategy.png)

**Moving Average (MA)**
The average closing price of the last N candles. It smooths out noise and shows the direction of the price.

![Moving Average](../images/moving_average.png)

**RSI (Relative Strength Index)**
A number from 0 to 100 that shows how strongly the price has moved recently. Very high can mean "rose too fast". Very low can mean "fell too fast".

![RSI](../images/rsi.png)

**Bollinger Bands**
Three lines around the price: an average in the middle, and one line above and below. The outer lines move further apart when the price jumps around more.

![Bollinger Bands](../images/bollinger_bands.png)

**Support / Resistance**
Price levels where the price often stopped before. Support is a level where falling often stopped. Resistance is a level where rising often stopped.

![Support and Resistance](../images/support_resistance.png)

**Market regime**
The current "mood" of the market: going up, going down, or moving sideways. A strategy that works in one regime can fail in another.

![Market Regime](../images/market_regime.png)

## Testing

**Backtest**
We cannot test a strategy on the future. A backtest replays the past: it pretends to trade with the strategy on old candles and records every trade.

![Backtest](../images/backtest.png)

**Trade**
One buy followed by one sell. It has an entry (price and time in) and an exit (price and time out).

![Trade](../images/trade.png)

**Trading fee**
The exchange takes a small cut of every trade. A strategy that trades very often can look profitable before fees and lose money after fees.

![Trading Fee](../images/trading_fee.png)

**Slippage**
The difference between the price you wanted and the price you actually got. It happens because the price moves while the order is filled.

![Slippage](../images/slippage.png)

**Look-ahead bias**
A test bug where the strategy uses information that was not known yet at that time. Example: deciding at 9:00 using the 9:00–9:05 candle's close price. Results look great but are impossible in real life.

![Look-ahead Bias](../images/look_ahead_bias.png)

**Overfitting**
A strategy that fits old data too closely, by luck, instead of finding a real pattern. It looks great in the backtest and fails on new data. The more combinations you try, the higher the risk.

![Overfitting](../images/overfitting.png)

**In-sample / Out-of-sample**
In-sample data is the data used to choose the best parameters. Out-of-sample data is data the strategy has never seen. Only out-of-sample results show if a strategy really works.

![In-sample and Out-of-sample](../images/in_sample_out_of_sample.png)

**Walk-forward test**
One out-of-sample check can be lucky too. A walk-forward test repeats it: choose parameters on one period, test on the next period, slide both forward, repeat. The final result joins only the test periods.

![Walk-forward Test](../images/walk_forward_test.png)

**Reproducibility**
Being able to run the same test again and get exactly the same result. It requires knowing the exact strategy version, parameters and data used.

![Reproducibility](../images/reproducibility.png)

## Measuring results

**Return**
How much money was gained or lost, as a percentage of the starting money.

![Return](../images/return.png)

**Win rate**
The share of trades that made money. A high win rate is not enough: many small wins can be wiped out by one big loss.

![Win Rate](../images/win_rate.png)

**Maximum drawdown (MDD)**
The biggest drop from a peak to a later low. It shows the worst pain a person would have felt. Example: 100 → 120 → 90 gives a drawdown of −25%.

![Maximum Drawdown](../images/max_drawdown.png)

**Profit factor**
Total money from winning trades divided by total money lost in losing trades. Above 1 means the strategy made more than it lost.

![Profit Factor](../images/profit_factor.png)

**Sharpe ratio**
Return alone ignores risk. The Sharpe ratio measures return per unit of risk (how much the results jump around). Higher is better.

![Sharpe Ratio](../images/sharpe_ratio.png)

## Search and ranking

**Search space**
All the strategy combinations and parameters that could be tested. It grows very fast as you add strategies and parameters.

![Search Space](../images/search_space.png)

**Random search**
Pick combinations at random from the search space and test them.

![Random Search](../images/random_search.png)

**Domain-guided search**
Use market knowledge to limit the search. Example: every combination must include one trend strategy and one momentum strategy.

![Domain-guided Search](../images/domain_guided_search.png)

**Genetic algorithm**
A search method copied from evolution: keep the best combinations, mix and change them a little, and test the new ones.

![Genetic Algorithm](../images/genetic_algorithm.png)

**Leaderboard**
A ranking table of the best strategies found so far, with their scores.

![Leaderboard](../images/leaderboard.png)

**Top-K**
Keep only the K best strategies on the leaderboard (for example, the top 10).

![Top-K](../images/top_k.png)

**Stop condition**
A rule that ends a search. Examples: after 1,000 candidates, after 1 hour, or after 50 tries with no improvement.

![Stop Condition](../images/stop_condition.png)

## News

**Sentiment**
Whether a piece of news is good, bad or neutral for the price. Often given as a label (POSITIVE / NEUTRAL / NEGATIVE) and a score.

![Sentiment](../images/sentiment.png)

**Sentiment analysis**
Using a machine learning model to read news text and guess its sentiment.

![Sentiment Analysis](../images/sentiment_analysis.png)
