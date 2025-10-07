# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   stockLookup.py
-       This script looks up the closing price for a stock 
-       that the user supplies by calling yfinance. The user
-       enters a stock ticker, then supplies the number of days
-       to look stock data for.  The script then uses matplotlib 
-       to plot the data within a tkinter window. 
-
-   Required Packages (required in imported Modules):
-       yfinance: 0.2.65
-       matplotlib: 3.8.0
-       numpy: 1.26.4
-       pandas: 2.1.2
-       tkinter: built-in
-       datetime: built-in
-
-   Required Modules:
-       getCompanyData.py
-
-   Methods:
-       main()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Oct 2025
--------------------------------------------------------------
'''
import stockLookupModules.getCompanyData as getCompanyData

# main()
def main():
    # Get Stock Data and plot it
    getCompanyData.fetch_and_plot_data()

if __name__ == "__main__":
    main()
