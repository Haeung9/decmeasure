import numpy
import math
import time
import os
import copy

from . import core
from . import lib

def main():
    parameters = core.Parameters()
    numberOfUsers = 1000
    initialBudgetMean = 500.0
    maximumUpdateDuration = 100
    maximumBlockCounter = 10000
    # [DR, PI, CV, userSnapshot] = singleSimulation(parameters, numberOfUsers, initialBudgetMean, maximumUpdateDuration, maximumBlockCounter)
    # target = []
    # for i in range(len(userSnapshot)):
    #     target.append(userSnapshot[i][-1].budget)
    # print(target)
    # print(userSnapshot[0][-1].profitRatioThreshold)

    # DRstr = list(map(str, DR))
    # PIstr = list(map(str, PI))
    # CVstr = list(map(str, CV))
    # file = open(os.path.join(os.getcwd(), "parameter1.txt"), mode="w")
    # file.writelines("\t".join(DRstr))
    # file.write("\n")
    # file.writelines("\t".join(PIstr))
    # file.write("\n")
    # file.writelines("\t".join(CVstr))
    # file.close()


def singleSimulation(parameters = core.Parameters(), Users = lib.generateMultipleUsers(core.Parameters(), 1000), maximumBlockCounter = 1000):
    DRHistory = [] # dropout ratio
    PIHistory = [] # polarization index
    CVHistory = [] # collusion vulnerability
    winnerIndexHistory = [] # winner history
    userSnapshot = []
    
    for blockCounter in range(maximumBlockCounter):
        # After a block
        [Users, DR, PI, CV, winnerIndex] = progressOneBlock(parameters, Users)
        
        # Archive history
        DRHistory.append(copy.deepcopy(DR))
        PIHistory.append(copy.deepcopy(PI))
        CVHistory.append(copy.deepcopy(CV))
        winnerIndexHistory.append(winnerIndex)

        # Take a snapshot
        if blockCounter % round(maximumBlockCounter/10) == 0:
            userSnapshot.append(copy.deepcopy(Users))
    
    return [userSnapshot, DRHistory, PIHistory, CVHistory, winnerIndexHistory]

def progressOneBlock(parameters, Users):
    # A block mining
    winnerIndex = lib.randomMining(Users)
    Users[winnerIndex].budget += parameters.blockReward

    # Update users' positions
    networkHashrate = lib.computeNetworkHashrate(Users)
    for i in range(len(Users)):
        Users[i].positionUpdate(networkHashrate, parameters)

    # Compute centralization
    DR = lib.computeDropoutRatio(Users)
    PI = lib.computePolarizationIndex(Users)
    CV = lib.computeCollusionVulnerability(Users)

    return [Users, DR, PI, CV, winnerIndex]

def comparisonSimulation():
    pass


if __name__ == "__main__":
    main()
