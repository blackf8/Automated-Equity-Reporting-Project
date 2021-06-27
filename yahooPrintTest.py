import input
from yahoofinancials import YahooFinancials as yf

df = []
tickers = ['^GSPC']
start_date = '2020-06-20'
end_date = '2021-6-20'
financials = yf(tickers)


# test = yf.get_financial_stmts(financials,'annual','balance',reformat=True)
# tickerDateBalance = str(list(test.get('balanceSheetHistory').get('TSLA')[0].keys())[0])
# print (test)
# print('------------------------')
# print(test.get('balanceSheetHistory').get('TSLA')[0].get(tickerDateBalance).get('shortLongTermDebt'))

test = yf.get_summary_data(financials,reformat=True) #this can grab beta.
# print (test.get('^GSPC').get('previousClose'))
print(test)

# test = yf.get_historical_price_data(financials,start_date,end_date,'daily')
# print(test.get('^FVX').get('prices')[len(test.get('^FVX').get('prices'))-1])
# print (test.get('^FVX').get('prices')[len(test.get('^FVX').get('prices'))-1].get('close'))