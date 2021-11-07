import binance.client
import pandas as pd
import numpy as np
import datetime as dt


import talib
from talib import MA_Type

from BinanceClient import BinanceClient
from BinanceClient import get_data

def crypto_data():
  ret_val = {}
  ret_val["df_BTC"] = get_data(dt.datetime(2021,10,7,10,0,0), "BTCUSDT")
  ret_val["df_Doge"] = get_data(dt.datetime(2021,10,7,10,0,0), "DOGEUSDT")
  ret_val["df_ETH"] = get_data(dt.datetime(2021,10,7,10,0,0), "ETHUSDT")
  ret_val["df_PAXG"] = get_data(dt.datetime(2021,10,7,10,0,0), "PAXGUSDT")
  ret_val["df_ONE"] = get_data(dt.datetime(2021,10,7,10,0,0), "ONEUSDT")
  ret_val["df_OXT"] = get_data(dt.datetime(2021,10,7,10,0,0), "OXTUSDT")
  ret_val["df_HNT"] = get_data(dt.datetime(2021,10,7,10,0,0), "HNTUSDT")
  ret_val["df_LINK"] = get_data(dt.datetime(2021,10,7,10,0,0), "LINKUSDT")

  for df in ret_val.values():
    period = 200
    upper, middle, lower = talib.BBANDS(
            df.close,
            timeperiod=period,
            nbdevup=3,
            nbdevdn=2,
            matype=0,
        )
    
    #Bollinger bands
    df["upper_BB"] = upper
    df["lower_BB"] = lower
    df["middle_BB"] = middle

    df["price"] = df.close.astype(float)
    df["ma"] = talib.EMA(df["price"], timeperiod=200)
    df['ADX0'] = talib.ADX(
        df.high,
        df.low,
        df.close,
        timeperiod=20
    )

    df.ADX0 = (df.ADX0-df.ADX0.min())/(df.ADX0.max()-df.ADX0.min())
    df["ADX0var"] = talib.VAR(df.ADX0, timeperiod=20, nbdev=1)
    df.ADX0var = (df.ADX0var-df.ADX0var.min())/(df.ADX0var.max()-df.ADX0var.min())
    df['ADX1'] = talib.ADX(
        df.high,
        df.low,
        df.close,
        timeperiod=100
    )

    df.ADX1 = (df.ADX1-df.ADX1.min())/(df.ADX1.max()-df.ADX1.min())
    df["ADX1var"] = talib.VAR(df.ADX1, timeperiod=20, nbdev=1)
    df.ADX1var = (df.ADX1var-df.ADX1var.min())/(df.ADX1var.max()-df.ADX1var.min())
    df['ADX2'] = talib.ADX(
        df.high,
        df.low,
        df.close,
        timeperiod=700
    )

    df.ADX2 = (df.ADX2-df.ADX2.min())/(df.ADX2.max()-df.ADX2.min())
    df["ADX2var"] = talib.VAR(df.ADX2, timeperiod=20, nbdev=1)
    df.ADX2var = (df.ADX2var-df.ADX2var.min())/(df.ADX2var.max()-df.ADX2var.min())
    

        #ATR
    df['ATR0'] = talib.ATR(
        df.high,
        df.low,
        df.close,
        timeperiod=20
    )
    df['ATR0'] = (df.ATR0-df.ATR0.min())/(df.ATR0.max()-df.ATR0.min())

    df['ATR1'] = talib.ATR(
        df.high,
        df.low,
        df.close,
        timeperiod=100
    )
    df['ATR1'] = (df.ATR1-df.ATR1.min())/(df.ATR1.max()-df.ATR1.min())

    df['ATR2'] = talib.ATR(
        df.high,
        df.low,
        df.close,
        timeperiod=700
    )
    df['ATR2'] = (df.ATR2-df.ATR2.min())/(df.ATR2.max()-df.ATR2.min())


    df['ARO0'] = talib.AROONOSC(
    high=df.high,
    low=df.low,
    timeperiod=20
    )
    df['ARO1'] = talib.AROONOSC(
        high=df.high,
        low=df.low,
        timeperiod=100
    )
    df['ARO2'] = talib.AROONOSC(
        high=df.high,
        low=df.low,
        timeperiod=700
    )



    df['WLR0'] = talib.WILLR(
        df.high,
        df.low,
        df.close,
        timeperiod=20
    )

    df['WLR1'] = talib.WILLR(
        df.high,
        df.low,
        df.close,
        timeperiod=100
    )

    df['WLR2'] = talib.WILLR(
        df.high,
        df.low,
        df.close,
        timeperiod=700
    )


    df.dropna(inplace = True)


    df["pricema"] = df.price / df.ma

    #normalising 
    df.ARO0 += 100
    df.ARO0 /= 200
    df.ARO0

    df.ARO1 += 100
    df.ARO1 /= 200
    df.ARO1

    df.ARO2 += 100
    df.ARO2 /= 200
    df.ARO2

    df.WLR0 += 100
    df.WLR0 /= 100

    df.WLR1 += 100
    df.WLR1 /= 100

    df.WLR2 += 100
    df.WLR2 /= 100
    df.WLR0



  return ret_val
