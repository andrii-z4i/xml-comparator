from unittest import TestCase
from diff.comparators.attr_comparator import AttrComparator
from diff.comparators.attr_comparator_policy import AttrComparatorPolicy
from unittest.mock import Mock
from tests import logging_configuration as lc


class TestAttrComparator(TestCase):
    def setUp(self):
        self._comparator = AttrComparator(lc.get_logger('attr'))

    def test_compare_different_attr_len(self):
        _left_element = Mock(attr={'a': 1, 'b': 2})
        _right_element = Mock(attr={'a': 1, 'b': 2, 'c': 3})
        self.assertFalse(self._comparator.compare(_left_element, _right_element))

    def test_compare_different_keys_when_equal_attr_len(self):
        _left_element = Mock(attr={'a': 1, 'b': 2, 'd': 3})
        _right_element = Mock(attr={'a': 1, 'b': 2, 'c': 3})
        self.assertFalse(self._comparator.compare(_left_element, _right_element))

    def test_compare_different_values_when_equal_keys_with_no_value_chek(self):
        _left_element = Mock(attr={'a': 1, 'b': 2, 'c': 3})
        _right_element = Mock(attr={'a': 1, 'b': 2, 'c': 4})
        self._comparator.set_check_values(False)
        self.assertTrue(self._comparator.compare(_left_element, _right_element))

    def test_compare_different_values_when_equal_keys_with_value_chek(self):
        _left_element = Mock(attr={'a': 1, 'b': 2, 'c': 3})
        _right_element = Mock(attr={'a': 1, 'b': 2, 'c': 4})
        self._comparator.set_check_values(True)
        self.assertFalse(self._comparator.compare(_left_element, _right_element))

    def test_compare_the_same_values_when_equal_keys_with_value_chek(self):
        _left_element = Mock(attr={'a': 1, 'b': 2, 'c': 4})
        _right_element = Mock(attr={'a': 1, 'b': 2, 'c': 4})
        self._comparator.set_check_values(True)
        self.assertTrue(self._comparator.compare(_left_element, _right_element))

    def test_compare_with_comparator_policy(self):
        _left_element = Mock(attr={'a': 3, 'b': 2, 'c': 4})
        _right_element = Mock(attr={'b': 2, 'd': 6, 'c': 4})
        _policy = AttrComparatorPolicy(lc.get_logger('attrPolicy'))
        _policy.add_attribute_name('b')
        _policy.add_attribute_name('c')
        self._comparator.set_check_values(True)
        self._comparator.set_attr_comparator_policy(_policy)

        self.assertTrue(self._comparator.compare(_left_element, _right_element))
