from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import csv

currDir = os.getcwd()
ETFPath = currDir + '\\ETFData\\'

#Given a pre-defined iShares ETF, this function returns a dataframe of the ETF holdings
def getiSharesHoldings(name,url):
    #Get CSV Link
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    link = soup.find('a', string='Detailed Holdings and Analytics', href=True)
    url = url+link['href']
    
    #Download CSV of holdings
    s=requests.get(url).text
    c=pd.read_csv(StringIO(s),skiprows=range(0,10))
    output = pd.concat([c['Ticker'], c['Weight (%)'],c['Asset Class']], axis=1)
    output.name=name

    #return ETF data
    return output

#Load ETF Holding Data
def loadETFHolding(name):
    importData = dirList = pd.read_csv(ETFPath + name + '.csv', header=0, index_col=0,encoding = "ISO-8859-1")
    return importData

#Load ETF Directory
def loadETFDirectory():
    dirList = pd.read_csv(ETFPath + 'directory.csv', header=0, index_col=0)
    return dirList

#Write to directory but make sure there are no duplicates
def writeETFDirectory(dirList):
    dirList=dirList.drop_duplicates()
    dirList.to_csv(ETFPath + 'directory.csv')
    return 0

def addETFHolding(name, url):
    #Try to get ETF Data first in case there is an error
    ETFData=getiSharesHoldings(name,url)
    
    #Update ETF Directory File
    dirList = loadETFDirectory()
    temp = pd.DataFrame(columns=['Names', 'URL'])
    temp.loc[0]=[name,url]
    dirList = dirList.append(temp, ignore_index=True)
    writeETFDirectory(dirList)

    #update EFT File
    ETFData.to_csv(ETFPath + name +'.csv')
    return 0

def getAllStockTickers():
    #create ticker list
    tickerFrame = pd.DataFrame(columns=['Ticker'])
    
    #load ETF Directory File
    dirList = pd.read_csv(ETFPath + 'directory.csv', header=0,index_col=0)
    print(dirList)
    
    #loop through ETF database and add to running list of ALL tickers
    for index, iRow in dirList.iterrows():
        tempTickers = loadETFHolding(iRow['Names'])
        tickerFrame = tickerFrame.append(tempTickers)
    #remove duplicates
    tickerFrame = tickerFrame.drop_duplicates()
    
    #return list of unique tickers
    return pd.DataFrame((tickerFrame[tickerFrame['Asset Class'] == 'Equity'])['Ticker']).reset_index(drop=True)

#update ETF Holdings
def updateETFHoldings():
    #load directory
    dirList = loadETFDirectory()
    
    #get values from online & resave
    for index, iRow in dirList.iterrows():
        ETFData=getiSharesHoldings(iRow['Names'],iRow['URL'])
        ETFData.to_csv(ETFPath + iRow['Names'] +'.csv')
    return 0

