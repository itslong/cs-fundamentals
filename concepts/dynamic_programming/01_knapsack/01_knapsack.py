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
        return self.helper_brute_force_pick_choices(0, 0)

    def helper_brute_pick_all_items(self, curr_weight, curr_val):
        if curr_weight > self.max_weight:
            return 0

        # set the max value to the current value.
        max_val = curr_val

        for choice in self.items:
            new_weight = curr_weight + choice['w']
            # only pick the item if it is under or equal to the max weight
            if new_weight <= self.max_weight:
                new_val = self.helper_brute_force_pick_choices(new_weight, curr_val + choice['v'])

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

    def top_down_selective_pick_using_cache(self):
        self.cache = {}
        return self.helper_top_down_selective_pick_using_cache(self.max_weight, 0)

    def helper_top_down_selective_pick_using_cache(self, avail_weight, index):
        if index >= len(self.items):
            return 0

        # check if the item has been cached
        if index not in self.cache:
            self.cache[index] = {}

        cached_val = self.cache[index].get('w', None)
        if cached_val is not None and len(cached_val) != 0:
            return cached_val

        curr_item_weight = self.items[index]['w']
        curr_item_value = self.items[index]['v']

        if avail_weight - curr_item_weight < 0:
            # adding this item would exceed the weight, so do not pick it
            max_value = self.helper_top_down_selective_pick_using_cache(avail_weight, index + 1)
        else:
            # both options are valid: pick this item or do not pick this item
            item_picked = self.helper_top_down_selective_pick_using_cache(avail_weight - curr_item_weight, index + 1) + curr_item_value
            item_not_picked = self.helper_top_down_selective_pick_using_cache(avail_weight, index + 1)

            # if item_picked > item_not_picked:
            #     remain_weight = avail_weight - curr_item_weight
            #     max_value = item_picked
            # else:
            #     remain_weight = avail_weight
            #     max_value = item_not_picked
            max_value = max(item_not_picked, item_picked)
        self.cache[index] = {'w': avail_weight, 'v': max_value}
        print('cache after adding: ', index, self.cache)
        return max_value



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

    def test_top_down_selective_pick_with_cache_solution(self):
        max_weight = 2
        data = [
            {'w': 2, 'v': 6},
            {'w': 2, 'v': 10},
            # {'w': 3, 'v': 12}
        ]
        knapsack = Knapsack(data, max_weight)

        actual = knapsack.top_down_selective_pick_using_cache()
        expected = 22
        self.assertEqual(actual, expected, "should return 22 value.")