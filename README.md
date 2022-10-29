# Analysis sharing

Sharing quantitative analyses on [Lake data](https://crypto-lake.com/#data).

## Hummingbot analysis

In the first notebook we analyse [Hummingbot](https://hummingbot.org/) market-making strategy on a combination of trade and level1 order book data. In a very simple simulation we can experiment with the profitability of variants of this strategy on historical data.

[**-> Open the notebook**](https://nbviewer.org/github/crypto-lake/analysis-sharing/blob/hb-backtest/hummingbot_backtest.ipynb)

We estimate that with this data-driven backtesting approach, you can **prevent a trading loss of 5% of your open order nominal monthly** even with a pretty simple analysis compared to the usual '*run the bot, check results after some time, tune parameters, repeat*' approach. Plus you save a lot of time. Note that this loss can be much bigger on volatile low-volume coins.

## Contributing

We would like to support data-driven research in the field of cryptocurrency trading and especially market-making. We encourage you to share your analyses and contribute to the existing ones in this repository by opening pull requests.

## Competition

Whoever contributes the best pull request into this repository, be it a new notebook or an improvement of an existing one will win a 1 year free *Crypto Lake* subscription and therefore access to up to 2 years of history of around 60 trading pairs for both big cap crypto tokens and small tokens traded in the Hummingbot liquidity campaigns. You can qualify by having any pull request merged by the end of 2022.

To clarify, the contributions don't have to be related to Hummingbot or its pure market-making strategy, they don't have to be profitable, but should be valuable by bringing insight into the market.

## Usage

Run locally with python3.8+. Install requirements.txt and run using `jupyter notebook` shell command.

Or run online via Binder using the link to nbviewer above and then the three rings icon to the top-left.
