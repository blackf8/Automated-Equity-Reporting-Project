import input
from box import PriceBox, DCFbox
from yahoofinancials import YahooFinancials as yf


df = []
tickers = ['TSLA']
start_date = '2018-11-27'
end_date = '2018-11-28'
financialsTicker = yf(tickers)
financialsFVX = yf('^FVX')
financialsGSPC = yf('^GSPC')


FVXdata = yf.get_historical_price_data(financialsFVX,'2020-06-22','2021-06-22','monthly')
GSPCdata = yf.get_summary_data(financialsGSPC,reformat=True)
tickerdataIncome = yf.get_financial_stmts(financialsTicker,'annual','income',reformat=True)
tickerdataBalance = yf.get_financial_stmts(financialsTicker,'annual','balance',reformat=True)
tickerdataCash = yf.get_financial_stmts(financialsTicker,'annual','cash',reformat=True)
tickerdataSummary = yf.get_summary_data(financialsTicker,reformat=True)
# for ticker in (tickers):
#     df.append(input.get_stock_price_data_withPD(financials,ticker,start_date,end_date,'daily')) 

box1 = DCFbox(financialsTicker)

box1.calcWACC(FVXdata, GSPCdata, tickerdataIncome, tickerdataBalance, tickerdataCash, tickerdataSummary)
