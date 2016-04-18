'''
Created on Apr 17, 2016

@author: XING
'''
from math import floor

class Depreciation(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def depreciationStraightLine(self, capitalInvestment, salvageValue, lifeYear):
        bv = capitalInvestment
        dep = (capitalInvestment - salvageValue) * 1.0 / lifeYear
        bookValue = [bv]
        depreciation = [0]
        for i in range(lifeYear):
            bv = bv - dep
            depreciation.append(dep)
            bookValue.append(bv)
        return depreciation, bookValue
    
    def depreciationDecliningBalance(self, capitalInvestment, salvageValue, lifeYear, multiplier = 2, rounding = 4):
        alpha = multiplier * 1.0 / lifeYear
        dep = capitalInvestment * alpha # 1st year depreciation
        bv = capitalInvestment - dep
        bookValue = [capitalInvestment, bv]
        depreciation = [0, dep]
        slFlag = False
        overFlag = False
        for i in range(1, lifeYear):
            if overFlag:
                dep = 0
            else:
                slDep = (bv - salvageValue) / (lifeYear - i)
                if (slFlag == False):
                    #dep = capitalInvestment * alpha * (1 - alpha)**i
                    dep = bv * alpha
                    if (dep <= slDep):
                        slFlag = True
                        dep = slDep
                else: # Switch to Straight Line Depreciation Method
                    dep = slDep
                if (bv - dep <= salvageValue):
                    dep = bv - salvageValue
                    bv = salvageValue
                    overFlag = True
                else:
                    bv = bv - dep
            depreciation.append(round(dep, rounding))
            bookValue.append(round(bv, rounding))
        return depreciation, bookValue
        
    def getMACRS(self, n, rounding = 4):
        if (n < 15):
            alpha = 2.0 / n
        else:
            alpha = 1.5 / n
        depreciationKthYear = round(alpha / 2.0, rounding)
        depreciation = [0, depreciationKthYear]
        bv = 1.0 - depreciationKthYear
        slFlag = False
        overFlag = False
        k = 0.5
        while (k < n):
            if overFlag:
                depreciationKthYear = 0
                #k = k + 1.0    
            else:
                slDep = bv / (n - k)
                if (slFlag == False):
                    depreciationKthYear = alpha * bv
                    if (depreciationKthYear <= slDep):
                        slFlag = True
                        depreciationKthYear = slDep
                else: # Switch to Straight Line Depreciation Method
                    depreciationKthYear = slDep
                if (k > n - 1):
                    depreciationKthYear = depreciationKthYear / 2.0
                if (bv - depreciationKthYear <= 0):
                    depreciationKthYear = bv
                    bv = 0
                    overFlag = True
                else:
                    bv = bv - depreciationKthYear
            k = k + 1
            depreciation.append(round(depreciationKthYear, rounding))
        return depreciation

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
    
    def getMACRSRealProperty(self, N, startingMonth = 1, n = None, rounding = 6):
        if (n == None):
            n = N
        k = (13 - startingMonth - 0.5) / 12   # Half-Month convention
        annualDepreciation = 1.0 / N
        depreciation = [0, round(k * annualDepreciation, rounding)]
        k = k + 1
        while (k < N + 1):
            k = k + 1
            if (k < n + 1):
                depreciation.append(round(annualDepreciation, rounding)) 
            else:
                numMonthsLastYear = (startingMonth - 0.5)/12 + n - floor(n)
                if (numMonthsLastYear > 1):
                    numMonthsLastYear = numMonthsLastYear - 1
                depreciation.append(round(numMonthsLastYear * annualDepreciation, rounding))
                break
        return depreciation
    
I = 39000
N = 8
S = 8000
tryDep = Depreciation()
#print [322000 * x for x in [0, .1429, .2449, .1749, .1249, .0893, .0892, .0893, .0446]]
print tryDep.depreciationStraightLine(I, S, N)
#print tryDep.depreciationDecliningBalance(I, S, N)
print tryDep.getMACRS(7)
print [I * x for x in tryDep.getMACRS(5)]
n = 3 + 5.0/12#
print tryDep.getMACRSRealProperty(27.5, 6)
print len(tryDep.getMACRSRealProperty(27.5, 6))
print tryDep.depreciationMACRS(7, duration=13) 