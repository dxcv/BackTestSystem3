
import yaml
import os
import pymongo
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
from .base import HoldingClass, BacktestSys


class test(BacktestSys):
    def __init__(self):
        self.current_file = __file__
        self.prepare()

    def strategy(self):
        holdingsObj = HoldingClass(self.dt)
        for k, v in self.data['future_price'].items():
            cls = v.CLOSE
            ma20 = pd.DataFrame(cls).rolling(window=20).mean().values.flatten()
            ma10 = pd.DataFrame(cls).rolling(window=10).mean().values.flatten()
            con = np.zeros(cls.shape)
            con[(cls > ma20) * (cls > ma10)] = 1
            con[(cls < ma10) * (cls > ma20)] = 0
            con[(cls < ma20) * (cls < ma10)] = -1
            con[(cls > ma10) * (cls < ma20)] = 0
            holdingsObj.add_holdings(k, con)
        return holdingsObj


if __name__ == '__main__':

    a = test()
    holdings = a.strategy()
    holdings = a.holdingsStandardization(holdings, mode=3)
    holdings = a.holdingsProcess(holdings)
    a.displayResult(holdings)
