import os
import sys
import unittest
import numpy
import math
import copy

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from decmeasure import core, lib, simulation

class SimulationTest(unittest.TestCase):
    def test_progressOneBlock(self):
        print("\n","--", sys._getframe(0).f_code.co_name)
        #
        rng = numpy.random.default_rng(555)
        SettingA = core.Parameters()
        numberOfUsers = 10

        # Generate users
        Users = lib.generateMultipleUsers(SettingA, numberOfUsers, rng=rng)
        previousUsers = copy.deepcopy(Users)

        # progress a block
        [Users, DR, PI, CV, winnerIndex] = simulation.progressOneBlock(SettingA, Users)

        # winner's budget changes
        previous = previousUsers[winnerIndex].budget
        updated = Users[winnerIndex].budget

        print("winnerbudget--> ", "previous: ", previous, ", updated: ", updated)
        self.assertNotEqual(previous, updated)
    
    def test_singleSimulation(self):
        print("\n","--", sys._getframe(0).f_code.co_name)
        rng = numpy.random.default_rng(555)
        SettingA = core.Parameters()
        numberOfUsers = 10
        Users = lib.generateMultipleUsers(SettingA, numberOfUsers, maximumUpdateDuration = 2 ,rng=rng)
        [userSnapshot, DRHistory, PIHistory, CVHistory, winnerIndexHistory] = simulation.singleSimulation(SettingA, Users, maximumBlockCounter = 20)
        print(PIHistory)
        print(winnerIndexHistory)
        print("blockReward: ", SettingA.blockReward, ", priceASIC: ", SettingA.priceASIC)
        print("*user[0] initial: ")
        userSnapshot[0][0].print()
        print("*user[0] final: ")
        userSnapshot[-1][0].print()
        pass

if __name__ == "__main__":
    unittest.main()