import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials
import time
import datetime
pd.set_option('display.max_columns',50)
pd.options.display.float_format = '{:,.2f}'.format

def in_dict(dict, key):
	"""
	Checks if key exists in dict, if so return corresponding valu
	Args:
		dict (Dictionary): The dictionary that we are checking.
		key (Dictionary Element): The element we are looking for in the dictionary.
	Returns:
		A value if key is in dict, else None.
	"""
	if(key in dict):
		return dict[key]
	else:
		return None

def format_float(value):
	"""
	Returns value formatted as float?
	Args:
		value (int): An integer that will be formatted.
	Returns:
		Formatted version of value as float.
	"""
	return f'{value:,.2f}'

def get_stats(financials, tickers):
	"""
	Calls .get_key_statistics_data on yfapi and retrieves corresponding metrics.
	Args:
		financials (YahooFinancials): Yahoo financials api object.
		tickers (List[Strings]): A list of strings containing company ticker names.
	Returns:
		data (DataFrame): The resulting metric data as pandas DataFrame.
	"""
	company_key_statistics_data = financials.get_key_statistics_data() #includes profit margins, forward eps, yearly change etc.
	samples = []
	for key in company_key_statistics_data.keys():
		company_key_statistics_data[key]["Company"] = key
		samples.append(list(company_key_statistics_data[key].values()))
	data = pd.DataFrame(samples, columns = company_key_statistics_data[tickers[0]].keys())
	return data

def get_sheet(financials, tickers, period, sheetType):
	"""
	Calls .get_financial_stmts on yfapi and retrieves corresponding financial sheet data.
	Args:
		financials (YahooFinancials): Yahoo financials api object.
		tickers (List[Strings]): A list of strings containing company ticker names.
		period (String): Represents frequency of financial statement data; quarterly, annually, ect.
		sheetType (String): The time of sheet to  fetch from yfapi; balance sheet, cash sheet, income sheet, ect.
	Returns:
		df (DataFrame): The data of the sheet in the form of a DataFrame.
		company_balance_sheet_data_qt[title] (Dictionary): The raw data in the form of a dictionary.
	"""

	title = ''
	if(sheetType == 'balance'):
		title = 'balanceSheetHistory'
	elif(sheetType == 'cash'):
		title = 'cashflowStatementHistory'
	elif(sheetType == 'income'):
		title = 'incomeStatementHistory'
	else: 
		return ('Incorect SheetType') #change in future to more solid error type

	if(period == 'quarterly'):
		title = title + 'Quarterly'
 
	company_balance_sheet_data_qt = financials.get_financial_stmts(period, sheetType) #get balance sheet
	df = pd.DataFrame(data = None, columns = ['date'])
	for company in tickers:
		tmp = company_balance_sheet_data_qt[title][company]
		dates = len(tmp)
		balance_sheet_contents = set()
		for i in range(0,dates):
			date = (list(tmp[i].keys())[0])
			balance_sheet_contents.update(set(tmp[i][date].keys()))

		for i in range(0,dates):
			date = (list(tmp[i].keys())[0])
			data = {'date': date, 'company': company}
			for key in balance_sheet_contents:
				val = in_dict(tmp[i][date], key)
				data[key] = val
			#'propertyPlantEquipment', 'totalCurrentAssets', 'longTermInvestments', 'netTangibleAssets', 'shortTermInvestments', 'netReceivables', 'accountsPayable']
			df = df.append(data, ignore_index = True)
	return df, company_balance_sheet_data_qt[title]


def get_stock_price_data_withPD(financials, tickers, start_date, end_date, period):
	"""
	Returns stock price data for given ticker symbols.
	Args:
		financials (YahooFinancials): Yahoo financials api object.
		tickers (List[Strings]): A list of strings containing company ticker names.
		start_date (String): A start date for when to start fetching for data.
		end_date (String): A end date for when to stop fetching for data.
		period (String): Represents frequency of financial statement data; quarterly, annually, ect.
	Returns:
		df (DataFrame): The data of the sheet in the form of a DataFrame.
		company_balance_sheet_data_qt[title] (Dictionary): The raw data in the form of a dictionary.
	"""
	#gets historical daily stock price of company
	historical_stock_prices_data = financials.get_historical_price_data(start_date, end_date, period)
	cols = ['company', 'date', 'high', 'low', 'open', 'close', 'volume', "adjclose", 'formatted_date']
	df = pd.DataFrame(data = None, columns = cols)

	for company_name in tickers:
		company_data = historical_stock_prices_data[company_name]
		for x in range(len(company_data['prices'])):
			tmp = company_data['prices'][x]
			data = {'company': company_name,
			'date': tmp['formatted_date'],
			'high': tmp['high'],
			'low': tmp['low'],
			'open': tmp['open'],
			'close': tmp['close'],
			'volume': tmp['volume'],
			'adjclose': tmp['adjclose'],
			'formatted_date': tmp['formatted_date']}
			df = df.append(data, ignore_index = True)
	return df, historical_stock_prices_data



#Used strictly for testing.
if __name__ == "__main__":

	print("Starting...")
	#start_time = time.time()

	tickers = ['MSFT', 'TSLA']#'MRNA'
	start_date = '2000-06-26'
	end_date = '2021-07-02'
	#end_date = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}"
	financials = YahooFinancials(tickers)

	#done
	#print(get_stats(financials, tickers))

	#done
	#df, prices = get_stock_price_data_withPD(financials, tickers, start_date, end_date, 'daily')
	#print(df["company"].value_counts())

	#done
	#df, sheet = get_sheet(financials, tickers, 'annual', 'income')
	#print('\n\nBalance Sheet Information')
	#print(df)

	#done
	#df, sheet = get_sheet(financials, tickers, 'quarterly', 'income')
	#print('\n\nIncome Sheet Information')
	#print(df)

	#done
	#df, sheet = get_sheet(financials, tickers, 'annual', 'cash')
	#print('\n\nIncome Sheet Information')
	#print(df)
