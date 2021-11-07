import input
from box import PriceBox, DCFbox
from yahoofinancials import YahooFinancials as yf
import time
startTime = time.time()


#only works for tsla atm, need to make this more generalized.

df = []
tickers = ['TSLA']
start_date = '2018-11-27'
end_date = '2018-11-28'
financialsTicker = yf(tickers)
financialsFVX = yf('^FVX')
financialsGSPC = yf('^GSPC')


FVXdata, GSPCdata, tickerdataIncome, tickerdataBalance, tickerdataCash, tickerdataSummary = input.boot_data(start_date, end_date, financialsTicker, financialsFVX, financialsGSPC)
df.append(input.get_stock_price_data_withPD(financialsTicker,tickers,start_date,end_date,'daily'))
box1 = DCFbox(financialsTicker, tickers)
WACCtemp = box1.calcWACC(FVXdata, GSPCdata, tickerdataIncome, tickerdataBalance, tickerdataCash, tickerdataSummary)
box1.WACC = WACCtemp
box1.calcFCFF()



executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
