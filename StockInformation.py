import threading

import AppConfig
from GoogleSheets import GoogleSheets
from YahooFinance import YahooFinance
    

class StockInformation():
    def __init__(self):
        self.x = 1
        self.gs = GoogleSheets()
        self.yf = YahooFinance()
        
    def generateStockInfoMultithread(self):
        # Retrieve list of tickers
        tickersList = self.gs.readRange(rangeName="A1:A5")
        
        threads = list()
        rowCounter = 1
        
        # create new thread for each ticker
        for tickerArr in tickersList:
            ticker = tickerArr[0] # Extract ticker from list of form ['CBA.AX']
            try:
                # Create thread
                yahooThread = threading.Thread(target=self.writeStockInfoThread, kwargs={'ticker': ticker, 'rowNum': rowCounter})
                threads.append(yahooThread)
                yahooThread.start()
            except Exception as e:
                print(e)
                
            
            # Increment row counter
            rowCounter += 1
        
        # Wait forall threads to finish, then close them
        for thread in threads:
            thread.join()
        return
        
    
    def writeStockInfoThread(self, ticker, rowNum):
        print(f"Thread started: writeInfo({ticker}, {rowNum})")
        
        if ticker == "Ticker":
            self.gs.writeStockInfo(self.getColumns(), rowNum)
            return 1
        
        # Retrieve all data from Yahoo Finance
        tickerData = self.yf.getTickerData(ticker)
        
        # Extract relevant information
        rowData = []
        for columnName in self.getColumns():
            try:
                rowData.append(tickerData.info[columnName])
            except Exception as e:
                print(e)
                rowData.append("")
                
        # Write to spreadsheet
        self.gs.writeStockInfo(rowData, rowNum)
        print(f"Thread ended (1): writeInfo({ticker}, {rowNum})")
        return 1
        
    def getColumns(self):
        return AppConfig.config["dataColumns"]