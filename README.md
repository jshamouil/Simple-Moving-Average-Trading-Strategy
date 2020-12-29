# Simple-Moving-Average-Trading-Strategy

## Summary: 
This notebook aims to give an introduction into writing an automated trading algorithm. This notebook uses Alpaca Markets and it's api to receive market data and execute trades. Also note that the 10 stocks chosen were chosen for no particular reason. I also make a few assumptions, my first assumption is that there already positions in the portfolio. My second assumption is that this strategy is run once a week, this could be done using cron tab.

## The Strategy
The way the program decides to long or short a particular stock is based on calculating the moving average, in this case we are using the 10 day moving average, and based on the stock price relative to the average we decide to either buy or short the stock. This action can be seen the the ma_position function in the trading_functions class. For example if the stock price is above the moving average value we are long and if it is below then we short.

## Alpaca Trading API
In this project I use Alpaca to receive market data and execute trades. Alpaca allows users to access their paper trading platform this way we can test our strategies before putting them into production. Please note that you will need to sign up in order to use their serice to receive an api-key and secret-key. 

### Tools Used in this Project 
* Python: pandas, matplotlib 
* Alpaca API

