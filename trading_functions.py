#this is a class that contains functions for alpaca trading

import math
import matplotlib.pyplot as plt
import pandas as pd
import alpaca_trade_api as tradeapi

class trading_functions:
    
    def __init__(self):
        self.api_key = "api-key"
        self.secret_key = "secret-key"
        self.end_point_url = "https://paper-api.alpaca.markets"
        self.api = tradeapi.REST(self.api_key, self.secret_key, self.end_point_url)
        
    def positions(self):
        return self.api.list_positions()
    
    #here we will convert the stock data to a data frame
    def get_pandas_barset(self, symbols, timeframe, limit, start = None, end=None, after=None, until=None):
        bar_set = self.api.get_barset(symbols, timeframe, limit, start, end, after, until)
        dataframes = {}

        for symbol in bar_set.keys():
            bars = bar_set[symbol]

            data = {
                'close': [bar.c for bar in bars],
                'high': [bar.h for bar in bars],
                'low': [bar.l for bar in bars],
                'open': [bar.o for bar in bars],
                'time': [bar.t for bar in bars],
                'volume': [bar.v for bar in bars]
            }

            dataframes[symbol] = pd.DataFrame(data)

        return dataframes
    
    #this is a function that closes all long or short positions
    def close_all_positions(self):
        self.api.cancel_all_orders()
        positions = self.api.list_positions()

        for position in positions:
            #make sure to cover short positions
            if (position.side == 'short'):
                side = 'buy'
            else:
                side = 'sell'

            self.api.submit_order(
                symbol = position.symbol,
                qty = abs(int(position.qty)),
                side = side,
                type = 'market',
                time_in_force = 'gtc'
            )

        return 
    
    def ma_position(self,n,ticker):
        bar_set = self.api.get_barset(ticker, "day", n)
        bars = bar_set[ticker]

        close = []

        for i in range(0,n):
            close.append(bars[i].c)

        x = math.floor(math.sqrt(100*2))
        ten_d = [0]*x
        for i in range(x,n):
            s = 0
            for j in range(i-x,i):
                s = s+close[j]
            ten_d.append(s/x)

        if (close[-1]>ten_d[-1]):
            return "buy"
        else:
            return "sell"
        
    def simple_ma(self, days, ticker):
        bar_set = self.api.get_barset(ticker, "day", days)
        bars = bar_set[ticker]
        s = 0
        for i in range(0,days):
            s=s+bars[i].c
        return s/days
    
    def ma_chart(self, days, ticker, ma):
        n=days
        x=ma
        close = []
        bar_set = self.api.get_barset(ticker, "day", n)
        for i in range(0,n):
            close.append(bar_set[ticker][i].c)

        x_ma = []
        for j in range(x,n):
            s=0
            for k in range(j-x,j):
                s = s+close[k]
            x_ma.append(s/x)

        plt.plot(close[x:-1])
        plt.plot(x_ma[x:-1])
        return