from abc import ABC, abstractmethod, ABCMeta
import heapdict
#import test
import input

# things needed (some are done)
# list of apis (preset inside each method)
# list of tickers (input)
# list of the results
# empty thing for data
# method for basic evaluation
# method that calls basic eval for each ticker  - implement specifics, will need to call a a method in input to get data
# one of two prev adds results to a list, mayb 2d array
# *maaaybe a method that takes the results and gives them a value that can be generalized more

class AbstractBox(ABC):
    # apiList=[]
    # tickerList=[]
    # resultList=[]
    # @abstractmethod
    # def __init__(self, n): #abstract constructor, idfk if this needs to be abstract or not bc we need tickers to be not abstract
    #     self.n = n
    # commented out due to unnecessary input
    # @abstractmethod
    # def inputProcessors(self):
    #     pass
    @abstractmethod
    def tickerEvaluator(self): #more parameters after talk w prabu
        pass
    @abstractmethod
    def totalEvaluator(self): # some specifics after prabu
        pass #dont think this needs to be abstract, but also we havent defined any ticker object bc its abstract as of rn so unsure
    @abstractmethod
    def equalizer(self):#this balances the results so diff boxes can be compared
        pass


class PriceBox(AbstractBox):
    def __init__(self, startDate, endDate, financials):
         #assumed dictionary of stocks we need to pull
        self.__startDate = startDate
        self.__endDate = endDate
        self.__financials = financials
        self._resultList = [[]]

    def tickerEvaluator(self, ticker):  # needs the 2 dates that are to be analyzed, also needs the ticker or tickers needed. If it only works with one ticker might want to do it inside evaluator

        df = input.get_stock_price_data_withPD(self.__financials,ticker,self.__startDate,self.__endDate,'daily')
        print (df)
        return

         #pulls out the company value as pandas
        # get value of ticker at startDate
        # get value of ticker at endDate-1110
        # compute percent price increase by startDate value/ endDate-1 value

    def totalEvaluator(self, tickerList):
        #
        hd = dict.fromkeys(tickerList)

        for ticker in tickerList:
            tickerValue = self.tickerEvaluator(ticker)
            hd[ticker]= tickerValue
        return hd

        # get the dictionary
        # run ticketEvaluator for all tickers in tickerList \/\/\/
        # for i in tickerList:
        #   binary_tree.append(tickerEvaluator(self, i))
        # sort the dictionary with some sort of 21a heresy to rank every company
        # return that

    def equalizer(self):
        pass #pass for now, there is only one box



