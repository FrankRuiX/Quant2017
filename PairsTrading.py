#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 15:36:03 2019

@author: frank
"""

import numpy as np
import pandas as pd
import itertools as it

""" Function for calculating the tracking variance
    among all selected the candidates 
    Assume the import data are returns 
    and they are same length """
def trackingVariance(x,y):
    percentage = 100
    length = len(x)
    
    priceX = np.ones(length) ###Normalized the Price
    priceY = np.ones(length)
    
    for i in range(1, length):
        priceX[i] = priceX[i - 1] * (1 + x[i]/percentage)
        priceY[i] = priceY[i - 1] * (1 + y[i]/percentage)
    
    return ((priceX - priceY).T).dot(priceX - priceY)

""" Function for Tracking Trading Signal 
    when i th is 0 and i + 1 th is 1 Open Position
    """
def signalOpen(x, y, benchmark):
    return [indicator(diff, benchmark) for diff in (x - y)]
    
""" Function for Determining the Open Position """
def indicator(num1, num2):
    threshold = 2
    if abs(num1) > threshold * abs(num2):
        return 1
    return 0
    

data = pd.read_excel("data.xlsx")
data = data.dropna(axis = 1)
data.index = [pd.to_datetime(date) for date in data['TICKER']]
data = data.drop('TICKER', axis = 1)
pairList = list(it.combinations(data.keys(), 2))

numOfTrain = 250
trainData = data.iloc[:numOfTrain, :]
trackingVarList = [trackingVariance(trainData[j[0]],trainData[j[1]])
                   for j in pairList]

""" Find the top 10 minimum tracking variance as pairs """
selectedNum = 10
selectedPairs = np.argsort(trackingVarList)[0:selectedNum]
pickedTicker = [pairList[i] for i in selectedPairs]

""" Testing """
testData = data.iloc[numOfTrain:, :]
testNum = 0 ### just selected the first pair
testPair1 = testData[[pickedTicker[testNum][0],pickedTicker[testNum][1]]]
benchmark1 = trackingVarList[selectedPairs[testNum]]
signaList = signalOpen(testPair1.iloc[:,0], testPair1.iloc[:,1], benchmark1)

