import math

class Parameters:
    def __init__(self, priceASIC = 10.0, hashrateASIC = 10.0, energyASIC = 1.0, 
    hashrateGPP = 1.0, energyGPP = 1.0, 
    blockReward = 100.0, energyPrice = 0.0002, optionEOS = True):
        self.priceASIC = priceASIC
        self.hashrateASIC = hashrateASIC
        self.energyASIC = energyASIC
        self.hashrateGPP = hashrateGPP
        self.energyGPP = energyGPP
        self.blockReward = blockReward
        self.energyPrice = energyPrice
        self.optionEOS = optionEOS
    def __repr__(self):
        return "Parameter class object"
    def print(self):
        print("AISC parameters: ", "\n\t", "Price: ",self.priceASIC, ", Hashrate: ", self.hashrateASIC, ", Energy: ", self.energyASIC)
        print("GPP parameters: ", "\n\t", "Hashrate: ", self.hashrateGPP, ", Energy: ", self.energyGPP)
        print("Environment parameters: ", "\n\t", "Block rewards: ", self.blockReward, ", Energy Price: ", self.energyPrice, ", EOS option:", self.optionEOS)

class User:
    """ State of a user
    """
    def __init__(self, parameters, rng, initialBudgetMean = 500.0, maximumUpdateDuration = 10):
        self.budget = rng.exponential(initialBudgetMean) # exponential random
        self.updateDuration = rng.integers(low = 1, high = maximumUpdateDuration, endpoint = True) # random
        self.updateCounter = rng.integers(low = 0, high = self.updateDuration - 1, endpoint = True)
        self.profitRatioThreshold = rng.random() /2.5 + 0.1 # 0.1 ~ 0.5
        self.rationality = rng.random() / 10
        self.numberASIC = math.ceil(self.budget / parameters.priceASIC)
        self.profit = 0.0
        self.profitRatio = 0.0
        self.energyPriceEffective = parameters.energyPrice
        self.role = "um" # um for miner, u0 for non-miner
        self.device = "ASIC+GPP"
        self.updateHashrate(parameters)

    def computeEnergyPriceEffective(self, parameters, energyConsumption):
        return parameters.energyPrice / (1 + math.log10(energyConsumption)/10.0)

    def updateHashrate(self, parameters):
        if self.role == "um":
            self.hashrate = 1.0 + parameters.hashrateASIC * self.numberASIC
        else:
            self.hashrate = 0.0

    def computeProfitRatio(self, networkHashrate, parameters, includeGPP):
        profit = self.computeProfit(networkHashrate, parameters, includeGPP)
        profitRatio = profit / self.computeEnergyCost(parameters, includeGPP)
        return profitRatio

    def computeProfit(self, networkHashrate, parameters, includeGPP):
        currentHashrate = self.hashrate
        newHashrate = parameters.hashrateASIC * self.numberASIC
        newHashrate = newHashrate + 1.0 if includeGPP else newHashrate
        probMine = newHashrate / (networkHashrate - currentHashrate + newHashrate)
        energyCost = self.computeEnergyCost(parameters, includeGPP)
        expectedReward = parameters.blockReward * probMine
        profit = expectedReward - energyCost
        return profit

    def computeEnergyCost(self, parameters, includeGPP):
        energyConsume = parameters.energyASIC * self.numberASIC
        energyConsume = energyConsume + 1.0 if includeGPP else energyConsume
        self.energyPriceEffective = self.computeEnergyPriceEffective(parameters, energyConsume) if parameters.optionEOS else parameters.energyPrice
        energyCost = self.energyPriceEffective * energyConsume
        return energyCost

    def positionUpdate(self, networkHashrate, parameters):
        self.updateCounter += 1
        if self.updateCounter >= self.updateDuration :
            self.numberASIC = math.ceil(self.budget / parameters.priceASIC)
            profitRatioIncludeGPP = self.computeProfitRatio(networkHashrate, parameters, True)
            profitRatioOnlyASIC = self.computeProfitRatio(networkHashrate, parameters, False)
            if profitRatioIncludeGPP > profitRatioOnlyASIC:
                self.profitRatio = profitRatioIncludeGPP
                self.profit = self.computeProfit(networkHashrate, parameters, True)
                self.device = "ASIC+GPP"
            else:
                self.profitRatio = profitRatioOnlyASIC
                self.profit = self.computeProfit(networkHashrate, parameters, False)
                self.device = "ASIC"

            if self.profitRatio < self.profitRatioThreshold :
                self.profitRatio = 0.0
                self.profit = 0.0
                self.role = "u0"
            else:
                self.role = "um"
            self.updateHashrate(parameters)
            self.updateCounter = 0

    def __repr__(self):
        return "User class object"
    def print(self):
        temp = []
        temp.append("budget: " + str(self.budget))
        temp.append("role: " + str(self.role))
        temp.append("device: " + str(self.device))
        temp.append("hashrate: " + str(self.hashrate))
        temp.append("profit: " + str(self.profit))
        temp.append("profitRatio: " + str(self.profitRatio))
        temp.append("energyPriceEffective: " + str(self.energyPriceEffective))
        temp.append("numberASIC: " + str(self.numberASIC))
        temp.append("updateDuration: " + str(self.updateDuration))
        temp.append("updateCounter: " + str(self.updateCounter))
        temp.append("profitRatioThreshold: " + str(self.profitRatioThreshold))
        temp.append("rationality: " + str(self.rationality))
        printString = ", ".join(temp)
        print(printString)

    
