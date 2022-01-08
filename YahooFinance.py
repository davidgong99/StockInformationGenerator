import requests
import yfinance as yf

class YahooFinance():
    def __init__(self):
        self.x = 1
        
    def _get(self, url):
        try:
            print("Sending GET request to ", url)
            # Send request
            r = requests.get(url)
            # print(r)
            return r
            # res = r.json()
            
        except Exception as e:
            print(e)
            return {}
        
    def getStockInformation(self, ticker):
        url = f"https://finance.yahoo.com/quote/FB/key-statistics?p=FB"
        # url = f"https://finance.yahoo.com/screener/predefined/day_gainers"
        return self._get(url)
        
    def getTickerData(self, ticker):
        return yf.Ticker(ticker)
        
        
    """
    This function generates a dictionary with the raw data to be inputted into the spreadsheet
    
    Input
        tickersList::list::list::string
            e.g. [['Tickers'],['CBA.AX'],['AAPL']]
        
    Output
        spreadsheetData::dictionary
            key: ticker::string
            value: tickerData::list::strings
    """
    def generateSpreadsheetDataDict(self, tickersList):
        spreadsheetData = {"Ticker": self._getColumns()}

        for t in tickersList:
    
            # t is in form ['CBA.AX']
            ticker = t[0]
            
            # Ignore column header "Ticker"
            if ticker == "Ticker":
                continue
                            
            # Retrieve ticker data from YF
            data = self.getTickerData(ticker)
            # print(data.info)
            # print(data.dividends)
            
            # Create output list
            tickerData = []
            
            # Append relevant data to output list
            for columnName in self._getColumns():
                try:
                    tickerData.append(data.info[columnName])
                except Exception as e:
                    print(e)
                    tickerData.append("")
            
            # Insert output data into output dictionary
            spreadsheetData[ticker] = tickerData
        
        return spreadsheetData
            
            
    def _getColumns(self):
        return ["sector","revenueGrowth","recommendationKey"]
            
        
        