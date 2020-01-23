"""


Given a positive integer n, find the least number of perfect square numbers (for example, 1, 4, 9, 16, ...) which sum to n.

Example 1:

Input: n = 12
Output: 3
Explanation: 12 = 4 + 4 + 4.
Example 2:

Input: n = 13
Output: 2
Explanation: 13 = 4 + 9.
"""
import unittest


class PerfectSquares:
    def __init__(self, n):
        """
        :param n: int
        """
        self.n = n

    def dp_solution(self):
        # initialize dp array to store sum of squares needed.
        # array will be 1-index
        if self.n == 0:
            return 0

        dp = [0 for i in range(self.n + 1)]

        # At each "perfect square index", ex: 4 = 2^2 or 9 = 3^3, dp[i] = 1 because only 1 perfect square is needed.
        squares = [0]

        # prefill squares up to range n
        for j in range(self.n + 1):
            if j * j <= self.n:
                squares.append(j * j)

        i = 1
        while i <= self.n:
            min_val = self.n

            for sq in squares:
                if sq == 0 or sq > i:
                    continue
                if sq == i:
                    dp[i] = 1
                    break
                else:
                    min_val = min(dp[sq] + dp[i - sq], min_val)
                    dp[i] = min_val
            i += 1
        return dp[self.n]


class TestPerfectSquares(unittest.TestCase):
    def setup(self):
        pass

    def test_dp_solution_1(self):
        n = 8
        pf = PerfectSquares(n)
        actual = pf.dp_solution()
        expected = 2

        self.assertEqual(actual, expected, "should be 2.")

    def test_dp_solution_2(self):
        n = 15
        pf = PerfectSquares(n)
        actual = pf.dp_solution()
        expected = 4

        self.assertEqual(actual, expected, "should be 4.")

    def test_dp_solution_3(self):
        n = 12
        pf = PerfectSquares(n)
        actual = pf.dp_solution()
        expected = 3

        self.assertEqual(actual, expected, "should be 3.")
