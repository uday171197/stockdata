from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
# import pandas_ta as pta
# from get_all_tickers import get_tickers as gt
import requests
from tqdm import tqdm

# Commodity Channel Index 
def CCI(df, ndays): 
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3 
    df['sma'] = df['TP'].rolling(ndays).mean()
    df['mad'] = df['TP'].rolling(ndays).apply(lambda x: pd.Series(x).mad())
    df['CCI'] = (df['TP'] - df['sma']) / (0.015 * df['mad']) 
    return df

# Ease of Movement 
def EVM(data, ndays): 
     dm = ((data['High'] + data['Low'])/2) - ((data['High'].shift(1) + data['Low'].shift(1))/2)
     br = (data['Volume'] / 100000000) / ((data['High'] - data['Low']))
     EVM = dm / br 
     EVM_MA = pd.Series(EVM.rolling(ndays).mean(), name = 'EVM') 
     data = data.join(EVM_MA) 
     return data 
 
    
# Simple Moving Average 
def SMA(data, ndays): 
     SMA = pd.Series(data['Close'].rolling(ndays).mean(), name = 'SMA') 
     data = data.join(SMA) 
     return data

# Exponentially-weighted Moving Average 
def EWMA(data, ndays): 
     EMA = pd.Series(data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean(), 
                     name = 'EWMA_' + str(ndays)) 
     data = data.join(EMA) 
     return data

# Rate of Change (ROC)
def ROC(data,n):
     N = data['Close'].diff(n)
     D = data['Close'].shift(n)
     ROC = pd.Series(N/D,name='Rate of Change')
     data = data.join(ROC)
     return data
 
# Compute the Bollinger Bands 
def BBANDS(data, window=50):
    MA = data.Close.rolling(window=window).mean()
    SD = data.Close.rolling(window=window).std()
    data['UpperBB'] = MA + (2 * SD) 
    data['LowerBB'] = MA - (2 * SD)
    return data

# Force Index 
def ForceIndex(data, ndays): 
    FI = pd.Series(data['Close'].diff(ndays) * data['Volume'], name = 'ForceIndex') 
    data = data.join(FI) 
    return data

def fetch_stock_data(symble,start_date,end_date,interval):
    data = yf.download(tickers=symble, start=start_date, end=end_date, interval=interval)
    
    # data = pdr.get_data_yahoo("GOOGL", start="1999-01-01", end="2021-07-26",interval='m') 
    # data = pd.DataFrame(data)
    # data['interval'] = interval
    return data
 
def calculate_technical_values(daily_data):
    daily_data = CCI(daily_data, 14) 
    # Compute the 14-day Ease of Movement for AAPL
    n = 14
    daily_data = EVM(daily_data, n)
    
    # Compute the 50-day SMA for NIFTY
    n = 50
    daily_data = SMA(daily_data,n)
    # Compute the 200-day EWMA for NIFTY
    ew = 200
    daily_data = EWMA(daily_data,ew)
    # Compute the 5-period Rate of Change for NIFTY
    n = 5
    daily_data = ROC(daily_data,n)
    # Compute the Bollinger Bands for NIFTY using the 50-day Moving average
    n = 50
    daily_data = BBANDS(daily_data, n)
    # Compute the Force Index for AAPL
    n = 1
    daily_data = ForceIndex(daily_data,n)
    return daily_data




def fetch_daily_data(tickers,today_date,main_data):
    for company in tqdm(tickers[:10]):
        today_date = str(datetime.today()).split()[0]
        daily_data = fetch_stock_data(company,"2009-01-01",today_date,'1d')
        daily_data = calculate_technical_values(daily_data)
        # main_data = main_data.append(daily_data,ignore_index = False)
        daily_data = daily_data.dropna(axis=0)
        daily_data = daily_data.reset_index()
        daily_data = daily_data[daily_data['Date'] > "2010-01-01"]
        daily_data.to_excel('../res/data/{}.xlsx'.format(company))
    return main_data


def fetch_weekly_data(tickers,today_date,main_data):
    for company in tqdm(tickers['symbol'][:10]):
        weakly_data = fetch_stock_data(company,"2009-01-01",today_date,'1wk')
        # Compute the Commodity Channel Index (CCI) for NIFTY based on the 14-day moving average
        weakly_data = calculate_technical_values(weakly_data)
        main_data = main_data.append(weakly_data,ignore_index = False)
        
    return main_data
        
        
def fetch_monthly_data(tickers,today_date,main_data):
    for company in tqdm(tickers['symbol'][:10]):
        monthly_data = fetch_stock_data(company,"2009-01-01",today_date,'1mo')
        # Compute the Commodity Channel Index (CCI) for NIFTY based on the 14-day moving average
        monthly_data = calculate_technical_values(monthly_data)
        main_data = main_data.append(monthly_data,ignore_index = False)
    return main_data
    
        
def fetch_3monthly_data(tickers,today_date,main_data):
    for company in tqdm(tickers['symbol'][:10]):
        monthly_data = fetch_stock_data(company,"2009-01-01",today_date,'3mo')
        # Compute the Commodity Channel Index (CCI) for NIFTY based on the 14-day moving average
        monthly_data = calculate_technical_values(monthly_data)
        main_data = main_data.append(monthly_data,ignore_index = False)
    return main_data
        
 
today_date = str(datetime.today()).split()[0]   
tickers = pd.read_excel('../res/nasdaq_all_tickers.xlsx')
tickers.columns
main_data= pd.DataFrame()
filter_tickers = tickers[tickers['volume'] >200757]['symbol'].reset_index(drop=True)
daily_data = fetch_daily_data(filter_tickers,today_date,main_data)
daily_data = daily_data.dropna(axis=0)
     







    
