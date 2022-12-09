# Analysis sharing

Sharing crypto-related quantitative analyses on our [historical market data](https://crypto-lake.com/#data), which are distinctive by including also the [order book data](https://crypto-lake.com/order-book-data/). This repository is curated and reviewed by *Lefty*, an experienced quant and former *Head of Research* of an equity prop-trading company, who is currently on top of the *Hummingbot* [leaderboard](https://miner.hummingbot.io/leaderboard).

## 1. Hummingbot analysis

In the first notebook, we analyze [Hummingbot](https://hummingbot.org/) market-making strategy on a combination of trade and level_1 order book data. In a very simple simulation, we can experiment with the profitability of variants of this strategy on historical data. This is intended as a basis for your own analysis, not as a direct basis for trading.

We estimate that with this data-driven backtesting approach, you can **prevent a trading loss of >=10% of your open order nominal monthly** even with a pretty simple analysis compared to the usual '*run the bot, check results after some time, tune parameters, repeat*' approach. And you save a lot of time. Note that this effect can be much bigger on volatile low-volume coins. To support this in the Hummingbot community, we offer a [50% data discount](https://crypto-lake.com/#hbot) with discount code *HBOT50*.

[**-> Open the notebook in nbviewer**](https://nbviewer.org/github/crypto-lake/analysis-sharing/blob/main/hummingbot_backtest.ipynb)

---

## Competition

We would like to support data-driven research in the field of cryptocurrency trading and especially market-making. We encourage you to share your analyses and contribute to the existing ones in this repository by opening pull requests. For your effort, you get a review of your analysis ideas and code, which will help you get better at quantitative analysis and its implementation.

Whoever contributes the best pull request into this repository, be it a new notebook or an improvement of an existing one will **win a 1 year free *Crypto Lake* data subscription** (worth $480) and therefore access to up to 2 years of history of around 60 trading pairs for both big cap crypto tokens and small tokens traded in the Hummingbot liquidity campaigns. You can qualify by having any pull request merged by the end of 2022.

To clarify, the contributions don't have to be related to Hummingbot or its pure market-making strategy, they don't have to be profitable, but should be valuable by bringing insight into the market. You can even just contribute a slight modification of your existing research. We reserve the right to choose the best contribution or have a community vote.

**To join the competition, email us at hi (at) crypto-lake (.) com**. We will send you back some research tips for the start.

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
- Q: Can you give me the market data for free?
  - A: We actually have to pay to collect them and even pay for the traffic when you're downloading them from AWS.
- Q: Can I also use other data than *Lake*?
  - A: Sure, but don't mix data sources unless necessary.
- Q: I need more data for my competition contribution, can you provide it?
  - A: Probably yes, ask us once you open PR and send some code, so we can assess.
- Q: Must the code be perfect? I am concerned with my programming skills.
  - A: No, the code is secondary to a good analysis. Just clean it up and perhaps consider its readability before first opening PR. We prefer early PRs to perfect PRs.
- Q: Can I order a paid data subscription and then participate/win the competition?
  - A: Sure, If you win, we will stop charging the subscription fee for a year.
- Q: When should I submit my entry?
  - A: The competition ends at the end of December, but in order to get the code merged, I would suggest opening a Pull Request in mid-December at the latest. Or you can open a PR with incomplete code even earlier if you want more feedback on the ideas and not just the code.
- Q: Where can I follow *Lake* and this competition?
  - A: <a href="https://twitter.com/intent/user?screen_name=crypto_lake_com">Follow us on Twitter</a>
