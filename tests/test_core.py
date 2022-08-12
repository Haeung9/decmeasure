import os
import sys
import unittest
import numpy
import math
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from decmeasure import core

class CoreTest(unittest.TestCase):
    def test_parameters_setting(self):
        print ("\n","--",sys._getframe(0).f_code.co_name)
        # Test parameter setting
        SettingA = core.Parameters() # Set a default parameter set
        expected = 10.0
        evaluated = SettingA.priceASIC
        print("priceASIC--> ", "expected = ", expected, ", evaluated = ", evaluated)
        self.assertEqual(expected, evaluated)

        # Test parameter change
        SettingA.priceASIC = 12.0 # change a parameter
        expected = 12.0
        evaluated = SettingA.priceASIC
        print("priceASIC--> ", "expected = ", expected, ", evaluated = ", evaluated)
        self.assertEqual(expected, evaluated)

    def test_user_setting(self):
        print("\n","--", sys._getframe(0).f_code.co_name)

        # Test generate a user
        rng = numpy.random.default_rng(1)
        SettingA = core.Parameters()
        UserA = core.User(SettingA, rng) # initialize a user
        print("hashrate--> ", "expected = ", UserA.hashrate, ", NotEqual to = ", 0.0)
        self.assertNotEqual(UserA.hashrate, 0.0) 

    def test_multiple_user(self):
        print("\n","--", sys._getframe(0).f_code.co_name)

        # Test generate multiple users
        SettingA = core.Parameters()
        rng = numpy.random.default_rng(1)
        numberOfUsers = 1000
        Users = []
        for i in range(numberOfUsers): # initialize multiple users
            Users.append(core.User(SettingA, rng))
            # print("budget of user ", i, ": ", Users[i].budget)
        
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

if __name__ == "__main__":
    unittest.main()