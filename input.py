import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials
import time
import datetime
pd.set_option('display.max_columns',50)

#checks if key exists in dict, if so return corresponding val
def in_dict(dict, key):
	if(key in dict):
		return dict[key]
	else:
		return None

def format_float(value):
	return f'{value:,.2f}'

pd.options.display.float_format = '{:,.2f}'.format

def get_stats(financials, tickers):
	company_key_statistics_data = financials.get_key_statistics_data() #includes profit margins, forward eps, yearly change etc.
	return company_key_statistics_data[tickers]

#returns a dataframe obj representing the companies balance sheet
#To do
#1.) show more years [in prog] ???
	#cant pull all the years without finance plus
#2.) respond accurately to period parameter [check]
#3.) add cash to possible sheets [check]
#4.) add multiple companies ?
	# Adjust code to keep in mind we want to run on multiple companies.
	# focusing on fetching the data (put on burner for now.)
#5.) misaligned possible data values ? --> dict idea. [check]
	#detect if a value is missing.   } Something we need to look into as we use data.
	#work towards fix if possibe.    }


#implement yf.get_summary_data(financials,reformat=True), refer to yahooPrintTeset.py for how it works.
#
def get_sheet(financials, tickers, period, sheetType):
	title = ''
	if(sheetType == 'balance'):
		title = 'balanceSheetHistory'
	elif(sheetType == 'cash'):
		title = 'cashflowStatementHistory'
	else:
		title = 'incomeStatementHistory'


	if(period == 'quarterly'):
		title = title + 'Quarterly'

	company_balance_sheet_data_qt = financials.get_financial_stmts(period, sheetType) #get balance sheet

	df = pd.DataFrame(data = None, columns = ['date'])
	tmp = company_balance_sheet_data_qt[title][tickers]
	dates = len(tmp)

	balance_sheet_contents = set()
	for i in range(0,dates):
		date = (list(tmp[i].keys())[0])
		balance_sheet_contents.update(set(tmp[i][date].keys()))

	for i in range(0,dates):
		date = (list(tmp[i].keys())[0])
		data = {'date': date}
		for key in balance_sheet_contents:
			val = in_dict(tmp[i][date], key)
			data[key] = val
		#'propertyPlantEquipment', 'totalCurrentAssets', 'longTermInvestments', 'netTangibleAssets', 'shortTermInvestments', 'netReceivables', 'accountsPayable']
		df = df.append(data, ignore_index = True)
	return df, tmp


def get_financial_stmt_withPD(financials, tickers, period, finStmtType):
	financialStmt = financials.get_financial_stmts(tickers,period,finStmtType,reformat=True)
	pass

#returns stock price data for ticker symbol
def get_stock_price_data_withPD(financials, tickers, start_date, end_date, period):
	#gets historical daily stock price of company
	historical_stock_prices_data = financials.get_historical_price_data(start_date, end_date, period)
	company_data = historical_stock_prices_data[tickers]
	df = pd.DataFrame(data = None, columns = list(company_data["prices"][0].keys()))
	for x in range(len(company_data['prices'])):
		tmp = company_data['prices'][x]
		data = {'date': tmp['formatted_date'],
		'high': tmp['high'],
		'low': tmp['low'],
		'open': tmp['open'],
		'close': tmp['close'],
		'volume': tmp['volume'],
		'adjclose': tmp['adjclose'],
		'formatted_date': tmp['formatted_date']}
		df = df.append(data, ignore_index = True)
	return df, list(company_data["prices"])

# def getMarketData():
# 	tickers = 'MRNA'
# 	financials = YahooFinancials(tickers)

# 	#	company_stock_price = financials.get_stock_price_data() #gets stock price information

# 	historical_stock_prices_data = financials.get_historical_price_data('2015-11-27', '2020-11-27', 'daily') #gets historical daily stock price of company
# 	#	get_Div_data(historical_stock_prices_data[tickers])
# 	get_stock_price_data_withPD(historical_stock_prices_data[tickers])
# 	#	company_balance_sheet_data_qt = financials.get_financial_stmts('quarterly', 'balance') #get balance sheet
# 	#	company_income_statement_data_qt = financials.get_financial_stmts('quarterly', 'income') #get income statement

# 	#company_key_statistics_data = financials.get_key_statistics_data() #includes profit margins, forward eps, yearly change etc.
# 	#	get_forward_pe(company_key_statistics_data[tickers])
# 	#	get_trailing_eps(company_key_statistics_data[tickers])
# 	#	get_foward_eps(company_key_statistics_data[tickers])
# 	#	get_ytdReturn(company_key_statistics_data[tickers])

# 	#1company_earnings_data = financials.get_stock_earnings_data() #historical eps only for 1 year span
# 	#	get_earnings_data(company_earnings_data[tickers])

# 	#1company_dividend_yield = financials.get_dividend_yield() #current dividends yield
# 	#1company_dividend = financials.get_dividend_rate() #current dividends rate
# 	#1company_avg_div_yield_1year = financials.get_annual_avg_div_yield()	#average 1 year div yield
# 	#1company_avg_div_yield_5year = financials.get_five_yr_avg_div_yield()	#average 5 year div yield
# 	#1company_eps = financials.get_earnings_per_share() #current eps
# 	#1company_pe = financials.get_pe_ratio()	#current pe ratio
# 	#1company_beta = financials.get_beta() #current beta
# 	#1company_current_stock_price = financials.get_current_price() #current stock price

# 	#1company_revenue = financials.get_total_revenue() #current company revenue
# 	#1company_operating_income = financials.get_operating_income() #current company operating income
# 	#1company_net_income = financials.get_net_income() #current net income

