# Get data from : http://pythonprogramming.net/static/downloads/machine-learning-data/intraQuarter.zip
import pandas as pd
import os
import time
from datetime import datetime

path = '/Users/mohammedjalil/github/ml-invest/data/intraQuarter'

def Key_Stats(gather='Total Debt/Equity (mrq)'):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    print(stock_list)

Key_Stats()

