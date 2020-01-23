"""
Given an array of integers where each value 1 <= x <= len(array),
write a function that finds all the duplicates in the array.

dups([1, 2, 3])    = []
dups([1, 2, 2])    = [2]
dups([3, 3, 3])    = [3]
dups([2, 1, 2, 1]) = [1, 2]

"""
import unittest

class FindDuplicates(object):
    """
    Questions to ask:

    1. Does the output order matter?
    2. Can the result itself contain duplicates?
    """
    def __init__(self, arr):
        self.arr = arr

    def brute_force_solution(self):
        """
        Time: O(n)
        Space: O(n)

        """
        d = {}
        output = []

        for i in self.arr:
            if i in d and i not in output:
                output.append(i)
            else:
                d[i] = 1

        return output

    def encoding_solution(self):
        """
        Time: O(n)
        Space: O(1)
        """
        result = set()

        for a in self.arr:
            index = abs(a) - 1

            if self.arr[index] < 0:
                # if the INDEX is negative, add the CURRENT value
                result.add(abs(a))
            else:
                self.arr[index] = self.arr[index] * -1

        return list(result)


class TestFindDuplicates(unittest.TestCase):
    def test_brute_force_solution__no_dupes(self):
        arr = [1, 2, 3]
        fd = FindDuplicates(arr)
        actual = fd.brute_force_solution()
        expected = []

        self.assertEqual(actual, expected, 'there are no dupes. should return an empty array.')

    def test_brute_force_solution__dupes1(self):
        arr = [1, 2, 5, 1, 2]
        fd = FindDuplicates(arr)
        actual = fd.brute_force_solution()
        expected = [1, 2]

        self.assertEqual(actual, expected, 'there are dupes. should return the dupes: [1,2].')

    def test_brute_force_solution__dupes2(self):
        arr = [3, 3, 3]
        fd = FindDuplicates(arr)
        actual = fd.brute_force_solution()
        expected = [3]

        self.assertEqual(actual, expected, 'there are dupes. should return the dupes: [3].')

    def test_encoding_solution__1(self):
        arr = [1, 2, 2, 3, 3, 6]
        fd = FindDuplicates(arr)
        actual = fd.encoding_solution()
        expected = [2, 3]

        self.assertEqual(actual, expected, 'there are dupes. should return the dupes: [2,3].')

    def test_encoding_solution__2(self):
        arr = [1, 2, 5, 4, 2, 6, 2, 5, 1]
        fd = FindDuplicates(arr)
        actual = fd.encoding_solution()
        expected = [1, 2, 5]

        self.assertEqual(actual, expected, 'there are dupes. should return the dupes: [1,2,5].')


if __name__ == '__main__':
    TestFindDuplicates()
