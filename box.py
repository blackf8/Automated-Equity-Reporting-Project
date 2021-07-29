from abc import ABC, abstractmethod, ABCMeta
from yahoofinancials import YahooFinancials as yf
import pandas as pd
import numpy as np
import heapdict
import datetime 
from datetime import date as dt
import logging 

#import test
import input
today =dt.today()
logging.basicConfig(filename=str('DCFcalc'+today.strftime('%Y-%m-%d')),level=logging.INFO,format ='%(asctime)s:%(message)s')
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
    def __init__(self,tickers):
        self.__tickers = tickers
        self.__today = dt.today()
        self.__minusOneYear = dt.today()-datetime.timedelta(days=365)

                    
        #WACC stuff here
    def equalizer(self):
        pass

    def calcWACC(self, ticker): #ticker must be a single str inside of a list
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
        logging.info('Begin of WACC calculations\n\n')
        tickerdataIncome = input.get_sheet(yf(ticker),ticker,'annual','income')
        tickerdataCash = input.get_sheet(yf(ticker),ticker,'annual','cash')
        tickerdataBalance = input.get_sheet(yf(ticker),ticker, 'annual','balance')
        tickerdataSummary = yf.get_summary_data(yf(ticker),reformat=True)
        FVXdata = input.get_stock_price_data_withPD(yf('^FVX'),['^FVX'],self.__minusOneYear.strftime("%Y-%m-%d"),self.__today.strftime("%Y-%m-%d"),'monthly')
        GSPCdata = yf.get_summary_data(yf('^GSPC'),reformat=True)
        # Cost of Equity
        # riskFreeRate = (FVXdata.get('^FVX').get('prices')[len(FVXdata.get('^FVX').get('prices'))-1].get('close'))/100

        riskFreeRate =FVXdata.loc[:,'close'].iloc[-1]
        riskFreeRate = riskFreeRate/100
        logging.info("riskFreeRate: "+str(riskFreeRate))
        beta = tickerdataSummary.get(ticker[0]).get('beta') #yf get_beta()
        #DONT CHANGE THIS, TICKERDATASUMMARY IS NOT IN 
        logging.info("beta: "+str(beta))

        #marketReturn calc
        currentMarketValue = GSPCdata.get('^GSPC').get('regularMarketOpen')
        logging.info('currentMarketValue: '+str(currentMarketValue))
        previousMarketValue = GSPCdata.get('^GSPC').get('regularMarketOpen') #these two may require a bit of sorting
        logging.info('previousMarketValue: '+str(previousMarketValue))
        marketReturn = .098 #((currentMarketValue-previousMarketValue)/abs(previousMarketValue))
        logging.info("marketReturn: "+str(marketReturn))

        marketRiskPremium = marketReturn - riskFreeRate
        logging.info("marketRiskPremium: "+str(marketRiskPremium))

        costOfEquity = riskFreeRate + (beta*marketRiskPremium)
        logging.info("costOfEquity: "+str(costOfEquity))

        #tickerDateIncome = str(list(tickerdataIncome.get('incomeStatementHistory').get('TSLA')[0].keys())[0]) #
        # tickerDateBalance = str(list(tickerdataBalance.get('balanceSheetHistory').get('TSLA')[0].keys())[0])
        # Cost of Debt
        # interestExpense = abs(tickerdataIncome.get('incomeStatementHistory').get('TSLA')[0].get(tickerDateIncome).get('interestExpense')) #COMPLETED tickerdata
         
        interestExpense = abs(tickerdataIncome.loc[0,'interestExpense'])
        logging.info("interestExpense: "+str(interestExpense))

        # longTermDebt = tickerdataBalance.get('balanceSheetHistory').get('TSLA')[0].get(tickerDateBalance).get('longTermDebt') #COMPLETE
        # shortLongTermDebt = tickerdataBalance.get('balanceSheetHistory').get('TSLA')[0].get(tickerDateBalance).get('shortLongTermDebt') #COMPLETE
        longTermDebt = tickerdataBalance.loc[0,'longTermDebt']
        logging.info('longTermDebt: '+str(longTermDebt))
        shortLongTermDebt = tickerdataBalance.loc[0,'longTermDebt']
        logging.info ('shortLongTermDebt: '+str(shortLongTermDebt))
        totalDebt = shortLongTermDebt + longTermDebt
        costofDebt = interestExpense/totalDebt

        logging.info("totalDebt: "+str(totalDebt))
        logging.info ("costofDebt: "+str(+costofDebt))

        #WACC calc
        # ebit = tickerdataIncome.get('incomeStatementHistory').get('TSLA')[0].get(tickerDateIncome).get('ebit') #COMPLETE
        ebit = tickerdataIncome.loc[0,'ebit']
        logging.info("ebit: "+str(ebit))
        
        # equityValue = tickerdataSummary.get('TSLA').get("marketCap")
        equityValue = tickerdataSummary.get(ticker[0]).get('marketCap')
        logging.info('equityValue: '+str(equityValue))
        # cash = tickerdataBalance.get('balanceSheetHistory').get('TSLA')[0].get(tickerDateBalance).get('cash') #COMPLETE
        cash = tickerdataBalance.loc[0,'cash']
        logging.info("cash: "+str(cash))
        enterpriseValue = equityValue+totalDebt-cash
        equityWeight = equityValue/enterpriseValue
        debtWeight = totalDebt/enterpriseValue
        # taxExpense = tickerdataIncome.get('incomeStatementHistory').get('TSLA')[0].get(tickerDateIncome).get('incomeTaxExpense') #COMPLETE
        taxExpense = tickerdataIncome.loc[0,'incomeTaxExpense']
        logging.info("taxExpense: "+str(taxExpense))
        taxRate = taxExpense/ebit
        WACC = (equityWeight*costOfEquity)+(debtWeight*costofDebt*(1-taxRate))
        logging.info("WACC: "+str(WACC))
        logging.info("\n\nEnd of WACC calculations")
        return WACC

    def calcFCFF(self,ticker, WACC): 
        logging.info("\n\nStart of FCFF calculations\n\n")
        def calcDeltaNWC(self):
            balanceSheet = input.get_sheet(yf(ticker),ticker,'annual','balance')
            currentAssets = balanceSheet.loc[:,'totalCurrentAssets']
            currentLiabilities = balanceSheet.loc[:,'totalCurrentLiabilities']
            # changeInNWC = (currentAssetsY1-currentLiabilitiesY1)-(currentAssetsY0-currentLiabilitiesY0)
            changeInNWC = pd.DataFrame(columns=['changeInNWC'])
            logging.info("changeInNWC: "+str(changeInNWC)) 
            #for now, projections are hardcoded, in the future, we will be reading them off a csv file.


        # EBIT Calculation
        # = Revenue - Cost of goods sold - Operating Expenses 
        # FCFF Calculation
        # = EBIT - taxes + (depreciation+amortization) - capital expenditure - change in net working capital (change in NWC)
        # change in NWC = (this year current assets - this year current liabilities) - (last year current assets - last year current liabilities)
        
        incomeStatement = input.get_sheet(yf(ticker),ticker,'annual','income')
        cashflowStatement = input.get_sheet(yf(ticker),ticker,'annual','cash')
        balanceSheet = input.get_sheet(yf(ticker),ticker, 'annual','balance')
        keyStatements = input.get_stats(yf(ticker),ticker)
        revenue = incomeStatement.loc[:,'totalRevenue']
        costOfGoodsSold = incomeStatement.loc[:,'costOfRevenue']
        grossProfit = incomeStatement.loc[:,'grossProfit']
        depreciation = cashflowStatement.loc[:,'depreciation']
        sgaExpenses = incomeStatement.loc[:,'sellingGeneralAdministrative']
        incomeTaxExpense = incomeStatement.loc[:,'incomeTaxExpense']
        capex = cashflowStatement.loc[:,'capitalExpenditures']
        netReceivables = balanceSheet.loc[:,'netReceivables']
        inventory = balanceSheet.loc[:,'inventory']
        totalCurrentLiabilities = balanceSheet.loc[:,'totalCurrentLiabilities']
        cash = balanceSheet.loc[:,'cash']
        shortTermDebt = balanceSheet.loc[:,'shortLongTermDebt']
        longTermDebt = balanceSheet.loc[:,'longTermDebt']
        totalDebt = shortTermDebt + longTermDebt
        sharesOutstanding = keyStatements.loc[:,'sharesOutstanding']

        logging.info("revenue: "+str(revenue)) 
        logging.info("costOfGoodsSold: "+str(costOfGoodsSold)) 
        logging.info("grossProfit: "+str(grossProfit)) 
        logging.info("depreciation: "+str(depreciation)) 
        logging.info("sgaExpenses: "+str(sgaExpenses)) 
        logging.info("incomeTaxExpense: "+str(incomeTaxExpense)) 
        logging.info("capex: "+str(capex)) 
        logging.info("netReceivables: "+str(netReceivables)) 
        logging.info("inventory: "+str(inventory)) 
        logging.info("totalCurrentLiabilities: "+str(totalCurrentLiabilities)) 
        logging.info("cash: "+str(cash)) 
        logging.info("shortTermDebt: "+str(shortTermDebt)) 
        logging.info("longTermDebt: "+str(longTermDebt)) 
        logging.info("totalDebt: "+str(totalDebt)) 
        logging.info("sharesOutstanding: "+str(sharesOutstanding)) 
        #for income tax purposess
        ebit = incomeStatement.loc[:,'ebit']
        logging.info("ebit: "+str(ebit)) 

        yearsProjected = ['2020','2021','2022','2023','2024','2025'] 
        
        #can be optimized for accuracy using Rosenbaum & Pearl DCF changeinNWC method (calculate and project ratios)
        changeInNWC = []
        changeInNWC.append(0)
        #if year x is the current year, then change in net working capital for year x = ((current assets of year x) - (current liabilities of year x-debt)) - ((current assets of year x-1 - cash) - (current liabilities of year x-1-debt))
        #change in: all under balance sheet
        #netReceivables
        #inventory
        #totalCurrentLiabilities
                
        for i in range(3):
            #old - new
            #((old_netR+old_inv)-old_totalCurL)-((new_netR+new_inv)-new_totalCurL)
            #extend this for loops with another loop later for more companies 
            tmp = abs(((netReceivables[i]+inventory[i])-totalCurrentLiabilities[i]))-abs(((netReceivables[i+1]+inventory[i+1])-totalCurrentLiabilities[i+1]))
            # changeInNWC.append(tmp)
            changeInNWC.append(abs(tmp))
        changeInNWC = pd.Series(changeInNWC)
        logging.info("changeInNWC: "+str(changeInNWC))

        ebitda = revenue - costOfGoodsSold - sgaExpenses
        ebit =  ebitda - depreciation #different from ebit for more careful calculations. 
        ebiat = ebit - incomeTaxExpense
        logging.info("ebiat: "+str(ebiat))
        
        unleveredFCF = ebiat + depreciation - capex - changeInNWC
        logging.info("unleveredFCF: "+str(unleveredFCF))
        #incomeTaxRate calculations; IMPROVE ACCURACY OF TAX RATE PROJECTIONS
        incomeTaxRate = incomeTaxExpense/ebit
        tempTaxRate = incomeTaxRate.copy(deep=True)

        for index, value in incomeTaxRate.items():
            tempTaxRate.loc[index] = max(0,value)

        incomeTaxRate = tempTaxRate
        
        #this needs to be like 3 for loops of csv calls, projecting per company, then projecting ever company
        #will be fast
        starterRevenue = list(revenue)
        growthRates = [.1231,.0432,.069,.061,.003,.006] #get these numbers from the excel sheet; csv file
        projRevenues = []
        tempValue = starterRevenue[0]
        projRevenues.append(tempValue)
        for i in range (5):
            tempValue = tempValue*(1+growthRates[i])
            projRevenues.append(tempValue)

        projRevenuesDF = pd.DataFrame(columns=yearsProjected)
        logging.info("projRevenuesDF: "+str(projRevenuesDF))
        projRevenuesDF.loc[0] = projRevenues#loc will be set to i of for loop in future, dw.
        # print(projRevenuesDF)   
        listRevenuesDF = projRevenuesDF.loc[0]
        # print(projRevenuesDF.iloc[0][0]) # [[0],[0]] gives a dataframe, but this gives just a number
        # print(projRevenuesDF)

        
        #Value Projections PROBABLY SHOVE THIS SOMEWHERELSE 
        actualValues = []
        projectedValues = []
        
        actualValues.append(costOfGoodsSold)
        actualValues.append(sgaExpenses)
        actualValues.append(depreciation)
        actualValues.append(capex)
        actualValues.append(changeInNWC)
        actualValues.append(incomeTaxRate)

        for actual in actualValues:
            tempActual = actual.copy(deep=True)
            tempProj = pd.Series()
            for i in range(5):
                avgSeries = tempActual.copy(deep=True)
                avgSeries = avgSeries.loc[i:int(i+3)]
                avg = avgSeries.mean()
                tmpAppend = pd.Series([avg])
                tempProj = tempProj.append(tmpAppend, ignore_index=True)
                tempActual = tempActual.append(tmpAppend, ignore_index=True)
            projectedValues.append(tempProj) #append tempProj for just projections, tempActual includes previous years data along with future projections
        
        projCostOfGoodsSold = projectedValues[0]
        projsgaExpenses = projectedValues[1]
        projDepreciation = projectedValues[2]
        projcapex = projectedValues[3]
        projChangeInNWC = projectedValues[4]
        projIncomeTaxRate = projectedValues[5]
        logging.info("projCostOfGoodsSold: "+str(projCostOfGoodsSold))
        logging.info("projsgaExpenses: "+str(projsgaExpenses))
        logging.info("projDepreciation: "+str(projDepreciation))
        logging.info("projcapex: "+str(projcapex))
        logging.info("projChangeInNWC: "+str(projChangeInNWC))
        logging.info("projIncomeTaxRate: "+str(projIncomeTaxRate))
        # print (projectedValues)
        # print("Start of actualValues \n")      
        # print(actualValues)
        # print("Start of projectedValues \n")
        # print(projectedValues)

        #projected ebit calculations here 
        # 
        listRevenuesDF = listRevenuesDF.reset_index(drop = True)
        projRevenuesOnly = listRevenuesDF.drop(labels=[0]) 
        projRevenuesOnly = projRevenuesOnly.reset_index(drop = True)
        projebitda = projRevenuesOnly - projCostOfGoodsSold - projsgaExpenses
        logging.info("projebitda: "+str(projebitda))
        # tmpProjebitda = []
        # for i in range (5):
        #     tmp = projRevenuesOnly.iloc[i] - projCostOfGoodsSold.iloc[i] - projsgaExpenses.iloc[i]
        #     tmpProjebitda.append(tmp)
        # projebitda = pd.Series(tmpProjebitda)
        # print(projCostOfGoodsSold)
        # print(projsgaExpenses)
        # print(projebitda)
        projebit = projebitda - projDepreciation
        # print(projebit)
        projIncomeTaxExpense = projebit*projIncomeTaxRate
        # print(projIncomeTaxExpense)
        projebiat = projebit - projIncomeTaxExpense
        # print(projebiat)
        # end of ebit calc

        projUnleveredFCFF = projebiat + projDepreciation - projcapex - projChangeInNWC
        # print(projUnleveredFCFF)
        #start of Discounted Levered FCFF
        # print(WACC)
        tmpVal = pd.Series() #((1+WACC)^t)
        for i in range(5):
            x = (1+WACC)**(i+1)
            tmpInsert = pd.Series([x])
            tmpVal = tmpVal.append(tmpInsert, ignore_index=True)
        projLeveredFCFF = projUnleveredFCFF/tmpVal
        # print(projLeveredFCFF)
        #end of Discounted Levered FCFF
        perpetualGrowthRate = .02
        terminalValue = projLeveredFCFF.iloc[-1]*((x*(1+perpetualGrowthRate))/(WACC-perpetualGrowthRate))
        enterpriseValue = projLeveredFCFF.sum()+terminalValue   
        equityValue = enterpriseValue + cash.iloc[-1] - totalDebt.iloc[-1]
        estimatedSharePrice = equityValue/sharesOutstanding.iloc[-1]
        print(estimatedSharePrice)
        logging.info("\n\n###### estimatedSharePrice: "+str(estimatedSharePrice)"\n\n")
        return estimatedSharePrice
        # print (estimatedSharePrice)
    
    def tickerEvaluator(self,ticker):
        WACC = self.calcWACC (ticker)
        estimatedSharePrice = self.calcFCFF(ticker,WACC)
        return estimatedSharePrice

    def totalEvaluator(self,tickers):
        df = pd.Series()
        for tick in tickers: #input.py can only accept lists, so tick is str, ticker is list with a str, and tickers is list of strs
            ticker = [tick]
            estimatedSharedPrice = self.tickerEvaluator(ticker)
            tmp = {tick:estimatedSharedPrice}
            tmpdf = pd.Series(tmp)
            df.append(tmpdf)
        print(df)
        return df
    

        
if __name__ == "__main__":
    # send to output
    #stocks for testing: GME, AMC, TSLA
    pass
