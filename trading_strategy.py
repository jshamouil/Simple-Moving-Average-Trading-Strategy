from trading_functions import trading_functions 
import math
api = trading_functions()

# defind the period for our moving average
time_frame = 10

#get stock symbols in our current portolio
n=len(api.api.list_positions())
stocks = []
for i in range(0,n):
    stocks.append(api.api.list_positions()[i].symbol)
print(stocks)

# let's calculate the position of each stock based on our moving average model
positions = []
for i in stocks:
    pos = api.ma_position(time_frame,i)
    positions.append(pos)
    
# for now we'll keep it simple by allocating an equal amont to each asset
stock_data = api.get_pandas_barset(stocks,'day',time_frame)
closing_prices = []
for symbol in stocks:
    x = stock_data[symbol].iloc[-1].close
    closing_prices.append(x)
    
quantity = []
buying_power = float(api.api.get_account().buying_power)
stock_cap = buying_power / n
for i in range(0,n):
    x = math.floor(stock_cap/closing_prices[i])
    quantity.append(x)
    
#close all positions
api.close_all_positions()

# purchase stocks
for i in range(0,n):
        api.api.submit_order(
            symbol = stocks[i],
            qty = quantity[i],
            side = positions[i],
            type = 'market',
            time_in_force = 'gtc'
        )