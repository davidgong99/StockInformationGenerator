import AppConfig
from GoogleSheets import GoogleSheets
from YahooFinance import YahooFinance
    
def generateStockInfo(gs):

    # Initialise YahooFinance handler
    yf = YahooFinance()

    # Retrieve list of tickers
    tickersList = gs.readRange(rangeName="A1:A5")
    
    spreadsheetData = yf.generateSpreadsheetDataDict(tickersList)
    
    print(spreadsheetData)
    
    tickerRow = 1
    for tickerArr in tickersList:
        ticker = tickerArr[0]
        
        gs.writeStockInfo(spreadsheetData[ticker], tickerRow)
        
        tickerRow += 1
        
    
    return ""
    


def main():
    print('as')
    AppConfig.init()
    gs = GoogleSheets()
    
    generateStockInfo(gs)
    
if __name__=='__main__':
    main()