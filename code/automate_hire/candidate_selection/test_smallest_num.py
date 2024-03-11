import unittest

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


if __name__ == '__main__':
    unittest.main()