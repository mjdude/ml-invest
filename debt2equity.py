# Get data from : http://pythonprogramming.net/static/downloads/machine-learning-data/intraQuarter.zip
import pandas as pd
import os
import time
from datetime import datetime

path = '/Users/mohammedjalil/github/ml-invest/data/intraQuarter'

def Key_Stats(gather='Total Debt/Equity (mrq)'):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date', 'Unix', 'Ticker', 'DE Ratio'])
    sp500_df = pd.DataFrame.from_csv('data/yahoo-s&p/^GSPC.csv')

    for each_dir in stock_list[1:]:
        # print('dir is ', each_dir )
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("KeyStats/")[1]
        # print('ticker is ', ticker)
        #make sure to skip folders with no files in them
        if len(each_file) > 0:
            for file in each_file:
                # print('file is ', file)
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir + '/' + file
                source = open(full_file_path, 'r').read()
                try:
                    value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    # print('value is ', value)
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        # print('date is ', sp500_date)
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        # print('row is :', row)
                        sp500_value = float(row['Adj Close'])
                    except Exception as e:
                        # print(e)
                        # If on the weekend we go back 3 days (259200) so we get data from the weekday
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        # print('date is ', sp500_date)
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        # print('row is :', row)
                        sp500_value = float(row['Adj Close'])
                    
                    stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    print('stock price: ', stock_price, ' ticker: ', ticker)

                    df = df.append({'Date' : date_stamp, 'Unix': unix_time , 'Ticker' : ticker , 'DE Ratio' :value ,}, ignore_index = True)
                except Exception as e:
                    pass
                
                save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/','')+('.csv')
                # print(save)
                df.to_csv(save)


Key_Stats()

