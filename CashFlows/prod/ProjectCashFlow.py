'''
Created on Apr 15, 2016

@author: XING
'''
import math
import CashFlows.prod.Depreciation as Depreciation

class ProjectCashFlow(object):
    '''
    classdocs
    '''


    def __init__(self, duration, nMACRS, MARR,
                 investmentCapital, salvageValue, taxRate):
        '''
        Constructor
        '''
        self.duration = duration
        self.nMACRS = nMACRS
        self.taxRate = taxRate
        self.MARR = MARR
        self.investmentCapital = investmentCapital
        self.salvageValue = salvageValue
#         self.demand = demand
#         self.price = price
#         self.variableCost = variableCost 
#         self.fixedCost = fixedCost
        
    def getRevenue(self, duration, price, demand):
        revenue = [1.0 * price * demand] * duration
        revenue = [0] + revenue
        return revenue

            
    def getMACRS(self, n):
        if (n == 3):
            MACRS = [0, .3333, .4445, .1481, .0741]
        elif (n == 5):
            MACRS = [0, .2, .32, .192, .1152, .1152, .576]
        elif (n == 7):
            MACRS = [0, .1429, .2449, .1749, .1249, .0893, .0892, .0893, .0446]
        elif (n == 10):
            MACRS = [0, .1, .18, .144, .1152, .0922, .0737, .0655, .0655, .0656, .0655, .0328]
        return MACRS

    def depreciationMACRS(self, nMACRS, investmentCapital = 1.0, duration = None):
        if (duration == None):
            duration = nMACRS + 1
        depreciation = [0] * (duration + 1)
        MACRS = self.getMACRS(nMACRS)
        n = min(duration, nMACRS + 1)
        for i in range(1, n + 1):
            depreciation[i] = investmentCapital * MACRS[i]
        if (nMACRS + 1 > duration):
            depreciation[duration] = investmentCapital * MACRS[duration] / 2.0
        return depreciation           
        
    def getDiscountFactor(self, duration, MARR):
        df = [1.0 / ((1.0 + MARR)**i) for i in range(duration + 1)]
        return df
    
    def getCost(self, variableCost, demand, fixedCost, duration):
        cost = [1.0 *variableCost * demand + fixedCost] * duration
        cost = [0] + cost
        return cost
        
    def getNetIncome(self, taxRate, duration, nMACRS, investmentCapital, price, demand, variableCost, fixedCost):
        revenue = self.getRevenue(duration, price, demand)
        cost = self.getCost(variableCost, demand, fixedCost, duration)
        depreciation = self.getDepreciation(duration, nMACRS, investmentCapital)
        #debtInterest = [0] * (duration+1)
        netIncome = [0] * (duration + 1)
        for i in range(1, duration + 1):
            taxableIncome = revenue[i] - cost[i] - depreciation[i] #- debtInterest[i]
            netIncome[i] = (1.0 - taxRate) * taxableIncome
        return netIncome
    
    def getGainsTax(self, investmentCapital, duration, nMACRS, salvageValue, taxRate):
        depreciation = self.getDepreciation(duration, nMACRS, investmentCapital)
        bookValue = investmentCapital - sum(depreciation)
        gains = salvageValue - bookValue
        return taxRate * 1.0 * gains
    
    def getNetCashFlow(self, taxRate, duration, nMACRS, investmentCapital, price, demand, variableCost, fixedCost, salvageValue, workingCapital):
        ncf = [0] * (duration + 1)
        ncf[0] = -investmentCapital - workingCapital
        netIncome = self.getNetIncome(taxRate, duration, nMACRS, investmentCapital, price, demand, variableCost, fixedCost)
        depreciation = self.getDepreciation(duration, nMACRS, investmentCapital)
        for i in range(1, duration + 1):
            ncf[i] = netIncome[i] + depreciation[i] 
        ncf[duration] = ncf[duration] + salvageValue - self.getGainsTax(investmentCapital, duration, nMACRS, salvageValue, taxRate) + workingCapital
        return ncf
    
    def getPresentValue(self, cashFlow, MARR):
        n = len(cashFlow) - 1
        pv = [0] * (n + 1)
        df = self.getDiscountFactor(n, MARR)
        for i in range(n + 1):
            pv[i] = cashFlow[i] * df[i]
        return pv
    
    def getNPV(self, presentValue):
        return sum(presentValue)
    
change = [-.2, -.15, -.1, -.05, 0, .05, .1, .15, .2] 

duration = 13
nMACRS = 7
taxRate = .39
MARR = .2
investmentCapital = 265000 + 40000
# x = 2000
# p = 50
# v = 15
# f = 10000
# s = 40000
variableCost = 0
fixedCost = 0
#price = 32000
price = 40347
demand = 1
salvageValue = 31000
workingCapital = 0
pcf = ProjectCashFlow(duration, MARR, investmentCapital, nMACRS, salvageValue, taxRate)
print pcf.getDepreciation(duration, nMACRS, investmentCapital)
#print pcf.getRevenue(duration, price, demand)
#print pcf.getNetIncome(taxRate, duration, nMACRS, investmentCapital, price, demand, variableCost, fixedCost)
ncf = pcf.getNetCashFlow(taxRate, duration, nMACRS, investmentCapital, price, demand, variableCost, fixedCost, salvageValue, workingCapital)
print ncf
pv = pcf.getPresentValue(ncf, MARR)
npv = pcf.getNPV(pv)


# for k in change:
#         price = p 
#         demand = x 
#         variableCost = v 
#         fixedCost = f 
#         salvageValue = s * (1 + k)
#         
#         pcf = ProjectCashFlow(duration, nMACRS, taxRate, MARR,
#                  investmentCapital, demand, price, variableCost, fixedCost, salvageValue)
#         ncf = pcf.getNetCashFlow(taxRate, duration, nMACRS, investmentCapital, price, demand, variableCost, fixedCost, salvageValue)
#         pv = pcf.getPresentValue(ncf, MARR)
#         npv = pcf.getNPV(pv)
#         print "{k:2d}%: \t {v:9d}".format(k=int(k*100), v=int(npv))