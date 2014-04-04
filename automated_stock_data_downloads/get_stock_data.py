#!/usr/bin/env python
# encoding: utf-8
"""
.. module:: get_stock_data.py
    :synopsis: 
.. moduleauthor:: Robert D. West <robet.david.west@gmail.com>
"""

import bs4
import datetime
import fish
import openpyxl
import pandas
import pandas.io.data
import numpy
import time
import urllib2


def adj_close(interface_filename='get_stocks_for_tsr.xlsx', assumptions_first_row=4, ticker_first_row=8, assumptions_columns='B:C', ticker_columns='C'):

    """
    Given a Vaulation Date, Lookback Period and a list of tickers, this function will output a matrix of adjusted daily close stock 
    price data for each ticker provided, as well as the annualised volatility of the log returns of each ticker. 
    
    All user inputs are entered via the interface file
        
        default interface_filename:  get_stock_data.xlsx
        sheet name: Assumptions
        
            |   A   |           B               |       C           |
        --------------------------------------------------------------------------
        1   |       |                           |                   |
        2   |       |                           |                   |
        3   |       |                           |                   |
        4   |       |   Valuation Date          |   MM/DD/YYYY  |
        5   |       |   Lookback Period (years) |   3               |
        6   |       |                           |                   |
        7   |       |                           |   Tickers         |
                                                    ----------------
        8   |       |                       1   |   A               |
        9   |       |                       2   |   AA              |
        10  |       |                       3   |   AAPL            |       
        :                                   :       :
    
    :ARGS:
    
        interface_filename: :meth:`str` The name of the excel interface file. The default name is <get_stock_data.xlsx>
    
        assumptions_first_row :meth: `int` The first row in the excel interface of input data. Do not change from the default 
        value unless the interface file has been modified
        
        ticker_first_row  :meth: `int` The first row in the excel interface of ticker data. Do not change from the default 
        value unless the interface file has been modified
        
         assumptions_columns :meth:`str` A string showing the columns within the excel interface file holding the general
         assumptions. Do not change from the default value unless the interface file has been modified
         
         ticker_columns  :meth:`str` A string showing the column within the excel interface file holding the tickers. Do not
         change from the default value unless the interface file has been modified
    
    :RETURNS:
    
    The function will add 3 new sheets to the existing interface file
    
    1.  Adj Close data:     Adjusted close daily stock price data over the 
                        specified period for all tickers
    2.  Volatility:     The volatility of every ticker
    3.  No Data:        A list of tickers that do not have any stock price 
                        history over specified period 
    
    .. warning:: Requires Internet Connectivity
    
    Because the function calls the `Yahoo! API <http://www.finance.yahoo.com>`_
    internet connectivity is required for the function to work
    """
    
    ############################
    # Show the progress fish to user
    fish.Fish()
    
    ############################
    #read general assumptions from the interfacefile
    assumptions  = pandas.read_excel(interface_filename, 'Assumptions', skiprows = assumptions_first_row - 2, index_col = 0, parse_cols= assumption_columns)
    
    val_date = assumptions.ix['Valuation Date', 0]
    val_date = pandas.Timestamp(val_date) #cast date to Pandas timestamp
    
    lookback_period = assumptions.ix['Lookback Period (years)', 0]
    lookback_date = val_date - datetime.timedelta(days = 365.25 * lookback_period)
    lookback_date = pandas.Timestamp(lookback_date) #cast date to Pandas timestamp for consistency
        
        
    ############################
    #get list of tickers from the interface file
    ticker_data = pandas.read_excel(filename, 'Assumptions', skiprows = ticker_first_row - 2, parse_cols= ticker_columns)
    ticker_data = ticker_data[ticker_data.Tickers.notnull()] # remove rows that do not contain tickers
    
    
    ############################
    # Download adjusted stock price data directly from Yahoo! API   
    stock_dict = {}
    no_data = []
    for ticker in ticker_data.Tickers:
        # make sure the selected ticker has stock data over the specified period, if not display a message and exclude the ticker
        try:
            stock_dict[ticker] = pandas.io.data.DataReader(ticker, "yahoo", lookback_date, val_date)['Adj Close']       
        except IOError:     
            print "Ticker %s has no data between %s and %s" %(ticker, lookback_date, val_date)  
            no_data.append(ticker)
    
    stock_data = pandas.DataFrame(stock_dict)
    no_data = pandas.DataFrame({'Ticker':no_data})
    
    
    ############################
    # Get volatilities 
    log_returns = stock_data.apply(numpy.log).diff() #calculate log returns of daily adjustced close prices
    sigma = log_returns.apply(numpy.std)  * numpy.sqrt(252)
    sigma = pandas.DataFrame({'Volatility':sigma})  


    ##############  
    # Export to excel
    book = openpyxl.load_workbook(interface_filename) # open excel workbook
    
    needed_worksheets = [] # Remove old data from previous runs 
    for sheets in book.worksheets:
        if sheets.title != 'Adj Close data' and sheets.title != 'Volatility' and sheets.title != 'No Data' :
            needed_worksheets.append(sheets)
    book.worksheets = needed_worksheets
    
    writer = pandas.ExcelWriter(interface_filename)  
    writer.book = book # Give ExcelWriter needed worksheets
    
    stock_data.to_excel(writer,'Adj Close data') # add new worksheets with current data
    sigma.to_excel(writer,'Volatility')
    no_data.to_excel(writer,'No Data')
    writer.save()

