# Get data from : http://pythonprogramming.net/static/downloads/machine-learning-data/intraQuarter.zip
import pandas as pd
import os
import time
import matplotlib
import matplotlib.pyplot as plt
import re

from datetime import datetime
from time import mktime
from matplotlib import style


style.use('dark_background')

# Mac path
# path = '/Users/mohammedjalil/github/ml-invest/data/intraQuarter'

# Linux Path
path = '/home/mo/github/ml-invest/data/intraQuarter'

def Key_Stats(gather='Total Debt/Equity (mrq)'):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date', 
                                 'Unix', 
                                 'Ticker', 
                                 'DE Ratio', 
                                 'Price', 
                                 'stock_p_shange', 
                                 'SP500', 
                                 'sp500_p_change',
                                 'Difference'])

    sp500_df = pd.DataFrame.from_csv('data/yahoo-s&p/^GSPC.csv')
    ticker_list = []

    #every time the stock changes we wont be able to do a percentage difference
    starting_stock_value = False
    starting_sp500_value = False

    for each_dir in stock_list[1:100]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("KeyStats/")[1]
        ticker_list.append(ticker)
        #make sure to skip folders with no files in them
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                full_file_path = each_dir + '/' + file
                source = open(full_file_path, 'r').read()
                try:
                    #fill in some missing data
                    try:
                        value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except Exception as e:
                        value = float(source.split(gather + ':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])                        
                        # print(str(e), ticker, file)
                        #time.sleep(15)
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row['Adj Close'])
                    except Exception as e:
                        # If on the weekend we go back 3 days (259200) so we get data from the weekday
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row['Adj Close'])
                    

                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:

                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            
                            print(stock_price)
                        except Exception as e:                    
                            stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            
                            # print('Latest: ', stock_price)
                            # print(str(e), ticker, file)
                        # time.sleep(15)

                        # print(str(e), ticker, file)
                        #time.sleep(15)


                    # Here we have enough information to calculate the percentage change
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    df = df.append({'Date' : date_stamp, 
                                    'Unix': unix_time , 
                                    'Ticker' : ticker , 
                                    'DE Ratio' :value ,
                                    'Price' :stock_price,
                                    'stock_p_change': stock_p_change,
                                    'SP500': sp500_value,
                                    'sp500_p_change': sp500_p_change ,
                                    'Difference' : stock_p_change - sp500_p_change}, ignore_index = True)
                except Exception as e:
                    pass
                

    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])
            plot_df['Difference'].plot(label=each_ticker)
            plt.legend()

        except:
            pass
    
    plt.show()
    save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/','')+('.csv')
    # print(save)
    df.to_csv(save)


Key_Stats()

