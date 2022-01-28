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
    
        nextRow = self.config["startRow"] # tracks which rows we should process next
        
        tickerCount = nextRow + self.config["tickerCount"]
        threadLimit = self.config["threadLimit"]
        
    
        while nextRow <= tickerCount: # Iterate until tickerCount row is processed
            firstRowInBatch = nextRow
            lastRowInBatch = min(nextRow + threadLimit - 1, tickerCount)
            
            # Retrieve list of tickers
            tickersList = self.gs.readRange(spreadsheetRange=f"!A{nextRow}:A{lastRowInBatch}")
            
            threads = list()
            
            # This buffer ditionary is used to keep row data in order by storing their index as a key
            # The buffer dictionary will then be transformed into a list ordered by key 
            #   to maintain the order of data after multithreading
            # key: index::integer
            # value: rowData::list
            stockDataBuffer = {}
            
            # create new thread for each ticker
            for tickerArr in tickersList:
                ticker = tickerArr[0] # Extract ticker from list of form ['CBA.AX']
                try:
                    # Create thread
                    
                    print(f"Main    : create and start thread for {ticker}")
                    yahooThread = threading.Thread(
                        target=self.appendYahooDataThread, 
                        kwargs={'ticker': ticker, 'rowNum': nextRow, 'dataBuffer': stockDataBuffer}
                    )
                    threads.append(yahooThread)
                    yahooThread.start()
                except Exception as e:
                    print("Exception in generateStockInfoMultithread()")
                    print(e)
                    
                
                # Increment row counter
                nextRow += 1
            
            # Wait forall threads to finish, then close them
            for thread in threads:
                print(f"Main    : before joining thread for {ticker}")
                thread.join()
                print(f"Main    : thread for {ticker} done")
            
            # Convery stockDataBuffer into a list
            stockDataList = []
            
            for i in range(firstRowInBatch, lastRowInBatch + 1):
                try:
                    stockDataList.append(stockDataBuffer[i])
                except Exception as e:
                    print("Exception extracting data from stockDataBuffer")
                    print(e)
            
            self.gs.writeStockInfo(stockDataList, firstRowInBatch)
        return
        
    '''
    This function will retrieve all the stock info from YahooFinance, and append it to an external list
    
    Input
        ticker::string - YahooFinance formatted ticker
        rowNum::integer - To track the current row number
        dataBuffer::dictionary - For outputting stock data from thread
        retryAttempt::integer - To track retry attempt number
    Output
        None::None
    Impact
        Updates dataBuffer::dictionary with the stock data for the current ticker
            Key: rowNum::integer
            Value: rowData::list
    '''
    def appendYahooDataThread(self, ticker, rowNum, dataBuffer, retryAttempt=0):
        print(f"    Thread started: writeInfo({ticker}, {rowNum}, {retryAttempt})")
        
        try:

            if ticker == "Ticker":
                headerRow = []
                for column in self.getColumns():
                    headerRow.append(column.niceName)
                dataBuffer[rowNum] = headerRow
                return 1
            
            # Retrieve all data from Yahoo Finance
            tickerData = self.yf.getTickerData(ticker)
            print(f"     {ticker}: Ticker data retrieved")
            
            # Extract relevant information
            rowData = []
            for column in self.getColumns():
                try:
                    # Check if exists or is None
                    if column.keyName not in tickerData.info or not tickerData.info[column.keyName]:
                        rowData.append("")
                    else:
                        rowData.append(column.format(tickerData.info[column.keyName]))
                        
                        # rowData.append(tickerData.info[columnName])
                except Exception as e:
                    print("Exception getting column name")
                    print(e)
                    rowData.append("")
                    
            # Write to spreadsheet
            # self.gs.writeStockInfo(rowData, rowNum)
            dataBuffer[rowNum] = rowData
            print(f"     {ticker}: Ticker data added to buffer")
        except Exception as e:
            print(f"Exception in writeStockInfoThread({ticker},{rowNum},{retryAttempt})")
            print(e)
            
            
            if retryAttempt < 3:
            
                print(f"Retrying: writeInfo({ticker}, {rowNum})")
                return self.appendYahooDataThread(ticker, rowNum, retryAttempt + 1)
            else:
                print(f"Thread failed (0): writeInfo({ticker}, {rowNum})")
                return 0
            
        print(f"Thread ended (1): writeInfo({ticker}, {rowNum})")
        return 1
        
    def getColumns(self):
        return self.config["dataColumns"]