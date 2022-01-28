
def init():
    global config
    config = {
        # Get this from the URL of your spreadsheet
        "spreadsheetID": "1XbFflGI5sn_w4Bxt-rRg-mb-AYFrDfGWS7-qMSJZomY",

        # This is the name of the sheet you want to update
        # Note: This script will OVERRIDE whatever is in that range
        # You can also specify a range like this: "MySheet!A3:M8"
        "spreadsheetName": "Sheet1",
        
        # Column names
        "dataColumns": ["shortName","sector","marketCap","enterpriseToEbitda","lastDividendValue","trailingAnnualDividendYield","fiveYearAvgDividendYield","trailingAnnualDividendRate","lastDividendDate","exDividendDate","payoutRatio","lastSplitFactor","lastSplitDate","recommendationKey"],
        
        # Starting row to process from
        "startRow": 101,
        
        # Number of total rows of tickers to search for
        "tickerCount": 30,
        
        # Number of threads to create at once
        "threadLimit": 5,
    }