def sp500_tickers_to_series():
    """
    Obtain all current S&P contituent tickers from wikipedia and return then in a
    :class:`pandas.Series`

    """
    return sp_helper_fun()

def sp500_tickers():
    """ 
    Obtain all current S&P contituent tickers from wikipedia.
    
    The results will be output into a csv file
    """
    tickers = sp_helper_fun()
    ## Get current date in dd/mm/yyyy format
    date = time.strftime("%m_%d_%Y")
    
    ## Export tickers to CSV file and date stamp the file
    tickers.to_csv('sp500_tickers_'+ date+'.csv', index = False)
    return None

def sp_helper_fun():
    """
    Reuse the beautifully constructed core functionality in a helper
    function for the other sp500 functions to allow an output to a
    ``.csv`` or to a :class:`pandas.Series`
    """
    ############################
    # Show the progress fish to user
    fish.Fish()
    
    url = 'http://en.wikipedia.org/wiki/List_of_S&P_500_companies'
    soup = bs4.BeautifulSoup(urllib2.urlopen(url))
     
    #currently, all the data is stored in <table class="wikitable sortable">
    table = soup.find('table', {'class':'wikitable sortable'})
    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text.encode('utf8') for val in row.find_all('td')])
    
    dataTable = pandas.DataFrame(rows)
    tickers = dataTable[0]
    return tickers

def russell3000_tickers_to_series():
    """
    Obtain all current Russell 3000 contituent tickers from www.marketvolume.com
    and output into a :class:`pandas.Series`
    """
    return russell3000_helper_fun()

def russell3000_tickers():
    """
    Obtain all current Russell 3000 contituent tickers from www.marketvolume.com.
     
    The results will be output into a csv file
    """
    ## Get current date in dd/mm/yyyy format
    date  = time.strftime("%m_%d_%Y")
    tickers = russell3000_helper_fun()
    tickers.to_csv('russell3000_tickers_'+ date+'.csv', index = False)
    
def russell3000_helper_fun():
    """
    Reuse the beautifully constructed core functionality in a helper
    function for the other russell3000 functions to allow an output to a
    ``.csv`` or to a :class:`pandas.Series`

    """
    tickers_per_page = 250
    num_pages = 12
    url_start = 'http://www.marketvolume.com/indexes_exchanges/r3000_components.asp?s=RUA&row='
    url_num_refs = [tickers_per_page*x for x in range(0,num_pages)]
     
    allData = pandas.DataFrame()
    for url_num in url_num_refs:
        print url_num
        
        soup = bs4.BeautifulSoup(urllib2.urlopen(url_start + str(url_num)))
         
        #currently, all the data is stored in <table id="mkt">
        table = soup.find('table', {'id': 'mkt'})
        rows = []
        
        for row in table.find_all('tr'):
            rows.append([val.text.encode('utf8') for val in row.find_all('td')])
        
        dataTable = pandas.DataFrame(rows)
        dataTable = pandas.DataFrame({'Symbol': dataTable[0]})
        
        allData = allData.append(dataTable, ignore_index=True)
            
    allData = allData[allData.Symbol != 'Symbol'] #remove header rows that are read in as tickers
    
    # Remove duplicate tickers (there may be some crossover between the urls)
    allData = allData.drop_duplicates(cols='Symbol', take_last=True)
    allData = allData.sort('Symbol')
    
    ## Export tickers to CSV file and date stamp the file
    tickers = allData.Symbol
    return tickers
