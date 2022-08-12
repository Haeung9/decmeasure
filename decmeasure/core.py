import math

class Parameters:
    def __init__(self):
        self.priceASIC = 10.0
        self.hashrateASIC = 10.0
        self.energyASIC = 1.0
        self.hashrateGPP = 1.0
        self.energyGPP = 1.0
        self.blockReward = 100.0
        self.energyPrice = 0.001
        self.optionEOS = True
    def __repr__(self):
        return "Parameter class object"
    def print(self):
        print("AISC parameters: ", "\n\t", "Price: ",self.priceASIC, ", Hashrate: ", self.hashrateASIC, ", Energy: ", self.energyASIC)
        print("GPP parameters: ", "\n\t", "Hashrate: ", self.hashrateGPP, ", Energy: ", self.energyGPP)
        print("Environment parameters: ", "\n\t", "Block rewards: ", self.blockReward, ", Energy Price: ", self.energyPrice, ", EOS option:", self.optionEOS)

class User:
    def __init__(self, parameters, rng, initialBudgetMean = 500.0, maximumUpdateDuration = 100):
        self.budget = rng.exponential(initialBudgetMean) # exponential random
        self.updateDuration = rng.integers(low = 1, high = maximumUpdateDuration, endpoint = True) # random
        self.updateCounter = rng.integers(low = 0, high = self.updateDuration - 1, endpoint = True)
        self.profitRatioThreshold = rng.random() /10
        self.rationality = rng.random() / 10
        self.numberASIC = math.ceil(self.budget / parameters.priceASIC)
        self.profit = 0.0
        self.profitRatio = 0.0
        self.energyPriceEffective = parameters.energyPrice
        self.role = "um"
        self.device = "ASIC+GPP"
        self.updateHashrate(parameters)

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
        energyPrice = parameters.energyPrice
        energyPrice = energyPrice/(1.0 + math.log10(energyConsume)) if parameters.optionEOS else energyPrice
        energyCost = energyPrice * energyConsume
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

    
