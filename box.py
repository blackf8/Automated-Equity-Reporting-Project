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
    
    if __name__ == "__main__":
        # send to output
        #stocks for testing: GME, AMC, TSLA

        pass 

