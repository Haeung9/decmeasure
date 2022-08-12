import numpy
import math
import time
import sys
import os
import copy

from . import core
from . import lib

def main():
    parametersA = core.Parameters(priceASIC= 10.0)
    parametersB = core.Parameters(priceASIC= 20.0)
    parametersC = core.Parameters(priceASIC= 50.0)
    parametersD = core.Parameters(priceASIC= 100.0)
    numberOfUsers = 1000
    initialBudgetMean = 500.0
    maximumUpdateDuration = 100
    maximumBlockCounter = 1000
    datadirpath = os.path.join(os.getcwd(), "data")
    fileParameters = open(os.path.join(datadirpath, "parameterA.txt"), mode="w")
    stdout = sys.stdout
    sys.stdout = fileParameters
    parametersA.print()
    fileParameters.close()
    sys.stdout = stdout

    # Generate UsersA for parametersA
    UserA = lib.generateMultipleUsers(parametersA, numberOfUsers, initialBudgetMean, maximumUpdateDuration)
    # Single simulation for parametersA
    [userSnapshot, DRHistory, PIHistory, CVHistory, winnerIndexHistory] = singleSimulation(parametersA,UserA,maximumBlockCounter)
    # Write the result in the file
    DRstr = list(map(str, DRHistory))
    PIstr = list(map(str, PIHistory))
    CVstr = list(map(str, CVHistory))
    fileResults = open(os.path.join(datadirpath, "resultA.txt"), mode="w")
    fileResults.write("DRHistory \n")
    fileResults.writelines("\t".join(DRstr))
    fileResults.write("\nPIHistory \n")
    fileResults.writelines("\t".join(PIstr))
    fileResults.write("\nCVHistory \n")
    fileResults.writelines("\t".join(CVstr))
    fileResults.write("\n")
    fileResults.close()

    fileSnapshots = open(os.path.join(datadirpath, "snapshotA.txt"), mode="w")
    stdout = sys.stdout
    sys.stdout = fileSnapshots
    for i in range(len(userSnapshot)):
        fileSnapshots.write("Snapshot ")
        fileSnapshots.write(str(i))
        fileSnapshots.write(":\n")
        for j in range(numberOfUsers):
            userSnapshot[i][j].print()
    sys.stdout = stdout
    fileSnapshots.close()

    # Generate UsersB for parametersB
    pass
    # Single simulation for parametersB
    pass
    # Append the result in the file
    pass


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

if __name__ == "__main__":
    main()
