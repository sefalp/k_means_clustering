#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 08:59:23 2020

@author: sefa
"""

import numpy as np
import random
import math
import pandas as pd
import matplotlib.pyplot as plt

#Chooses random dots in dataset for the first step of algorithm
def randomDots(data,dotNum):
    lengthOfData = len(data)
    randomDots = []
    i = 0
    while(i < dotNum):
        ra = random.randint(0,lengthOfData)
        if(ra not in randomDots):
            randomDots.append(ra)
            i = i+1
    for no,y in enumerate(randomDots):
        randomDots[no] = data[y]
        data[y][2] = no
    return randomDots

# finds average point in clusters for cluster update
def averagePoint(array):
    firstSum = 0
    secondSum = 0
    for i in array:
        firstSum += i[0]
        secondSum += i[1]
    firstAv = float("{0:.2f}".format(firstSum/len(array)))
    secondAv = float("{0:.2f}".format(secondSum/len(array)))
    return [firstAv,secondAv]

# Euclidean distance finder function
def findDistance(element1,element2):
    result = math.sqrt((float(element1[0])-float(element2[0]))**2 + (float(element1[1])-float(element2[1]))**2)
    return result

# Gives label to the data according to its nearest cluster point
def labeledData(data,dotArray):
    dist = 999
    for dot in dotArray:
        distance = findDistance(data,dot)
        if(distance < dist):
            dist = distance
            data[2] = dot[2]
    return data

# gives  new label(cluster) to the all data elements.
def newClusters(Dataset,dotArray):
    setData = []
    for data in Dataset:
        dat = labeledData(data,dotArray)
        setData.append(dat)
    return setData

# Finds total cluster change to know when the algorithm will be terminated
def totalClusterPositionChange(newArray,oldArray,k):
    totalDist = 0
    for i in range (k):
        totalDist = totalDist + findDistance(newArray[i],oldArray[i])
    return totalDist

# Plotter function to plot k means clusters as dot graph
def plotter(Dataset,clusters):
    df = pd.DataFrame(Dataset)
    colors = ['red', 'gray', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown']
    df[2] = df[2].astype(int)
    classlbl = df[2]
    
    df_c = pd.DataFrame(clusters)

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111)

    colors = np.asarray(colors)
    colorslist = colors[classlbl]
    

    for x, y, c in zip(df[0], df[1], colorslist):
        ax.scatter(x, y, color=c, cmap='viridis', alpha=0.5)

    for x, y in zip(df_c[0], df_c[1]):
        ax.scatter(x, y, color='black', cmap='viridis', alpha=1)

    return plt.show()

# Finds objective function for any iteration to see success of the algorithm and compare with other iterations
def objectiveFunction(Dataset,dots):
    objectiveFuncValue = 0
    for i in range(len(dots)):
        arr = []
        for data in Dataset:
            if(data[2] == i):
                arr.append(data)
        for dot in arr:
            objectiveFuncValue = objectiveFuncValue + findDistance(dot,dots[i])
    return objectiveFuncValue
#Plots objective function as line graph to see algorithms process according to iteration number 
def lineGraphPlot(Dataset):
    plt.plot(range(len(Dataset)),Dataset,'o-')
    plt.title('Objective Function Plot')
    plt.xlabel("iteration number")
    plt.ylabel("objective function value")
    
    
def getDatasetandClusterNum():
    a = input("Which dataset do you want to use : {} , {} or {}".format(1,2,3))
    if(a == 1):
        data = "data1.txt"
    elif(a == 2):
        data = "data2.txt"
    else:
        data= "data3.txt"
    clusterNum = input("How many clusters you need to seperate data ? ")
    return data,clusterNum

"""
def meanDistance(element,array):
    totalDist = 0
    for arr in array:
        totalDist = totalDist + findDistance(element,array)
    return totalDist/len(array)
"""

# Main function 
def k_means_clustering(dataset,k):
    
    #gets datas from file and puts them into array for processing.
    f = open(dataset, "r")
    Dataset = []
    num_lines = sum(1 for line in open('data1.txt'))
    for i in range(num_lines):
        x = f.readline().split(",")
        x = np.array(x)
        y = x.astype(np.float)
        y[2] = 0
        Dataset.append(y)
    
    
    objectiveFunctionArray = []
    clustArray = []
    totalDist = 999
    #First clusters choosed randomly and data seperated according to closest clusters
    dots = randomDots(Dataset,k)
    Dataset = newClusters(Dataset,dots)
    plotter(Dataset,dots)
    objectiveFunctionArray.append(objectiveFunction(Dataset,dots))
    clustArray.append(dots)
    
    # totalDist defines total distance change between last two iterations thus algorithm knows when to stop. 
    while(totalDist > 0.0001):
        clusters = []
        for i in range(len(dots)):
            arr = []
            for data in Dataset:
                # datas seperated according to their label and average point obtains to new cluster update
                if(data[2] == i):
                    arr.append(data)
            average = averagePoint(arr)
            average.append(i)
            clusters.append(average)
        # Average points of clusters updated as new cluster point  
        clustArray.append(clusters)
        totalDist = totalClusterPositionChange(clustArray[-1],clustArray[-2],k)
        # According to new cluster points, cluesters updated
        Dataset = newClusters(Dataset,clustArray[-1])
        objectiveFunctionArray.append(objectiveFunction(Dataset,clustArray[-1]))
    plotter(Dataset,clustArray[-1])
    lineGraphPlot(objectiveFunctionArray)
    print("Final objective function value is {}".format(objectiveFunctionArray[-1]))
    print("Total itearation count is {}".format(len(objectiveFunctionArray)))
    

dataset,clusterNum = getDatasetandClusterNum()
k_means_clustering(dataset,clusterNum)






