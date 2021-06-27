import input
from box import PriceBox
from yahoofinancials import YahooFinancials


df = []
tickers = ['TSLA','GME','AMC']
start_date = '2015-11-27'
end_date = '2015-11-27'
financials = YahooFinancials(tickers)
# for ticker in (tickers):
#     df.append(input.get_stock_price_data_withPD(financials,ticker,start_date,end_date,'daily')) 

box1 = PriceBox(start_date, end_date,financials)
print(box1)