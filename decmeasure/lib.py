import numpy
import math
import time
from bisect import bisect_right

from . import core

def generateMultipleUsers(parameters, numberOfUsers, initialBudgetMean = 500.0, maximumUpdateDuration = 100, rng = numpy.random.default_rng(round(time.time()))):
    Users = []
    for i in range(numberOfUsers): # initialize multiple users
        Users.append(core.User(parameters, rng, initialBudgetMean, maximumUpdateDuration))
    return Users

def randomMining(Users, rng = numpy.random.default_rng(round(time.time()))):
    networkHashrate = computeNetworkHashrate(Users)
    miningCMF = [Users[0].hashrate/networkHashrate] * len(Users)
    for i in range(len(Users)-1):
        miningPMF = Users[i+1].hashrate / networkHashrate
        miningCMF[i+1] = miningCMF[i] + miningPMF
    randomNumber = rng.random()
    winnerIndex = bisect_right(miningCMF,randomNumber)
    return winnerIndex

def computeDropoutRatio(Users):
    numberOfUsers = len(Users)
    numberOfDroppedOut = 0
    for i in range(numberOfUsers):
        if Users[i].role == "u0":
            numberOfDroppedOut += 1
    return numberOfDroppedOut / numberOfUsers

def computePolarizationIndex(Users):
    numberOfUsers = len(Users)
    numberOfUpperClass = math.ceil(numberOfUsers/10)
    hashrate = sortedHashrate(Users, True)
    upperClassHashrate = 0
    networkHashrate = computeNetworkHashrate(Users)
    for i in range(numberOfUpperClass):
        upperClassHashrate += hashrate[i]
    return upperClassHashrate / networkHashrate

def computeCollusionVulnerability(Users):
    hashrate = sortedHashrate(Users, True)
    numberOfUpperClass = 0
    upperClassHashrate = 0
    networkHashrate = computeNetworkHashrate(Users)
    while (upperClassHashrate/networkHashrate) <= 0.5:
        upperClassHashrate += hashrate[numberOfUpperClass]
        numberOfUpperClass += 1
    return 1 - numberOfUpperClass/len(Users)

def sortedHashrate(Users, reverseFlag = False):
    sorted = []
    for i in range(len(Users)):
        sorted.append(Users[i].hashrate)
    sorted.sort(reverse=reverseFlag)
    return sorted

def computeNetworkHashrate(Users):
    networkHashrate = 0.0
    for i in range(len(Users)):
        networkHashrate += Users[i].hashrate
    return networkHashrate
