automated_stock_data_downloads
=============================

##Installation

To install the `automated_stock_data_downloads` module onto your computer, go into
your desired folder of choice (say `Downloads`), and:

1. Clone the repository

	    $ cd ~/Downloads
	    $ git clone https://github.com/robertdavidwest/automated_stock_data_downloads

2. `cd` into the `automated_stock_data_downloads` directory

        $ cd automated_stock_data_downloads

3. Install the package

        $python setup.py install

4. Check your install.  From anywhere on your machine, be able to open
   `iPython` and import the library, for example:

	    $ cd ~/
	    $ ipython

        IPython 1.1.0 -- An enhanced Interactive Python.
        ?         -> Introduction and overview of IPython's features.
        %quickref -> Quick reference.
        help      -> Python's own help system.
        object?   -> Details about 'object', use 'object??' for extra details.
	
        In [1]: import get_stock_data


##Documentation 

The module 'get_stock_data' contains three functions: `adj_close()`, `sp500_tickers()` and 
`russell3000_tickers()`.

* `adjclose()`

		def adj_close(interface_filename='get_stocks_for_tsr.xlsx', assumptions_first_row=4, ticker_first_row=8, assumptions_columns='B:C', ticker_columns='C'):
	

	Given a Vaulation Date, Lookback Period and a list of tickers, this function will output a matrix of adjusted daily close stock 
price data for each ticker provided, as well as the annualised volatility of the log returns of each ticker. 

	All user inputs are entered via the interface file
	
		default interface_filename:	 get_stock_data.xlsx
		sheet name:	Assumptions
		
			|	A	|			B				|		C			|
		--------------------------------------------------------------------------
		1	|		|							|					|
		2	|		|							|					|
		3	|		|							|					|
		4	|		|	Valuation Date	 		|	MM/DD/YYYY	|
		5	|		|	Lookback Period (years)	|	3				|
		6	|		|							|					|
		7	|		|							|	Tickers			|
													----------------
		8	|		|						1	|	A				|
		9	|		|						2	|	AA				|
		10	|		|						3	|	AAPL			|		
		:									:		:
		

				
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

		1. 	Adj Close data: 	Adjusted close daily stock price data over the 
					specified period for all tickers
		2. 	Volatility:		The volatility of every ticker
		3.	No Data: 		A list of tickers that do not have any stock price 
					history over specified period 

		.. warning:: Requires Internet Connectivity

		Because the function calls the `Yahoo! API <http://www.finance.yahoo.com>` internet connectivity is required for the function to work


* `sp500_tickers()`
	
		def sp500_tickers():

	
	Obtain all current S&P contituent tickers from wikipedia.
	
	The results will be output into a csv file
	
* `russell3000_tickers()`
	
		def russell3000_tickers():
		
	Obtain all current Russell 3000 contituent tickers from www.marketvolume.com.
	 
	The results will be output into a csv file
