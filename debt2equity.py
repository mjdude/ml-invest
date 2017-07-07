# Get data from : http://pythonprogramming.net/static/downloads/machine-learning-data/intraQuarter.zip
import pandas as pd
import os
import time
from datetime import datetime

path = '/Users/mohammedjalil/github/ml-invest/data/intraQuarter'

def Key_Stats(gather='Total Debt/Equity (mrq)'):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    #print(stock_list)

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        #make sure to skip folders with no files in them
        if len(each_file) > 0:
            for file in each_file:
                data_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(data_stamp.timetuple())
                print(data_stamp, unix_time)
                time.sleep(15)


Key_Stats()

