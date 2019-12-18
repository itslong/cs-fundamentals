"""
Imagine that you have a knapsack which can carry a certain maximum amount of weight
and you have a set of items with their own weight and a monetary value.
You are going to to sell your items in the market but you can only carry what fits in the knapsack.
How do you maximize the amount of money that you can earn?


Given a list of items with values and weights, as well as a max weight,
find the maximum value you can generate from items,
where the sum of the weights is less than or equal to the max. eg.

items = {(w:2, v:6), (w:2, v:10), (w:3, v:12)}
max weight = 5
knapsack(items, max weight) = 22
"""

import unittest


class Knapsack:
    def __init__(self, items, max_weight):
        self.items = items
        self.max_weight = max_weight

    def brute_force_pick_all_items(self):
        return self.helper_brute_pick_all_items(0, 0)

    def helper_brute_pick_all_items(self, curr_weight, curr_val):
        if curr_weight > self.max_weight:
            return 0

        # set the max value to the current value.
        max_val = curr_val

        for choice in self.items:
            new_weight = curr_weight + choice['w']
            # only pick the item if it is under or equal to the max weight
            if new_weight <= self.max_weight:
                new_val = self.helper_brute_pick_all_items(new_weight, curr_val + choice['v'])

                # compare the weight with the item picked.
                if new_val > max_val:
                    max_val = new_val
        return max_val

    def brute_force_selective_pick(self):
        return self.helper_brute_force_selective_pick(self.max_weight, 0)

    def helper_brute_force_selective_pick(self, avail_weight, index):
        if index >= len(self.items):
            return 0

        # pick the current item if theres available weight, otherwise, skip it
        curr_item_weight = self.items[index]['w']
        if avail_weight - curr_item_weight < 0:
            return self.helper_brute_force_selective_pick(avail_weight, index + 1)
        else:
            # there is weight available, so get the max value of either picking the item or skipping the item
            item_picked = self.helper_brute_force_selective_pick(avail_weight - curr_item_weight, index + 1) + self.items[index]['v']
            item_not_picked = self.helper_brute_force_selective_pick(avail_weight, index + 1)

            return max(item_picked, item_not_picked)

    def dp_pick_items(self):
        dp = [[0 for w in range(self.max_weight + 1)] for i in range(len(self.items))]

        index = 0
        r = 0
        rows = len(self.items)
        cols = self.max_weight

        while r < rows:
            c = 0
            while c <= cols:
                if c >= self.items[index]['w']:
                    """
                    1. pick previous item, do not pick current item
                    2. do not pick previous item, pick current item only
                    3. pick previous and pick current item
                    4. change in weight does not allow more items to be picked (3) so continue to pick current item
                    """
                    left = dp[r][c - 1] if c - 1 >= 0 else 0
                    above = dp[r - 1][c] if r - 1 >= 0 else 0
                    only_curr = self.items[index]['v']
                    pick_all = only_curr + dp[r - 1][c - self.items[index]['w']]
                    dp[r][c] = max(left, above, only_curr, pick_all)
                else:
                    left = dp[r][c - 1] if c - 1 >= 0 else 0
                    above = dp[r - 1][c] if r - 1 >= 0 else 0
                    dp[r][c] = max(left, above)
                c += 1
            index += 1
            r += 1

        return dp[len(self.items) - 1][self.max_weight]


class TestKnapsack(unittest.TestCase):

    def test_brute_force_solution(self):
        """
        assumes the same item can be picked repeatedly.
        """
        max_weight = 5
        data = [
            {'w': 2, 'v': 6},
            {'w': 2, 'v': 10},
            {'w': 3, 'v': 12}
        ]
        knapsack = Knapsack(data, max_weight)

        actual = knapsack.brute_force_pick_all_items()
        expected = 22
        self.assertEqual(actual, expected, "should return 22 value.")

    def test_brute_force_solution_2(self):
        """
         assumes the same item can be picked repeatedly.
         """
        max_weight = 8
        data = [
            {'w': 2, 'v': 8},
            {'w': 3, 'v': 6},
            {'w': 4, 'v': 4}
        ]
        knapsack = Knapsack(data, max_weight)
        actual = knapsack.brute_force_pick_all_items()
        expected = 32
        self.assertEqual(actual, expected, "should return 32 value.")

    def test_brute_force_solution_3(self):
        """
         assumes the same item can be picked repeatedly.
         """
        max_weight = 28
        data = [
            {'w': 2, 'v': 4},
            {'w': 5, 'v': 11},
            {'w': 7, 'v': 20},
            {'w': 3, 'v': 18}
        ]
        knapsack = Knapsack(data, max_weight)
        actual = knapsack.brute_force_pick_all_items()
        expected = 162
        self.assertEqual(actual, expected, "should return 162 value.")

    def test_brute_force_selective_pick_solution(self):
        """
         the same item cannot be picked repeatedly.
         """
        max_weight = 5
        data = [
            {'w': 2, 'v': 6},
            {'w': 2, 'v': 10},
            {'w': 3, 'v': 12}
        ]
        knapsack = Knapsack(data, max_weight)

        actual = knapsack.brute_force_selective_pick()
        expected = 22
        self.assertEqual(actual, expected, "should return 22 value.")

    def test_brute_force_selective_pick_solution_2(self):
        max_weight = 8
        data = [
            {'w': 2, 'v': 8},
            {'w': 3, 'v': 6},
            {'w': 4, 'v': 4}
        ]
        knapsack = Knapsack(data, max_weight)
        actual = knapsack.brute_force_selective_pick()
        expected = 14
        self.assertEqual(actual, expected, "should return 14 value.")

    def test_brute_force_selective_pick_solution_3(self):
        max_weight = 11
        data = [
            {'w': 2, 'v': 4},
            {'w': 5, 'v': 11},
            {'w': 6, 'v': 20},
            {'w': 3, 'v': 18}
        ]
        knapsack = Knapsack(data, max_weight)
        actual = knapsack.brute_force_selective_pick()
        expected = 42
        self.assertEqual(actual, expected, "should return 42 value.")

    def test_dp_solution(self):
        max_weight = 5
        data = [
            {'w': 2, 'v': 6},
            {'w': 2, 'v': 10},
            {'w': 3, 'v': 12}
        ]
        knapsack = Knapsack(data, max_weight)

        actual = knapsack.dp_pick_items()
        expected = 22
        self.assertEqual(actual, expected, 'should equal to 22')

    def test_dp_solution2(self):
        max_weight = 8
        data = [
            {'w': 2, 'v': 8},
            {'w': 3, 'v': 6},
            {'w': 4, 'v': 4}
        ]
        knapsack = Knapsack(data, max_weight)

        actual = knapsack.dp_pick_items()
        expected = 14
        self.assertEqual(actual, expected, 'should equal to 14')

    def test_dp_solution3(self):
        max_weight = 11
        data = [
            {'w': 2, 'v': 4},
            {'w': 5, 'v': 11},
            {'w': 6, 'v': 20},
            {'w': 3, 'v': 18}
        ]
        knapsack = Knapsack(data, max_weight)

        actual = knapsack.dp_pick_items()
        expected = 42
        self.assertEqual(actual, expected, 'should equal to 42')
