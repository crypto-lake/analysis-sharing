# Analysis sharing

Sharing crypto-related quantitative analyses on our [historical market data](https://crypto-lake.com/#utm_source=github&utm_medium=organic&utm_campaign=analysis-sharing&utm_term=historical-market-data), which are distinctive by including also the [order book data](https://crypto-lake.com/order-book-data/#utm_source=github&utm_medium=organic&utm_campaign=analysis-sharing&utm_term=order-book-data). This repository is curated and reviewed by *Lefty*, an experienced quant and former *Head of Research* of an equity prop-trading company, who is currently on top of the *Hummingbot* [leaderboard](https://miner.hummingbot.io/leaderboard).

## 1. Hummingbot analysis

In the first notebook, we analyze [Hummingbot](https://hummingbot.org/) market-making strategy on a combination of trade and level_1 order book data. In a very simple simulation, we can experiment with the profitability of variants of this strategy on historical data. This is intended as a basis for your own analysis, not as a direct basis for trading.

We estimate that with this data-driven backtesting approach, you can **prevent a trading loss of >=10% of your open order nominal monthly** even with a pretty simple analysis compared to the usual '*run the bot, check results after some time, tune parameters, repeat*' approach. And you save a lot of time. Note that this effect can be much bigger on volatile low-volume coins.

[**-> Open the notebook in nbviewer**](https://nbviewer.org/github/crypto-lake/analysis-sharing/blob/main/hummingbot_backtest.ipynb)

## 2. Exploratory analysis

This notebook is looking on MM profitability, spread characteristics, order-book imbalance and a few autocorrelations on high-frequency order book data. There are some interesting results on extreme order-book imbalances and short-term returns autocorrelations.

[**-> Open first of the two notebooks in nbviewer**](https://nbviewer.org/github/crypto-lake/analysis-sharing/blob/main/exploratory_analysis/Crypto_Microstructure_BTC_USDT_Exploratory_Analysis.ipynb)

## 3. TWAP detection

We detect simple every-minute TWAP orders/executions in tick data and analyze their impact on price.

[**-> Open the notebook in nbviewer**](https://nbviewer.org/github/crypto-lake/analysis-sharing/blob/main/twap_detection.ipynb)

## 4. Fake volume detection

We detect fake volume in tick data by comparing trade prices to order book bests.

[**-> Open the notebook in nbviewer**](https://nbviewer.org/github/crypto-lake/analysis-sharing/blob/main/fake_volume_detection.ipynb)

---

## Contributing

There are a few contribution rules:

- quant research rule #1: keep things simple (*KISS*)
- keep the code clean, extract repeated code into functions or modules (DRY)
- each notebook should have markdown intro description in its header and conclusions in the footer
- prefer realistic simulation to smart trading logic/model

See the list of freely available [sample data](available-sample-data.png) or the [data schemata](https://crypto-lake.com/data/).

---

## Usage

Run locally with python3.8 or later. Install requirements.txt and run using `jupyter notebook` shell command.

Or run online via *Binder* using the link to *nbviewer* above and then click the three rings icon to the top-right.

## FAQ

- Q: Can you share your alpha? / Should we share our alpha?
  - A: No. The point of quant research is that everyone should come up with his own 'alpha'. This repository and *Lake* project just aim to make this easier by sharing the basics.
- Q: Can I also use other data than *Lake*?
  - A: Sure, but don't mix data sources unless necessary.
- Q: Where can I follow *Lake* and sharing analyses?
  - A: <a href="https://twitter.com/intent/user?screen_name=crypto_lake_com">Follow us on Twitter</a>
