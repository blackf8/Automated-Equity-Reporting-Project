from yahoofinancials import YahooFinancials

def getMarketData():
	tickers = 'MRNA'
	financials = YahooFinancials(tickers)

#	company_stock_price = financials.get_stock_price_data() #gets stock price information

	historical_stock_prices_data = financials.get_historical_price_data('2015-11-27', '2020-11-27', 'daily') #gets historical daily stock price of company
#	get_Div_data(historical_stock_prices_data[tickers])
	get_stock_price_data(historical_stock_prices_data[tickers])

#	company_balance_sheet_data_qt = financials.get_financial_stmts('quarterly', 'balance') #get balance sheet
#	company_income_statement_data_qt = financials.get_financial_stmts('quarterly', 'income') #get income statement

	company_key_statistics_data = financials.get_key_statistics_data() #includes profit margins, forward eps, yearly change etc.
#	get_forward_pe(company_key_statistics_data[tickers])
#	get_trailing_eps(company_key_statistics_data[tickers])
#	get_foward_eps(company_key_statistics_data[tickers])
#	get_ytdReturn(company_key_statistics_data[tickers])

	company_earnings_data = financials.get_stock_earnings_data() #historical eps only for 1 year span
#	get_earnings_data(company_earnings_data[tickers])

	company_dividend_yield = financials.get_dividend_yield() #current dividends yield
	company_dividend = financials.get_dividend_rate() #current dividends rate
	company_avg_div_yield_1year = financials.get_annual_avg_div_yield()	#average 1 year div yield
	company_avg_div_yield_5year = financials.get_five_yr_avg_div_yield()	#average 5 year div yield
	company_eps = financials.get_earnings_per_share() #current eps
	company_pe = financials.get_pe_ratio()	#current pe ratio
	company_beta = financials.get_beta() #current beta
	company_current_stock_price = financials.get_current_price() #current stock price

	company_revenue = financials.get_total_revenue() #current company revenue
	company_operating_income = financials.get_operating_income() #current company operating income
	company_net_income = financials.get_net_income() #current net income

	company_yearly_high = financials.get_yearly_high()	#get yearly high
	company_yearly_low = financials.get_yearly_low()	#get yearly low
	company_moving_50 = financials.get_50day_moving_avg()	#50 day moving average of stock
	company_moving_200 = financials.get_200day_moving_avg()	#200 day moving average of stock

#for stock price data
def get_price_data(company_data):
	keyList = list(company_data.keys())
	for x in keyList:
		company_data_specifics = company_data[x]
		print(str(x) + ": " + str(company_data_specifics))

#for hitorical price data
def get_Div_data(company_data):
	div_date_data = company_data['eventsData']['dividends']
	keyList = list(div_date_data.keys())
	print("Dividends Data")
	for date in keyList:
		div_price = div_date_data[date]['amount']
		print(str(date) + ": " + str(div_price))

def get_stock_price_data(company_data):
	historic_stock_price = company_data['prices']
	print("date: high | low | open | close | volume")
	for x in range(len(historic_stock_price)):
		date = historic_stock_price[x]['formatted_date']
		high = historic_stock_price[x]['high']
		low = historic_stock_price[x]['low']
		open = historic_stock_price[x]['open']
		close = historic_stock_price[x]['close']
		volume = historic_stock_price[x]['volume']
		print(str(date) + ": " + str(high) + " | " + str(low) + " | " + str(open) + " | " + str(close) + " | " + str(volume))

#for key statistics data
def get_foward_eps(company_data):
	forward_eps = company_data['forwardEps']
	print("Forward EPS: " + str(forward_eps))

def get_trailing_eps(company_data):
	trailing_eps = 	company_data['trailingEps']
	print("Trailing EPS: " + str(trailing_eps))

def get_ytdReturn(company_data):
	ytdReturn = company_data['ytdReturn']
	print("Year-to-Date Returns: " + str(ytdReturn))

def get_forward_pe(company_data):
	forward_pe = company_data['forwardPE']
	print("Forward P/E: " + str(forward_pe))

#stock earnings data
def get_earnings_data(company_data):
	earnings_data = company_data['earningsData']['quarterly']
	print("Earnings(past 4 quarters)")
	for quarter_earnings in earnings_data:
		print(quarter_earnings)

if __name__ == "__main__":
	getMarketData()
