# Name
"""farzam"""

# Requires
import pandas_ta as pd
import pandas_ta as ta
from functions.pandas_ta_supplementary_libraries import *


# Set parameters
def set_parameters(strategy, df):
    return {}

# Indicators

std_stdev20 = ta.stdev(strategy.df_base.close_price, length=20)
hma_250      = ta.hma(strategy.df_base.close_price,250)
# change_hma26 = ta.change(hma_250)

long_top  = 0.0
long_bot  = 0.0
long_diff = 0.0
short_top  = 0.0
short_bot  = 0.0
short_diff = 0.0
counter    = 0
topPer = 250
botPer = 250
long_trade = False
short_trade = False
highest_list = []
lowest_list = []
stop_loss_general   = 2.0
entry_price = 0.0
stop_loss_general_used = False


# Trade
print(candle)   
if counter > 0:
    counter= counter - 1
if std_stdev20.iat[candle] >= 300:
    counter = 240

top             = highest(strategy.df_base["high_price"], 250-counter, candle)
bot             = lowest(strategy.df_base["low_price"], 250-counter, candle)
diff            = top - bot
lowest_lookbacked = lowest(strategy.df_base["low_price"],  botPer-counter, candle)
highest_lookbacked = highest(strategy.df_base["high_price"],  topPer-counter, candle)
# same_lowest_cond =lowest_lookbacked == lowest(strategy.df_base["low_price"], 250-counter,candle-1) ==  lowest(strategy.df_base["low_price"], 250-counter, candle-2)== lowest(strategy.df_base["low_price"], 250-counter, candle-3) == lowest(strategy.df_base["low_price"], 250-counter, candle-4)
lowest_list.append(lowest_lookbacked)
highest_list.append(highest_lookbacked)
if len(lowest_list) > 5:
    same_lowest_cond =lowest_lookbacked >= lowest_list[-5]
else:
    same_lowest_cond = False
if len(highest_list) > 5:
    same_highest_cond =highest_lookbacked <= highest_list[-5]
else:
    same_highest_cond = False

if  close>= long_bot+ 0.9 * long_diff and long_trade:
    strategy.exit(candle, "exit long", from_entry="My Long Entry Id",comment = "take profit")
    long_top  = 0.0
    long_bot  = 0.0
    long_diff = 0.0
    long_trade = False
    entry_price = 0.0


if  close <= long_bot - 0.9 * long_diff and long_trade:
    strategy.exit(candle, "exit long","My Long Entry Id",comment = "stop loss")
    long_top  = 0.0
    long_bot  = 0.0
    long_diff = 0.0   
    long_trade = False 
    entry_price = 0.0

        
if  close <= short_top - 0.9 * short_diff and short_trade:
    strategy.exit(candle, "exit short", from_entry="My Short Entry Id",comment = "take profit")
    short_top  = 0.0
    short_bot  = 0.0
    short_diff = 0.0
    short_trade = False
    entry_price = 0.0

if  close >= short_top + 0.9 * short_diff and short_trade:
    strategy.exit(candle, "exit short","My Short Entry Id",comment = "stop loss")
    short_top  = 0.0
    short_bot  = 0.0
    short_diff = 0.0  
    short_trade = False  
    entry_price = 0.0

if std_stdev20.iat[candle] <= 200:
    position = strategy.position_size()
    if close <= bot + 0.2 * diff and position[0]==0 and position[1]==0 and same_lowest_cond and not stop_loss_general_used: 
        strategy.entry(candle, "My Long Entry Id", "long")
        long_top  = top
        long_bot  = bot
        long_diff = diff
        long_trade = True
        short_trade = False
        entry_price = close

    if close >= bot + 0.8 * diff and position[0]==0 and position[1]==0 and same_highest_cond and not stop_loss_general_used: 
        strategy.entry(candle, "My Short Entry Id", "short")
        short_top  = top
        short_bot  = bot
        short_diff = diff
        short_trade = True
        long_trade = False
        entry_price = close
                       
if long_trade and close <= entry_price * 0.98:
    strategy.exit(candle, "exit long","My Long Entry Id",comment = "stop loss general")
    stop_loss_general_used =True

if short_trade and close >= entry_price * 1.02:
    strategy.exit(candle, "exit short","My Short Entry Id",comment = "stop loss general")
    stop_loss_general_used =True

if stop_loss_general_used :
    if long_bot != 0 and (close <= long_bot - 0.9 * long_diff or  close >= long_bot + 0.9 * long_diff) :
        long_top  = 0.0
        long_bot  = 0.0
        long_diff = 0.0   
        long_trade = False 
        entry_price = 0.0
        stop_loss_general_used = False

    if short_top != 0 and ( close >= short_top + 0.9 * short_diff or close <= short_top - 0.9 * short_diff) :
        short_top  = 0.0
        short_bot  = 0.0
        short_diff = 0.0  
        short_trade = False  
        entry_price = 0.0
        stop_loss_general_used = False
