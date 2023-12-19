# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   getCompanyData.py
-       This module gets stock data using yfinance.  It also
-       gets the company name for the stock ticker provided
-       It then calls all the methods needed to get the stock
-       ticker, get the start/end dates and display the data.
-       
-
-   Required Packages (required in imported Modules):
-       yfinance: 0.2.31
-       requests: 2.31.0
-       re: built-in
-
-   Required Modules:
-       numDays.py
-       getTicker.py
-       displayData_ctk.py
-
-   Methods:
-       get_stock_data()
-       get_company_name()
-       fetch_and_plot_data()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Dec 2023
--------------------------------------------------------------
'''
import yfinance as yf
import plotStockModules.numDays as numDays
import plotStockModules.getTicker as getTicker
import plotStockModules.displayData as displayData

# get_data()- Using yfinance, get stock data for provided stock ticker.
# Requires: 
#   item- the stock ticker to fetch data for 
#
# Returns:
#   stockData- object containing stock data for past year for the provided symbol
#
def get_stock_data():
    global company_name
    global stockData
    item = getTicker.ticker
    # Pseudo status
    print('Fetching data for', item, '...')
    stockData = yf.download(tickers = item,
                         start= numDays.dates[2],
                         end= numDays.dates[3])
    cmp = yf.Ticker(item)
    try:
        # company_name = cmp.info['longName']

        # yfinance info seems to be flakey, so get company name by other means
        company_name = get_company_name(item)
    except:
        company_name = item
    return stockData

# get_company_name()- Get company name using it's stock ticker
# Requires: 
#   ticker- the stock ticker to fetch data for 
#
# Returns:
#   result- The name of the company
#
def get_company_name(ticker):
    import requests, re

    url = 'https://finance.yahoo.com/quote/WMT/'
    url = url.replace("WMT",ticker)

    req = requests.get(url)
    html = req.text

    name = re.search(r'\<title>([^\s]+)\ ([^\s]+)', html)
    result = str(name.group(0))
    result = result.replace("<title>", "")
    return result

def fetch_and_plot_data():
    global numdays
    global dates
    # Get the Ticker symbol
    getTicker.getTicker()
    # Get number of days to look up
    numDays.get_num_days()  
    # Get start/end dates based on numer of days
    numDays.get_dates()
    # Grab the data from yfinance
    get_stock_data()
    # Create window to display data in, plot the data, then display the data
    displayData.plot_window()