# 	#1company_yearly_high = financials.get_yearly_high()	#get yearly high
# 	#1company_yearly_low = financials.get_yearly_low()	#get yearly low
# 	#1company_moving_50 = financials.get_50day_moving_avg()	#50 day moving average of stock
# 	#1company_moving_200 = financials.get_200day_moving_avg()	#200 day moving average of stock

# def api_calls():
# 	tmp = {}
# 	tmp['company_dividend_yield'] = financials.get_dividend_yield() #current dividends yield
# 	#print(tmp['company_dividend_yield'])

# 	tmp['company_dividend'] = financials.get_dividend_rate() #current dividends rate
# 	#print(tmp['company_dividend'])


# 	tmp['company_avg_div_yield_1year'] = financials.get_annual_avg_div_yield()	#average 1 year div yield
# 	#print(tmp['company_avg_div_yield_1year'])

# 	tmp['company_avg_div_yield_5year'] = financials.get_five_yr_avg_div_yield()	#average 5 year div yield
# 	#print(tmp['company_avg_div_yield_5year'])



# 	tmp['company_eps'] = financials.get_earnings_per_share() #current eps
# 	#print(tmp['company_eps'])
# 	tmp['company_pe'] = financials.get_pe_ratio()	#current pe ratio
# 	#print(tmp['company_pe'])
# 	tmp['company_beta'] = financials.get_beta() #current beta
# 	#print(tmp['company_beta'])
# 	tmp['company_current_stock_price'] = financials.get_current_price() #current stock price
# 	#print(tmp['company_current_stock_price'])


# 	tmp['company_revenue'] = financials.get_total_revenue() #current company revenue
# 	#print(tmp['company_revenue'])
# 	tmp['company_operating_income'] = financials.get_operating_income() #current company operating income
# 	#print(tmp['company_operating_income'])
# 	tmp['company_net_income'] = financials.get_net_income() #current net income
# 	#print(tmp['company_net_income'])

# 	tmp['company_yearly_high'] = financials.get_yearly_high()	#get yearly high
# 	#print(tmp['company_yearly_high'])
# 	tmp['company_yearly_low'] = financials.get_yearly_low()	#get yearly low
# 	#print(tmp['company_yearly_low'])

# 	tmp['company_moving_50'] = financials.get_50day_moving_avg()	#50 day moving average of stock
# 	#print(tmp['company_moving_50'])
# 	tmp['company_moving_200'] = financials.get_200day_moving_avg()	#200 day moving average of stock
# 	#print(tmp['company_moving_200'])

# 	return tmp

if __name__ == "__main__":

	print("Starting...")
	start_time = time.time()

	tickers = 'MSFT'#'MRNA'
	start_date = '2000-06-26'
	end_date = '2021-07-02'
	#end_date = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}"
	financials = YahooFinancials(tickers)

	#done
	df, prices = get_stock_price_data_withPD(financials, tickers, start_date, end_date, 'daily')

	#done
	df, sheet = get_sheet(financials, tickers, 'annual', 'income')
	print('\n\nBalance Sheet Information')
	#print(df)

	# #done
	df, sheet = get_sheet(financials, tickers, 'quarterly', 'income')
	print('\n\nIncome Sheet Information')
	#print(df)


	# #done
	df, sheet = get_sheet(financials, tickers, 'annual', 'cash')
	print('\n\nIncome Sheet Information')
	print(df)

	#company_balance_sheet_data_qt = financials.get_financial_stmts('annual', 'cash') #get balance sheet
	#print(company_balance_sheet_data_qt)


	#company_balance_sheet_data_qt = financials.get_financial_stmts('annual', 'cash') #get balance sheet
	#print(company_balance_sheet_data_qt)
	"""
	df = get_stats(financials, tickers)
	print('\n\nStatistics')
	for i in df:
		print(i, df[i])
	"""

	"""
	print('\n\nExtra Api Calls')
	df = api_calls()
	for i in df:
		print(i, df[i])

	print("--- %s seconds ---" % (time.time() - start_time))
	print("Done.")
	"""



'''
Revenue: Price * Quantity of goods
Cost of Revenue: Cost of goods
Gross Income : Cost of Revenue - Net Income

Operating Income: Profit before taxes / other expenses
Also known as EBIT: Earnings Before Interest and Tax
EBITDA: Depreciation Amortization
Depreciation: cost of stuff that goes down
Amortization: cost of things depreciating
Additional expenses bsides interest / tax

Net Income: Profit after all costs

Cash Flow: Movement of money within a company
Think of a company as a bond.
Cash Flow = EBIT
- taxes
+ DA
- Capital Expenditures  (Investments in productive capacitity such as factories or machines)
- Increase in Non-Cash Working Capital	(Current Assets - Current Liabilitity)

Unlevered Cash Flow: aka raw cash flow
Once you take this raw cash flow you need to discount it

Old money is worth more.


WACC: weight_{equity} * cost of equity + weight_debt * cost of debt
weight_{equity} = Equity Value/(Equity Value + Debt Value)
weight_debt = Debt Value/(Equity Value + Debt Value)
Equity Value = Shares Outstanding * Current Share Price
Debt Value = Total Debt
Cost of Equity = Beta * (market return - risk free investment) - risk free investment
Beta: yahoo finance
Market Return: S&P annual return
Risk Free Investment: Usually use 10Y Treasury Yield(yahoo finance)
Cost of Debt = Interest Expense / Total Debt
Overall cost of the company you are gonna invest in

Terminal Value: Company will grow until the terminal value and then grow at a steady rate (2-3%)

Perpetual Growth: Last calculated cash flow*(1 + growth rate g)/(WACC - growth rate g)

Present Value of Company = Sum of Cash flows + Perpetual Growth
'''
