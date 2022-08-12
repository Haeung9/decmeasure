import os
import sys
import unittest
import numpy
import math
from bisect import bisect_right
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from decmeasure import core, lib

class LibTest(unittest.TestCase):
    def test_generateMultipleUsers(self):
        print("\n","--", sys._getframe(0).f_code.co_name)

        # Test generate multiple users
        SettingA = core.Parameters()
        numberOfUsers = 1000
        Users = lib.generateMultipleUsers(SettingA, numberOfUsers)
   
        expected = numberOfUsers
        evaluated = len(Users) 
        print("numberOfUsers--> ", "expected: ", expected, ", evaluated: ", evaluated)
        self.assertEqual(expected, evaluated)

        expected = "um"
        evaluated = Users[numberOfUsers%10].role
        print("role of User ", numberOfUsers%10, "--> ", "expected = ", expected, ", evaluated = ", evaluated)
        self.assertEqual(expected, evaluated)

        expected = 500.0 # mean
        evaluated = 0.0 # sample mean
        for i in range(numberOfUsers):
            evaluated += Users[i].budget
        evaluated = evaluated / numberOfUsers

        stdev = 0.0 # sample standard deviation
        for i in range(numberOfUsers):
            stdev += abs(evaluated - Users[i].budget)
        stdev = stdev / numberOfUsers

        _delta = 1.96 * stdev/math.sqrt(numberOfUsers) # 95 % CI
        print("average budget--> ", "expected = ", expected, " +- ", _delta, ", evaluated = ", evaluated)
        self.assertAlmostEqual(expected, evaluated, delta=_delta)
    
    def test_computeNetworkHashrate(self):
        print("\n","--", sys._getframe(0).f_code.co_name)
        SettingA = core.Parameters()
        numberOfUsers = 10
        rng = numpy.random.default_rng(555)
        Users = lib.generateMultipleUsers(SettingA, numberOfUsers, rng=rng)
        hashrateTest = []
        expected = 0.0
        for i in range(len(Users)):
            hashrateTest.append(Users[i].hashrate)
            expected += Users[i].hashrate
        evaluated = lib.computeNetworkHashrate(Users)
        print("hashrate list--> ", hashrateTest)
        print("networkHashrate--> ", "expected = ", expected, ", evaluated = ", evaluated)
        self.assertEqual(expected, evaluated)
    
    def test_randomMining(self):
        print("\n","--", sys._getframe(0).f_code.co_name)
        SettingA = core.Parameters()
        numberOfUsers = 10
        rng = numpy.random.default_rng(555) # seed
        Users = lib.generateMultipleUsers(SettingA, numberOfUsers, rng=rng)
        # hashrateTest = [361.0, 111.0, 251.0, 41.0, 61.0, 431.0, 811.0, 371.0, 311.0, 171.0]
        # networkHashrateTest = 2920.0
        # miningPMFTest = [0.123630136986301, 0.038013698630137, 0.085958904109589, 0.014041095890411, 0.020890410958904, 0.147602739726027, 0.277739726027397, 0.127054794520548, 0.106506849315068, 0.058561643835616]
        miningCMFTest = [0.123630136986301, 0.161643835616438, 0.247602739726027, 0.261643835616438, 0.282534246575342, 0.430136986301370, 0.707876712328767, 0.834931506849315, 0.941438356164383, 1.0]
        randomNumberTest = 0.4870115645342946

        expected = bisect_right(miningCMFTest, randomNumberTest) # 6
        evaluated = lib.randomMining(Users, rng=rng)

        print("winnerIndex--> ","expected = ", expected, ", evaluated = ", evaluated )
        self.assertEqual(expected, evaluated)

if __name__ == "__main__":
    unittest.main()