class DCFbox(AbstractBox):
    def __init__(self,financials):
        self.__financials = financials
        #WACC stuff here
    def tickerEvaluator(self):
        pass

    def totalEvaluator(self):
        pass

    def equalizer(self):
        pass

    def calcWACC(self, FVXdata, GSPCdata, tickerdataIncome, tickerdataBalance, tickerdataCash, tickerdataSummary):
        #variables needed:
        # WACC needs Cost of Equity and Cost of Debt

        #Risk Free Rate -->
        #Company Beta
        #Market Risk Premium = Market Return - Risk Free Rate
        #Cost of Equity = Risk Free Rate + (Company Beta * Market Risk Premium)

        #Interest Expense
        #Total Debt
        #Cost of Debt = Interest Expense/Total Debt

        #WACC
        # Enterprise Value = Equity Value + Total Debt - Cash
        # Tax Rate = Tax Expense/EBIT
        # Equity Weight = Equity Value/Enterprise Value
        # Equity Value = Current Share Price*Shares Outstanding
        # Debt Weight = Total Debt/Enterprise Value
        # WACC = (Equity Weight * Cost of Equity) + (Debt Weight * Cost of Debt * (1 - Tax Rate))

        # riskFreeRate = constant, use yahoo finance [^FVX]
        # beta = beta # grab this with test = yf.get_summary_data(financials,reformat=True)
        # marketReturn = e #percent change of ['^GSPC'] ticker (S&P 500 with 1 year) of yf.get_historical_price_data(financials,start_date,end_date,'monthly')
        # interestExpense = get_financial_stmts(annual,'income')

        # Possible workarounds: use pandas to compile list of dicts for marketValue values for easier reading

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #TODO
        #1.) make sure all strings are set as variables eventually (e.g TSLA can and will change)
        #2.) increase readability, probably though some pandas operation we can ask prabu
        #3.) abs value everything?
        #4.) figure out what makes this update every second
        #5.) accuracy improvement
        #5a.) marketReturn is a default number, see if this can be edited.


        # Cost of Equity
        riskFreeRate = (FVXdata.get('^FVX').get('prices')[len(FVXdata.get('^FVX').get('prices'))-1].get('close'))/100
        print ("riskFreeRate: "+str(riskFreeRate))
        beta = tickerdataSummary.get('TSLA').get('beta') #yf get_beta()
        print ("beta: "+str(beta))

        #marketReturn calc
        currentMarketValue = GSPCdata.get('^GSPC').get('regularMarketOpen')
        previousMarketValue = GSPCdata.get('^GSPC').get('regularMarketOpen') #these two may require a bit of sorting
        marketReturn = .098 #((currentMarketValue-previousMarketValue)/abs(previousMarketValue))
        print ("marketReturn: "+str(marketReturn))

        marketRiskPremium = marketReturn - riskFreeRate
        print ("marketRiskPremium: "+str(marketRiskPremium))

        costOfEquity = riskFreeRate + (beta*marketRiskPremium)
        print ("costOfEquity: "+str(costOfEquity))

        tickerDateIncome = str(list(tickerdataIncome.get('incomeStatementHistory').get('TSLA')[0].keys())[0]) #
        tickerDateBalance = str(list(tickerdataBalance.get('balanceSheetHistory').get('TSLA')[0].keys())[0])

        #Cost of Debt
        interestExpense = abs(tickerdataIncome.get('incomeStatementHistory').get('TSLA')[0].get(tickerDateIncome).get('interestExpense')) #COMPLETED tickerdata
        print ("interestExpense: "+str(interestExpense))

        longTermDebt = tickerdataBalance.get('balanceSheetHistory').get('TSLA')[0].get(tickerDateBalance).get('longTermDebt') #COMPLETE
        shortLongTermDebt = tickerdataBalance.get('balanceSheetHistory').get('TSLA')[0].get(tickerDateBalance).get('shortLongTermDebt') #COMPLETE
        totalDebt = shortLongTermDebt + longTermDebt
        costofDebt = interestExpense/totalDebt

        print ("totalDebt: "+str(totalDebt))
        print ("costofDebt: "+str(+costofDebt))

        #WACC calc
        ebit = tickerdataIncome.get('incomeStatementHistory').get('TSLA')[0].get(tickerDateIncome).get('ebit') #COMPLETE
        print ("ebit: "+str(ebit))

        equityValue = tickerdataSummary.get('TSLA').get("marketCap")
        cash = tickerdataBalance.get('balanceSheetHistory').get('TSLA')[0].get(tickerDateBalance).get('cash') #COMPLETE
        enterpriseValue = equityValue+totalDebt-cash
        equityWeight = equityValue/enterpriseValue
        debtWeight = totalDebt/enterpriseValue

        taxExpense = tickerdataIncome.get('incomeStatementHistory').get('TSLA')[0].get(tickerDateIncome).get('incomeTaxExpense') #COMPLETE

        taxRate = taxExpense/ebit
        WACC = (equityWeight*costOfEquity)+(debtWeight*costofDebt*(1-taxRate))
        print ("WACC: "+str(WACC))
        return WACC

    def calcFCFF(self): 
        # EBIT Calculation
        # = Revenue - Cost of goods sold - Operating Expenses 
        # FCFF Calculation
        # = EBIT - taxes + (depreciation+amortization) - capital expenditure - change in net working capital (change in NWC)
        # change in NWC = (this year current assets - this year current liabilities) - (last year current assets - last year current liabilities)

        pass
if __name__ == "__main__":
    # send to output
    #stocks for testing: GME, AMC, TSLA
    pass
