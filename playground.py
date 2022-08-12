import os
import sys
import math
import time

import numpy

from decmeasure import core, lib, simulation

# def main():
#     parameters = core.Parameters()
#     Users = lib.generateMultipleUsers(parameters, 11)
#     Threshold = math.ceil(len(Users) / 10)
#     budget = []
#     for i in range(len(Users)):
#         budget.append(Users[i].budget)
#     print(budget)
#     budget.sort(reverse=True)
#     print(budget)
#     print(Threshold)
#     budgetTopTen = budget[:Threshold]
#     print(budgetTopTen)


if __name__ == "__main__":
    simulation.main()