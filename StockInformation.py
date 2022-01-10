import threading

import AppConfig
from GoogleSheets import GoogleSheets
from YahooFinance import YahooFinance
    

class StockInformation():
    def __init__(self):
        self.x = 1
        self.gs = GoogleSheets()
        self.yf = YahooFinance()
        self.config = AppConfig.config
        
    def generateStockInfoMultithread(self):
    
        tickerCount = self.config["tickerCount"]
        threadLimit = self.config["threadLimit"]
        
        nextRow = 1 # tracks which rows we should process next
    
        while nextRow <= tickerCount: # Iterate until tickerCount row is processed
            # Retrieve list of tickers
            tickersList = self.gs.readRange(rangeName=f"A{nextRow}:A{nextRow + threadLimit - 1}")
            
            threads = list()
            # rowCounter = 1
            
            # create new thread for each ticker
            for tickerArr in tickersList:
                ticker = tickerArr[0] # Extract ticker from list of form ['CBA.AX']
                try:
                    # Create thread
                    yahooThread = threading.Thread(target=self.writeStockInfoThread, kwargs={'ticker': ticker, 'rowNum': nextRow})
                    threads.append(yahooThread)
                    yahooThread.start()
                except Exception as e:
                    print(e)
                    
                
                # Increment row counter
                nextRow += 1
            
            # Wait forall threads to finish, then close them
            for thread in threads:
                thread.join()
            # return
        
        return
        
        '''
        # Retrieve list of tickers
        tickersList = self.gs.readRange(rangeName=f"A1:A{tickerCount}")
        
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
        
        '''
    def writeStockInfoThread(self, ticker, rowNum, retryAttempt=0):
        print(f"Thread started: writeInfo({ticker}, {rowNum})")
        
        try:

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
        except Exception as e:
            print(e)
            
            if retryAttempt < 3:
            
                print(f"Retrying: writeInfo({ticker}, {rowNum})")
                return self.writeStockInfoThread(ticker, rowNum, retryAttempt + 1)
            else:
                print(f"Thread failed (0): writeInfo({ticker}, {rowNum})")
                return 0
            
        print(f"Thread ended (1): writeInfo({ticker}, {rowNum})")
        return 1
        
    def getColumns(self):
        return self.config["dataColumns"]