from unittest import TestCase
from xmlcomparator.comparators.attr_comparator_policy import AttrComparatorPolicy
from unittest.mock import Mock, patch, call
from tests import logging_configuration as lc


class TestAttrComparatorPolicy(TestCase):
    def test_instatiate_policy_no_throw(self):
        _policy = AttrComparatorPolicy()
        self.assertListEqual(_policy._attr_names, [])

    def test_add_attribute_name(self):
        _policy = AttrComparatorPolicy()

        with patch.object(_policy, '_print_debug_information') as _print_debug:
            _policy.add_attribute_name_to_compare('something')
            _policy.add_attribute_name_to_compare('something2')
            _policy.add_attribute_name_to_compare('something')

        self.assertListEqual(['something', 'something2'], _policy._attr_names)
        self.assertEqual(4, _print_debug.call_count)
        self.assertListEqual(
            [
                call("Adding 'something' attribute"),
                call("Adding 'something2' attribute"),
                call("Adding 'something' attribute"),
                call("Skipping add 'something' attribute since it exists"),
            ],
            _print_debug.call_args_list
        )

    def test_should_compare(self):
        _policy = AttrComparatorPolicy()

        with patch.object(_policy, '_print_debug_information') as _print_debug:
            _policy.add_attribute_name_to_compare('something')
            _policy.add_attribute_name_to_compare('something2')
            _policy.add_attribute_name_to_compare('something')
            self.assertTrue(_policy.should_compare('something'))
            self.assertFalse(_policy.should_compare('a'))

        self.assertListEqual(['something', 'something2'], _policy._attr_names)
        self.assertEqual(6, _print_debug.call_count)
        self.assertListEqual(
            [
                call("Adding 'something' attribute"),
                call("Adding 'something2' attribute"),
                call("Adding 'something' attribute"),
                call("Skipping add 'something' attribute since it exists"),
                call("There is necessity to compare 'something' attribute"),
                call("There is no necessity to compare 'a' attribute")
            ],
            _print_debug.call_args_list
        )
