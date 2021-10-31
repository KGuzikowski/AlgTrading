import talib


class Indicator:
    prev_states = []

    def __init__(self, timeperiod):
        self._timeperiod = timeperiod

    def __function(self):
        raise NotImplementedError()

    def __call__(self, df):
        """
        return:
        1 -> sell
        0 -> do nothing
        -1 -> buy
        """
        return self._function(df)


class RSI(Indicator):
    def __init__(self, timeperiod, lower, upper):
        super().__init__(timeperiod)
        self._lower = lower
        self._upper = upper

    def _function(self, df):
        rsi = talib.RSI(df.close.tail(self._timeperiod + 1), timeperiod=self._timeperiod).iloc[-1]
        
        if rsi >= self._upper:
            return 1
        elif rsi <= self._lower:
            return -1
        else:
            return 0


class BollingerBands(Indicator):
    def __init__(self, timeperiod, lower=2, upper=3):
        super().__init__(timeperiod)
        self._lower = lower
        self._upper = upper

    def _function(self, df):
        lower, middle, upper = talib.BBANDS(
            df.close.tail(self._timeperiod + 1),
            timeperiod=self._timeperiod,
            nbdevup=self._upper,
            nbdevdn=self._lower,
            matype=0,
        )
        closing =  df.close.iloc[-1]

        if closing >= upper.iloc[-1]:
            return 1
        elif closing <= lower.iloc[-1]:
            return -1
        else:
            return 0

class EMACross(Indicator):
    """
    If small EMA crosses big EMA from bottom -> buy
    If small EMA crosses big EMA from top -> sell
    """
    def __init__(self, timeperiod_S=100, timeperiod_B=500):
        self._timeperiod_S = timeperiod_S
        self._timeperiod_B = timeperiod_B

    def _function(self, df):
        ma_S = talib.EMA(df.close.tail(self._timeperiod_S + 1), timeperiod=self._timeperiod_S)
        ma_B = talib.EMA(df.close.tail(self._timeperiod_B + 1), timeperiod=self._timeperiod_B)

        ma_S0 = ma_S.iloc[-2]
        ma_S1 = ma_S.iloc[-1]
        ma_B0 = ma_B.iloc[-2]
        ma_B1 = ma_B.iloc[-1]

        if ma_S0 >= ma_B0 and ma_S1 <= ma_B1:
            # cross from top
            return 1
        elif ma_S0 <= ma_B0 and ma_S1 >= ma_B1:
            # cross from bottom
            return -1
        else:
            return 0



class EMA(Indicator):
    """
    If price crosses EMA from bottom -> buy
    If price crosses EMA from top -> sell
    """
    def __init__(self, timeperiod):
        super().__init__(timeperiod)

    def _function(self, df):
        ma = talib.EMA(df.close.tail(self._timeperiod + 1), timeperiod=self._timeperiod)

        ma0 = ma.iloc[-2]
        ma1 = ma.iloc[-1]
        close0 = df.close.iloc[-2]
        close1 = df.close.iloc[-1]

        if ma0 >= close0 and ma1 <= close1:
            # cross from top
            return 1
        elif ma0 <= close0 and ma1 >= close1:
            # cross from bottom
            return -1
        else:
            return 0


class NormalizedEMACross(Indicator):
    """
    If small EMA crosses big EMA from bottom -> buy
    If small EMA crosses big EMA from top -> sell
    """
    def __init__(self, timeperiod_S=100, timeperiod_B=500):
        self._timeperiod_S = timeperiod_S
        self._timeperiod_B = timeperiod_B

    def _function(self, df):
        ma_S = talib.EMA(df.close.tail(self._timeperiod_S + 1), timeperiod=self._timeperiod_S)
        ma_S = (ma_S-ma_S.mean())/ma_S.std()
        ma_B = talib.EMA(df.close.tail(self._timeperiod_B + 1), timeperiod=self._timeperiod_B)
        ma_B = (ma_B-ma_B.mean())/ma_B.std()

        ma_S0 = ma_S.iloc[-2]
        ma_S1 = ma_S.iloc[-1]
        ma_B0 = ma_B.iloc[-2]
        ma_B1 = ma_B.iloc[-1]

        if ma_S0 >= ma_B0 and ma_S1 <= ma_B1:
            # cross from top
            return 1
        elif ma_S0 <= ma_B0 and ma_S1 >= ma_B1:
            # cross from bottom
            return -1
        else:
            return 0


class NormalizedEMA(Indicator):
    """
    If normalized EMA > 0 -> sell
    If normalized EMA < 0 -> buy
    """
    def __init__(self, timeperiod=200):
        self._timeperiod = timeperiod

    def _function(self, df):
        ma = talib.EMA(df.close.tail(self._timeperiod + 1), timeperiod=self._timeperiod)
        ma = (ma-ma.mean())/ma.std()

        ma = ma.iloc[-1]
        print(ma)

        if ma > 0:
            return 1
        elif ma < 0:
            return -1
        else:
            return 0