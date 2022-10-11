import sys
import os
import copy
import time
import numpy

from . import core
from . import lib

def main():
    parametersA = core.Parameters(priceASIC= 10.0, hashrateASIC= 100.0, energyASIC= 10.0)
    parametersB = core.Parameters(priceASIC= 10.0, hashrateASIC= 80.0, energyASIC= 8.0)
    parametersC = core.Parameters(priceASIC= 10.0, hashrateASIC= 60.0, energyASIC= 6.0)
    parametersD = core.Parameters(priceASIC= 10.0, hashrateASIC= 40.0, energyASIC= 4.0)
    parameters = [parametersA, parametersB, parametersC, parametersD]
    numberOfUsers = 1000
    initialBudgetMean = 100.0
    maximumUpdateDuration = 10
    maximumBlockCounter = 4000
    seed = round(time.time())
    # save the random number generator seed for reproducibility
    datadirpath = os.path.join(os.getcwd(), "data")
    try:
        if not os.path.exists(datadirpath):
            os.makedirs(datadirpath)
    except OSError:
        print("Error: Failed to create the directory.")
    fileSeed = open(os.path.join(datadirpath, "randomSeed.txt"), mode="w")
    fileSeed.write(str(seed))
    fileSeed.close()

    for cnt_sim in range(len(parameters)):
        fileNameSeparator = str(cnt_sim)
        parameterFileName = "parameter"+ fileNameSeparator + ".txt"
        fileParameters = open(os.path.join(datadirpath, parameterFileName), mode="w")
        stdout = sys.stdout
        sys.stdout = fileParameters
        parameters[cnt_sim].print()
        fileParameters.close()
        sys.stdout = stdout
        rng = numpy.random.default_rng(seed)

        # Generate Users for parameters
        UserA = lib.generateMultipleUsers(parameters[cnt_sim], numberOfUsers, initialBudgetMean, maximumUpdateDuration, rng)
        # Single simulation for parameters
        [userSnapshot, DRHistory, PIHistory, CVHistory, winnerIndexHistory, networkHashrateHistory] = singleSimulation(parameters[cnt_sim],UserA,maximumBlockCounter)
        # Write the result in the file
        DRstr = list(map(str, DRHistory))
        PIstr = list(map(str, PIHistory))
        CVstr = list(map(str, CVHistory))
        HRstr = list(map(str,networkHashrateHistory))

        resultFileName = "result" + fileNameSeparator + ".csv"
        fileResults = open(os.path.join(datadirpath, resultFileName), mode="w")
        resultColumns = ["DRHistory", "PIHistory", "CVHistory", "HashrateHistory"]
        fileResults.write("\t".join(resultColumns))
        fileResults.write("\n")
        for i in range(len(DRstr)):
            fileResults.write(DRstr[i])
            fileResults.write("\t")
            fileResults.write(PIstr[i])
            fileResults.write("\t")
            fileResults.write(CVstr[i])
            fileResults.write("\t")
            fileResults.write(HRstr[i])
            fileResults.write("\n")
        fileResults.close()

        snapshotFileNamePrefix = "snapshot_forParameter" + fileNameSeparator
        for i in range(len(userSnapshot)):
            snapshotFileName = snapshotFileNamePrefix + "_No" + str(i) + ".csv"
            fileSnapshots = open(os.path.join(datadirpath, snapshotFileName), mode="w")
            columnString = userSnapshot[0][0].getColumns()
            fileSnapshots.write("\t".join(columnString))
            fileSnapshots.write("\n")
            for j in range(len(userSnapshot[i])):
                data = userSnapshot[i][j].getData()
                fileSnapshots.write("\t".join(data))
                fileSnapshots.write(":\n")
            fileSnapshots.close()


def singleSimulation(parameters = core.Parameters(), Users = lib.generateMultipleUsers(core.Parameters(), 1000), maximumBlockCounter = 1000):
    DRHistory = [] # dropout ratio
    PIHistory = [] # polarization index
    CVHistory = [] # collusion vulnerability
    winnerIndexHistory = [] # winner history
    networkHashrateHistory = []
    userSnapshot = []
    
    for blockCounter in range(maximumBlockCounter):
        # update users' states after mine a block
        [Users, DR, PI, CV, winnerIndex, networkHashrate] = progressOneBlock(parameters, Users)
        
        # Archive history
        DRHistory.append(copy.deepcopy(DR))
        PIHistory.append(copy.deepcopy(PI))
        CVHistory.append(copy.deepcopy(CV))
        networkHashrateHistory.append(copy.deepcopy(networkHashrate))
        winnerIndexHistory.append(winnerIndex)

        # Take a snapshot
        if blockCounter % round(maximumBlockCounter/10) == 0:
            userSnapshot.append(copy.deepcopy(Users))
    
    return [userSnapshot, DRHistory, PIHistory, CVHistory, winnerIndexHistory, networkHashrateHistory]

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

    return [Users, DR, PI, CV, winnerIndex, networkHashrate]

if __name__ == "__main__":
    main()
