import numpy
import math
import time
import sys
import os
import copy

from . import core
from . import lib

def main():
    parametersA = core.Parameters(priceASIC= 10.0, hashrateASIC= 100.0, energyASIC= 10.0, optionEOS= False)
    parametersB = core.Parameters(priceASIC= 10.0, hashrateASIC= 100.0, energyASIC= 20.0, optionEOS= False)
    parametersC = core.Parameters(priceASIC= 10.0, hashrateASIC= 100.0, energyASIC= 30.0, optionEOS= False)
    parametersD = core.Parameters(priceASIC= 10.0, hashrateASIC= 100.0, energyASIC= 50.0, optionEOS= False)
    parameters = [parametersA, parametersB, parametersC, parametersD]
    numberOfUsers = 1000
    initialBudgetMean = 500.0
    maximumUpdateDuration = 100
    maximumBlockCounter = 4000
    datadirpath = os.path.join(os.getcwd(), "data")
    try:
        if not os.path.exists(datadirpath):
            os.makedirs(datadirpath)
    except OSError:
        print("Error: Failed to create the directory.")

    for cnt_sim in range(len(parameters)):
        fileNameSeparator = str(cnt_sim)
        parameterFileName = "parameter"+ fileNameSeparator + ".txt"
        fileParameters = open(os.path.join(datadirpath, parameterFileName), mode="w")
        stdout = sys.stdout
        sys.stdout = fileParameters
        parameters[cnt_sim].print()
        fileParameters.close()
        sys.stdout = stdout

        # Generate Users for parameters
        UserA = lib.generateMultipleUsers(parameters[cnt_sim], numberOfUsers, initialBudgetMean, maximumUpdateDuration)
        # Single simulation for parameters
        [userSnapshot, DRHistory, PIHistory, CVHistory, winnerIndexHistory] = singleSimulation(parameters[cnt_sim],UserA,maximumBlockCounter)
        # Write the result in the file
        DRstr = list(map(str, DRHistory))
        PIstr = list(map(str, PIHistory))
        CVstr = list(map(str, CVHistory))

        resultFileName = "result" + fileNameSeparator + ".txt"
        fileResults = open(os.path.join(datadirpath, resultFileName), mode="w")
        fileResults.write("DRHistory \n")
        fileResults.writelines("\t".join(DRstr))
        fileResults.write("\nPIHistory \n")
        fileResults.writelines("\t".join(PIstr))
        fileResults.write("\nCVHistory \n")
        fileResults.writelines("\t".join(CVstr))
        fileResults.write("\n")
        fileResults.close()

        snapshotFileName = "snapshot" + fileNameSeparator + ".txt"
        fileSnapshots = open(os.path.join(datadirpath, snapshotFileName), mode="w")
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
