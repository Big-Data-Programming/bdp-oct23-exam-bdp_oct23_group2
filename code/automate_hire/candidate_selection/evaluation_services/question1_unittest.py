import unittest


a="""
def fact(n):  
    return 1 if (n==1 or n==0) else n * fact(n - 1); 
"""

exec(a)

class TestFactorialFunction(unittest.TestCase):
    def test_factorial_of_zero(self):
        self.assertEqual(fact(0), 1)

    def test_factorial_of_one(self):
        self.assertEqual(fact(1), 1)

    def test_factorial_of_two(self):
        self.assertEqual(fact(2), 2)

    def test_factorial_of_three(self):
        self.assertEqual(fact(3), 6)

    def test_factorial_of_four(self):
        self.assertEqual(fact(4), 24)

    def test_factorial_of_five(self):
        self.assertEqual(fact(5), 120)

    def test_factorial_of_six(self):
        self.assertEqual(fact(6), 720)

    def test_factorial_of_seven(self):
        self.assertEqual(fact(7), 5040)

    def test_factorial_of_ten(self):
        self.assertEqual(fact(10), 3628800)

    # def test_factorial_of_hell(self):
    #     self.assertEqual(fact(-1), -1)

    def test_negative_input(self):
        with self.assertRaises(RecursionError):
            fact(-1)

if __name__ == '__main__':
    unittest.main()