from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import csv

currDir = os.getcwd()

def getiSharesHoldings(selection):
    if(selection=='iShare_MedDev'):
        url= 'https://www.ishares.com/us/products/239516/ishares-us-medical-devices-etf/1467271812596.ajax?fileType=csv&fileName=IHI_holdings&dataType=fund'
    elif(False):#placeholders
        a=1
    elif(False):
        a=1
    else:
       print("Error in retrieving " + selection + " data")
       return 0
       
    s=requests.get(url).text
    c=pd.read_csv(StringIO(s),skiprows=range(0,10))

    output = pd.concat([c['Ticker'], c['Weight (%)'],c['Asset Class']], axis=1)
    """ For bug checking
    for i,stock in output.iterrows():
        print(stock)
        print('-----------------')
    """
    return output

def findNewAndUpdate(curHeldStocks):
    filename = currDir + '/tickerList.csv'
    oldStocks = pd.read_csv(filename)
    newFrame = oldStocks.append(curHeldStocks)
    

    newStocks = newFrame.drop_duplicates()

 
    newFrame.to_csv(filename)
    return newStocks

def getTickerHistory():

    return 0

def getStockPrices():

    return 0

#Get current ETF holdings
currentHoldings = getiSharesHoldings('iShare_MedDev')

#Get DF Column of Current Stocks (Equities)
currentStocks = currentHoldings[currentHoldings['Asset Class'] == 'Equity']['Ticker']

#Get a list of the new stocks
#newStocks = findNewAndUpdate(currentStocks)

page = requests.get('https://ca.finance.yahoo.com/quote/GOOG?ltr=1')
soup = BeautifulSoup(page.content, 'html.parser')
soup.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')

