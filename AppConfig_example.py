from Column import Column

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
        "dataColumns": [
            Column("shortName", "Short name"),
            Column("sector", "Sector"),
            Column("marketCap","Market Cap","millifyLarge"),
            Column("enterpriseToEbitda","EV/EBITDA"),
            Column("lastDividendValue","Last Dividend Value"),
            Column("trailingAnnualDividendYield","Trailing Annual Dividend Yield", "millifyPercentage"),
            Column("fiveYearAvgDividendYield",  "5Y Avg Dividend Yield"),
            Column("trailingAnnualDividendRate","Trailing Annual Dividend Rate"),
            Column("lastDividendDate",          "Last Dividend Date", "epochToDate"),
            Column("exDividendDate",            "Ex-Dividend Date", "epochToDate"),
            Column("payoutRatio",               "Payout Ratio", "millifyPercentage"),
            Column("lastSplitFactor","Last Split Factor"),
            Column("lastSplitDate","Last Split Date", "epochToDate"),
            Column("recommendationKey","Recommendation Key"),
        ],     
        
        # Starting row to process from
        "startRow": 101,
        
        # Number of total rows of tickers to search for
        "tickerCount": 30,
        
        # Number of threads to create at once
        "threadLimit": 5,
    }