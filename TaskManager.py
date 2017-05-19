import ETFScraper
import StockScraper
import datetime

stockUpdateTimer = datetime.datetime.now()
stockUpdateDelay = 60 #seconds
ETFUpdateTimer = datetime.datetime.now()
ETFUpdateDelay = 1 #days
heartBeatTimer = datetime.datetime.now()
heartBeatDelay = 20 #seconds


while(True):
    now = datetime.datetime.now()
    if((stockUpdateDelay <= (now - stockUpdateTimer).seconds) and (now.hour > 4) and (now.hour < 18)):
        StockScraper.takeSnapShot()
        stockUpdateTimer = now
        print("Stock Snapshot Taken!")

    if((ETFUpdateDelay <= (now - ETFUpdateTimer).days)):
        ETFScraper.updateETFHoldings()
        StockScraper.addTickers(ETFScraper.getAllStockTickers()['Ticker'])
        ETFUpdateTimer = now
        print("Updated ETFs and Stocks Directory")

    if(heartBeatDelay <= (now - heartBeatTimer).seconds):
        heartBeatTimer = now
        print("Running Stock Recorder!")



    
