import input
from box import PriceBox, DCFbox
from yahoofinancials import YahooFinancials as yf


df = []
tickers = ['TSLA','F']
financialsTicker = yf(tickers)
# start_date = '2018-11-27'
# end_date = '2018-11-28'
# financialsFVX = yf('^FVX')
# financialsGSPC = yf('^GSPC')


# FVXdata = yf.get_historical_price_data(financialsFVX,'2020-06-22','2021-06-22','monthly')
# tickerdataIncome = yf.get_financial_stmts(financialsTicker,'annual','income',reformat=True)
# tickerdataBalance = yf.get_financial_stmts(financialsTicker,'annual','balance',reformat=True)
# tickerdataCash = yf.get_financial_stmts(financialsTicker,'annual','cash',reformat=True)
# for ticker in (tickers):
#     df.append(input.get_stock_price_data_withPD(financialsTicker,ticker,start_date,end_date,'daily')) 

box1 = DCFbox(tickers)
box1.totalEvaluator(tickers)
