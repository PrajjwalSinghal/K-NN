#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 14:51:12 2019

@author: prajjwalsinghal
"""

 
import csv
import random
import math
import operator
 
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'r') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])
def LorentzianDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += math.log(1 + abs(instance1[x] - instance2[x]))
    return distance

def SoergelDistance(instance1, instance2, length):
    distance_max = 0
    distance_sub = 0
    for x in range(length):
        distance_sub += abs(instance1[x] - instance2[x])
        distance_max += max(instance1[x], instance2[x])
    return distance_sub/distance_max

def SorsenDistance(instance1, instance2, length):
    distance_sub = 0
    distance_sum = 0
    for x in range(length):
        distance_sub += abs(instance1[x] - instance2[x])
        distance_sum += abs(instance1[x] + instance2[x])
    return distance_sub/distance_sum

def ChebyshevDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        temp = abs(instance1[x] - instance2[x])
        distance = max(distance, temp) 
    return distance
def manhattanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += abs(instance1[x] - instance2[x])
    return distance
    
def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
 
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = LorentzianDistance(testInstance, trainingSet[x], length)
        #dist = SoregelDistance(testInstance, trainingSet[x], length)
        #dist = SorsenDistance(testInstance, trainingSet[x], length)
        #dist = ChebyshevDistance(testInstance, trainingSet[x], length)
        #dist = manhattanDistance(testInstance, trainingSet[x], length)
        #dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
 
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]
 
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0
	
def main():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('Iris.csv', split, trainingSet, testSet)
	# generate predictions
	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		#print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')
	
main()       
 

# Euclidean distance = Accuracy: 95.83333333333334%       
# manHattan distance = Accuracy: 97.67441860465115%
# ChebyshevDistance = Accuracy: 96.22641509433963%
# Sorsen Distance = Accuracy: 95.91836734693877%
# Soergel Distance = Accuracy: 98.14814814814815%
# Lorentzian Distance = Accuracy: 93.02325581395348%
        
        
        
        