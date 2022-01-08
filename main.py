
import AppConfig
from StockInformation import StockInformation

def main():
    AppConfig.init()
    
    # # Initialise Google Sheets handler
    # global gs
    # gs = GoogleSheets()
    
    # # Initialise YahooFinance handler
    # global yf
    # yf = YahooFinance()
    
    
    si = StockInformation()
    
    si.generateStockInfoMultithread()
    
if __name__=='__main__':
    main()