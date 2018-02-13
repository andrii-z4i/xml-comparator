from unittest import TestCase
from diff.comparators.attr_comparator import AttrComparator
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