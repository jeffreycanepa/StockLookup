# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   displayData.py
-       This module creates a window using tkinter.
-       Matplotlib is then used to plot data within the 
-       tkinter window. Tkinter is also used to ask the 
-       user for a stock ticker and the number of days for
-       which to looking up data for. Though this module does
-       not use yfinance, it is used by module getCompanyData
-       and is therefore listed as a requirement.
-
-   Required Packages (required in imported Modules):
-       yfinance: 0.2.31
-       tkinter: Tcl/Tk 8.6
-       matplotlib: 3.8.0
-       pandas: 2.1.1
-       numpy: 1.25.2
-
-   Required Modules:
-       numDays.py
-       getCompanyData.py
-
-   Methods:
-       plot_data()
-       set_winsize()
-       plot_window()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Oct 2025
--------------------------------------------------------------
'''
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
import numpy as np
from tkinter import *
import stockLookupModules.getCompanyData as getCompanyData
import stockLookupModules.numDays as numDays

# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-   object containing the stock data
#   ticker-    The stock ticker
#   window-    The tkinter window to plot the data to
#  
# Returns:
#
def plot_data(window):
    # Pull in data from getCompanyData and NumDays modules
    company_name = getCompanyData.company_name
    company = getCompanyData.stockData
    dates = numDays.dates

    # Set myDates to the index of the data
    myDates = company.index

    # convert the datetime index to ordinal values, which can be used to plot a regression line
    company.index.map(pd.Timestamp.toordinal)

    # Create a plot and add Closing price for stock
    fig, ax = plt.subplots(figsize=(8,7))
    ax.plot(company['Close'], color='blue', label=company_name)

    # Set plot title
    ax.set_title('{0} Closing Prices: {1} - {2}'.format(company_name, dates[4], dates[5]), size='large', color='black')

    # Set myDates values to numeric value for use in regression line
    myDates = mdates.date2num(myDates)
    
    # Plot the regression line for Company
    coefficients_close = np.polyfit(myDates, company['Close'], 1)
    p_close = np.poly1d(coefficients_close)
    ax.plot(myDates, p_close(myDates), linestyle='--', color='black')
   
    # Configure tick parameters
    ax.tick_params(axis='x', labelrotation=45)
    ax.tick_params(axis='both', labelsize=7)

    # Set label and title with font sizes
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price ($ USD)', fontsize=12)
    ax.legend()
    ax.grid(True)

    # Format x-axis labels as dates using mm-dd-yy format
    date_form = mdates.DateFormatter("%m-%d-%Y")
    ax.xaxis.set_major_formatter(date_form)
    fig.autofmt_xdate()
    
    # Create canvas and add it to Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# set_winsize()- Set the location/size of the window 
#
# Requires:
#   cwindow- The window object
#
# Returns:
#   string of the window dimensions to use.
#
def set_winsize(cwindow):
    winWidth = 800
    winHeight = 780
    x = (cwindow.winfo_screenwidth() / 2) - (winWidth / 2)
    winGeometry = f'{winWidth}x{winHeight}+{int(x)}+{80}'
    return winGeometry

# plot_window()- A tk window for displaying the data plot from plot_data().  Quiting dialog
#               quits the app.
#
# Required:
#   company_data- The object returned by yfinance that contains the stock data
#   ticker-       The stock ticker used to do the lookup
#
# Returns:
#
def plot_window():
    # Create the window
    plotWindow = Tk()
    plotWindow.title(getCompanyData.company_name +  ' Closing Prices')
    
    # size the window
    plotWindow.geometry(set_winsize(plotWindow))

    # Quit window/app if user closes dialog using the window's close widget
    def on_closing():
        plotWindow.destroy()

    # Quit window/app if user uses the Return key
    def on_return(event):
        plotWindow.destroy()
        getCompanyData.fetch_and_plot_data()

    plotWindow.protocol('WM_DELETE_WINDOW', on_closing)

    # lock the window size
    plotWindow.resizable(False, False)

    # Using Matplotlib display company stock data
    plot_data(plotWindow)

    # Add a button to ask for a new stock symbol
    bt_1 = Button(plotWindow, text='Enter New Ticker')
    bt_1.bind('<Return>', on_return)
    bt_1.bind('<Button-1>', on_return)
    bt_1.focus()
    bt_1.pack()

    plotWindow.mainloop() 