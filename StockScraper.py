from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import os
import csv
import itertools
import datetime
from multiprocessing import Pool

currDir = os.getcwd()
StockPath = currDir + '\\DailyStockData\\'

#Returns a dataframe of the stock data of the given stock ticker list
def getSnapShot(tickerList):
    url = 'http://finance.yahoo.com/d/quotes.csv?s='
    for ticker in tickerList:
        url = url + str(ticker)
        if (str(ticker) != str(tickerList.iloc[-1])):
            url = url + '+'
    url = url + "&f=pabva5b6"
    resp = requests.get(url).text
    snapshot = pd.DataFrame(columns =['Price', 'Ask', 'Bid', 'Volume', 'Ask Volume', 'Bid Volume'])
    for line, ticker in zip(resp.split('\n'), tickerList):
            stats = line.split(',')
            tempFrame = pd.DataFrame(data=np.array(stats).reshape(1,-1), columns =['Price', 'Ask', 'Bid', 'Volume', 'Ask Volume', 'Bid Volume'], index=[str(ticker)])
            snapshot=snapshot.append(tempFrame) 
    return snapshot

#Load Stock List Directory
def loadTickerDirectory():
    dirList = pd.read_csv(StockPath + 'directory.csv', header=0, index_col=0)
    return dirList

def addTickers(tickerList):
    dirList = loadTickerDirectory()
    dirList = dirList.append(pd.DataFrame(tickerList), ignore_index=True)
    dirList = dirList.drop_duplicates()
    dirList.to_csv(StockPath + 'directory.csv')
    return 0

#using the directories stock list, saves a CSV of the stock data at that point in time
def takeSnapShot():
    time = datetime.datetime.now()

    snapshot = getSnapShot(loadTickerDirectory()['Ticker'])
    
    snapshot.to_csv(StockPath + str(time.date()) + '_'
                    + str(time.hour) + '-'
                    + str(time.minute) + '-'
                    + str(time.second) + '.csv')
    return snapshot
