# StockInformationGenerator

This program will help retrieve stock information for a list of stocks inside a spreadsheet

Input format
* Column of stock symbols (following Yahoo Finance convention - e.g. CBA.AX)

Output
* Populated columns for each piece of information from Yahoo Finance's statistics page

# TODO

1. Update multithreading workflow - 
    * Threads should be used to READ from yahoofinance, and append the data to an external list
    * After the threads finish excuting, there should be a batch update to google sheets
    * Current workflow: Each thread READS from yahoofinance and WRITES to google sheets individually -> seg fault
    * httplib used by googleapiclient is not thread-safe [source](https://googleapis.github.io/google-api-python-client/docs/thread_safety.html)
2. Add option to start from certain row