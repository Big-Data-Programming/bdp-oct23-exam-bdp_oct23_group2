import unittest
import re
import sys
import io

a="""
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):  # Only check up to the square root of the number
        if number % i == 0:
            return False
    return True 
"""
exec(a)

class TestPrimeNum(unittest.TestCase):
    
    def test_negative_number(self):
        self.assertFalse(is_prime(-1), "Negative numbers are not prime.")

    def test_zero(self):
        self.assertFalse(is_prime(0), "0 is not prime.")

    def test_one(self):
        self.assertFalse(is_prime(1), "1 is not prime.")

    def test_smallest_prime(self):
        self.assertTrue(is_prime(2), "2 is prime.")

    def test_small_prime(self):
        self.assertTrue(is_prime(3), "3 is prime.")

    def test_even_non_prime(self):
        self.assertFalse(is_prime(4), "4 is not prime because it is divisible by 2.")

    def test_odd_non_prime(self):
        self.assertFalse(is_prime(9), "9 is not prime because it is divisible by 3.")

    def test_large_prime(self):
        self.assertTrue(is_prime(29), "29 is prime.")

    def test_large_non_prime(self):
        self.assertFalse(is_prime(35), "35 is not prime because it is divisible by 5 and 7.")

    def test_very_large_prime(self):
        self.assertTrue(is_prime(97),"97 is prime")

def capture():
    # Redirect stdout to capture the test runner's output
    old_stdout = sys.stdout  # Backup the original stdout
    sys.stdout = buffer = io.StringIO()

    # Load and run the tests
    test_loader = unittest.TestLoader()
    test = test_loader.loadTestsFromTestCase(TestPrimeNum)
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