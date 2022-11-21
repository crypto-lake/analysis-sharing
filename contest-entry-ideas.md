# Contest entry ideas

## Hummingbot backtest

Extend the Hummingbot [Pure Market Making](https://docs.hummingbot.org/strategies/pure-market-making/) strategy [backtest notebook](https://nbviewer.org/github/crypto-lake/analysis-sharing/blob/main/hummingbot_backtest.ipynb).

| compexity | description | corresponding Hummingbot parameters |
| -- | -- | -- |
| medium | Properly simulate **order refresh**, the mechanics of when orders are cancelled and re-created. | add order_refresh_time, order_refresh_tolarance_pct, minimum_spread. Maybe even filled_order_delay |
| medium | Properly simulate **inventory balancing**. eg. if you trade BTC-USDT, the strategy should alter bid/ask quote quantities to try to reach 50%-50% balance between your BTC and USDT position value. if you have $900 of BTC and $100 USDT, it should sell BTC aggressively by setting bigger ask and smaller bid quote quantities. | add inventory_skew_enabled and inventory_range_multiplier |
| easy | Add some useful **metrics** for backtest results: annualized sharpe ratio, 99-percentile daily drawdown, mean daily turnover, percentage of hours with at least one fill. the metrics should be computed by some function accepting a dataframe with fills (`df` in the code). | |
| hard | Add **liquidity mining rewards** to the total profit. That would require introducing some function computing eg. daily/weekly reward based on: our spread, our order size, average spread of others, average open order size of others, max spread for the campaign (usually 2%) and total weekly reward. <br /> Some code and explanation of Hummingbot rewards is here: <https://colab.research.google.com/drive/16jPA04Dq4N3tBon-Z2kNbyatkkeZN796?usp=sharing> (currently used spread_factor is 8). | |
<!-- | hard | Can we detect **pump and dump** events early enough to use that info profitably, perhaps by stopping to quote? This is unfortunately frequent on small-cap coins. -->

## Other topics

| compexity | description |
| -- | -- |
| easy | **Analyze arbitrage** (= price differences) on FTRB-USDT between ASCENDEX and GATEIO exchanges. You can compare mid-to-mid distance for start. Print out statistics how big the price differences are and for how long they last. |
| hard | **Backtest arbitrage** strategy for the above. |
<!-- | easy | Analyze **Leaderboard** history. How many people from historical top 10 stay there longer then eg. 3 months? For how long are people from current top 20 using Hummingbot? This would tell us more about how hard is profitable liquidity mining. <br> Use *<https://api.hummingbot.io/bounty/leaderboard?start=1667260800000&market_id=-1>* json api endpoint| -->
