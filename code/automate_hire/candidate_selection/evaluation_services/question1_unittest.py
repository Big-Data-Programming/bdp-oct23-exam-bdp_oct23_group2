import unittest
import re
import sys
import io

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

def capture():
    # Redirect stdout to capture the test runner's output
    old_stdout = sys.stdout  # Backup the original stdout
    sys.stdout = buffer = io.StringIO()

    # Load and run the tests
    test_loader = unittest.TestLoader()
    test = test_loader.loadTestsFromTestCase(TestFactorialFunction)
    run_test = unittest.TextTestRunner(stream=sys.stdout)
    run_test.run(test)

    # Restore stdout
    sys.stdout = old_stdout

    # Extract the captured output from the buffer
    captured_output = buffer.getvalue()
    # print("Captured Output:\n", captured_output)

    #Saving Runtime
    pattern_one = r"Ran \d+ tests in ([\d.]+)s"
    match_1 = re.search(pattern_one, captured_output)
    if match_1:
        time_taken = match_1.group(1)
        print(f"Time taken to run the tests: {time_taken}s")
    else:
        print("Time taken to run the tests not found.")

    #Saving number of test failed
    pattern_two=r"failures=([\d]+)"
    match_2=re.search(pattern_two, captured_output)
    if match_2:
        test_failed=match_2.group(1)
        print(f"No. of test cases failed: {test_failed}")
    else:
        print("No. of test failed: 0")

if __name__ == '__main__':
    capture()
