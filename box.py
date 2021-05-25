from abc import ABC, abstractmethod, ABCMeta
import test
# things needed (some are done)
# list of apis (preset inside each method)
# list of tickers (input)
# list of the results
# empty thing for data
# method for basic evaluation
# method that calls basic eval for each ticker  - implement specifics, will need to call a a method in input to get data
# one of two prev adds results to a list, mayb 2d array
# *maaaybe a method that takes the results and gives them a value that can be generalized more

class abstractBox(object, metaclass=ABCMeta):
    apiList=[]
    tickerList=[]
    resultList=[]
    
    @abstractmethod
    def __init__(self, n): #abstract constructor, idfk if this needs to be abstract or not bc we need tickers to be not abstract
        self.n = n
    @abstractmethod
    def tickerEvaluator(self): #more parameters after talk w prabu
        pass 
    def totalEvaluator(self): # some specifics after prabu
        pass #dont think this needs to be abstract, but also we havent defined any ticker object bc its abstract as of rn so unsure
    @abstractmethod
    def equalizer(self):#this balances the results so diff boxes can be compared
        pass

