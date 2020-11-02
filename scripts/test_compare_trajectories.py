import unittest
from collections import Counter        

from compare_trajectories import get_similarity, VERY


class TestCompareTrajectories(unittest.TestCase):
    code_str = 'ctr = 0\nfor i in s:\n    if(i == "a" or i == "i" or i == "o" or i =="e" or i == "u"):\n        ctr = ctr + 1\nprint ("Number of vowels:",ctr)\n'
    code_pset = '1-1'    

    def test_get_similarity(self) -> None:
        response = get_similarity(TestCompareTrajectories.code_str,
                                  TestCompareTrajectories.code_pset,
                                  subjective=False)
        expected_response = f"Your code is {VERY} similar to correct solutions submitted by other students in previous years."
        
        print(response)
        print(expected_response)

        self.assertTrue(response == expected_response)

if __name__ == '__main__':
    tester = TestCompareTrajectories()
    tester.test_get_similarity()
