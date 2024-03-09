import unittest
import re
import sys
import io

a="""
def smallest_num(a,b,c):
    num1=a
    num2=b
    num3=c
    smallest = 0
    if num1 <= num2 and num1 <= num3:
        smallest = num1
    if num2 <= num1 and num2 <= num3:
        smallest = num2
    if num3 <= num1 and num3 <= num2:
        smallest = num3
    return smallest
"""
exec(a) 

class TestSmallestNum(unittest.TestCase):
    def test_all_positive(self):
        self.assertEqual(smallest_num(1, 2, 3), 1)

    def test_all_negative(self):
        self.assertEqual(smallest_num(-1, -2, -3), -3)

    def test_mixed_signs(self):
        self.assertEqual(smallest_num(-1, 2, 3), -1)

    def test_zero_included(self):
        self.assertEqual(smallest_num(0, 1, 2), 0)

    def test_all_zeros(self):
        self.assertEqual(smallest_num(0, 0, 0), 0)

    def test_all_same(self):
        self.assertEqual(smallest_num(2, 2, 2), 2)

    def test_two_smallest_same(self):
        self.assertEqual(smallest_num(2, 2, 3), 2)

    def test_floats(self):
        self.assertEqual(smallest_num(1.5, 2.5, 0.5), 0.5)

    def test_with_large_numbers(self):
        self.assertEqual(smallest_num(100000, 200000, 300000), 100000)

    def test_with_small_and_large(self):
        self.assertEqual(smallest_num(-100000, 200000, 300000), -100000)


def capture():
    # Redirect stdout to capture the test runner's output
    old_stdout = sys.stdout  # Backup the original stdout
    sys.stdout = buffer = io.StringIO()

    # Load and run the tests
    test_loader = unittest.TestLoader()
    test = test_loader.loadTestsFromTestCase(TestSmallestNum)
    run_test = unittest.TextTestRunner(stream=sys.stdout)
    run_test.run(test)

    # Restore stdout
    sys.stdout = old_stdout

    # Extract the captured output from the buffer
    captured_output = buffer.getvalue()
    print("Captured Output:\n", captured_output)

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