from unittest import TestCase
from xmlscomparator.comparators.comparator_policy import ComparatorPolicy


class TestComparatorPolicy(TestCase):
    def test_instantiate_throws(self):
        with self.assertRaises(TypeError) as _ex:
            _comparator_policy = ComparatorPolicy()
        self.assertTrue(_ex.exception.args[0].find(
            "Can't instantiate abstract class") != -1)
