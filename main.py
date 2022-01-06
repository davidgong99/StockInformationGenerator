import AppConfig
from GoogleSheets import GoogleSheets
    
    
def generateStockInfo(gs):

    # Retrieve list of tickers
    tickers = gs.readRange(rangeName="A1:A5")
    
    return ""
    


def main():
    print('as')
    AppConfig.init()
    gs = GoogleSheets()
    
    generateStockInfo(gs)
    
if __name__=='__main__':
    main()