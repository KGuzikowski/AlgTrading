import binance.client
import pandas as pd
import numpy as np
import datetime as dt


import talib
from talib import MA_Type

from BinanceClient import BinanceClient
from BinanceClient import get_data

def crypto_data(timeperiods):
  ret_val = {}
  ret_val["df_BTC"] = get_data(dt.datetime(2021,10,7,10,0,0), "BTCUSDT")
  ret_val["df_Doge"] = get_data(dt.datetime(2021,10,7,10,0,0), "DOGEUSDT")
  ret_val["df_ETH"] = get_data(dt.datetime(2021,10,7,10,0,0), "ETHUSDT")
  ret_val["df_PAXG"] = get_data(dt.datetime(2021,10,7,10,0,0), "PAXGUSDT")
  ret_val["df_ONE"] = get_data(dt.datetime(2021,10,7,10,0,0), "ONEUSDT")
  ret_val["df_OXT"] = get_data(dt.datetime(2021,10,7,10,0,0), "OXTUSDT")
  ret_val["df_HNT"] = get_data(dt.datetime(2021,10,7,10,0,0), "HNTUSDT")
  ret_val["df_LINK"] = get_data(dt.datetime(2021,10,7,10,0,0), "LINKUSDT")

  ret_val = prepare_data(ret_val, timeperiods)
  return ret_val


def prepare_data(ret_val, timeperiods):



  for df in ret_val.values():
    upper, middle, lower = talib.BBANDS(
            df.close,
            timeperiod=timeperiods["BB"],
            nbdevup=3,
            nbdevdn=2,
            matype=0
        )
    
    #Bollinger bands
    df["upper_BB"] = upper
    df["lower_BB"] = lower
    df["middle_BB"] = middle

    df["price"] = df.close.astype(float)
    df["ma"] = talib.EMA(df["price"], timeperiod=timeperiods["EMA"])
    df['ADX0'] = talib.ADX(
        df.high,
        df.low,
        df.close,
        timeperiod=timeperiods["ADX0"] #20
    )

    df.ADX0 = (df.ADX0-df.ADX0.min())/(df.ADX0.max()-df.ADX0.min())
    df["ADX0var"] = talib.VAR(df.ADX0, timeperiod=timeperiods["ADX0var"], nbdev=1)
    df.ADX0var = (df.ADX0var-df.ADX0var.min())/(df.ADX0var.max()-df.ADX0var.min())
    

        #ATR
    df['ATR0'] = talib.ATR(
        df.high,
        df.low,
        df.close,
        timeperiod=timeperiods["ATR0"] 
    )
    df['ATR0'] = (df.ATR0-df.ATR0.min())/(df.ATR0.max()-df.ATR0.min())

    df['ARO0'] = talib.AROONOSC(
    high=df.high,
    low=df.low,
    timeperiod=timeperiods["ARO0"]
    )


    df['WLR0'] = talib.WILLR(
        df.high,
        df.low,
        df.close,
        timeperiod=timeperiods["WLR0"]
    )


    df.dropna(inplace = True)


    df["pricema"] = df.price / df.ma

    #normalising 
    df.ARO0 += 100
    df.ARO0 /= 200
    df.ARO0

    df.WLR0 += 100
    df.WLR0 /= 100


  return ret_val
