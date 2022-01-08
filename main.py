import threading

import AppConfig
from GoogleSheets import GoogleSheets
from YahooFinance import YahooFinance
    
# def generateStockInfo():

#     # Retrieve list of tickers
#     tickersList = gs.readRange(rangeName="A1:A5")
    
#     spreadsheetData = yf.generateSpreadsheetDataDict(tickersList)
    
#     print(spreadsheetData)
    
#     tickerRow = 1
#     for tickerArr in tickersList:
#         ticker = tickerArr[0]
        
#         gs.writeStockInfo(spreadsheetData[ticker], tickerRow)
        
#         tickerRow += 1
        
    
#     return ""
    
def generateStockInfoMultithread():
    
    # Retrieve list of tickers
    tickersList = gs.readRange(rangeName="A1:A5")
    
    threads = list()
    rowCounter = 1
    
    # create new thread for each ticker
    for tickerArr in tickersList:
        ticker = tickerArr[0] # Extract ticker from list of form ['CBA.AX']
        
        # Create thread
        yahooThread = threading.Thread(target=writeStockInfoThread, kwargs={'ticker': ticker, 'rowNum': rowCounter})
        threads.append(yahooThread)
        yahooThread.start()
        
        # Increment row counter
        rowCounter += 1
    
    # Wait forall threads to finish, then close them
    for thread in threads:
        thread.join()
    return

def writeStockInfoThread(ticker, rowNum):
    print(f"Thread started: writeInfo({ticker}, {rowNum})")
    
    if ticker == "Ticker":
        gs.writeStockInfo(getColumns(), rowNum)
        return 1
    
    # Retrieve all data from Yahoo Finance
    tickerData = yf.getTickerData(ticker)
    
    # Extract relevant information
    rowData = []
    for columnName in getColumns():
        try:
            rowData.append(tickerData.info[columnName])
        except Exception as e:
            print(e)
            rowData.append("")
            
    # Write to spreadsheet
    gs.writeStockInfo(rowData, rowNum)
    print(f"Thread ended (1): writeInfo({ticker}, {rowNum})")
    return 1
    
def getColumns():
    return ["sector","revenueGrowth","recommendationKey"]

def main():
    AppConfig.init()
    
    # Initialise Google Sheets handler
    global gs
    gs = GoogleSheets()
    
    # Initialise YahooFinance handler
    global yf
    yf = YahooFinance()
    
    
    generateStockInfoMultithread()
    
if __name__=='__main__':
    main()