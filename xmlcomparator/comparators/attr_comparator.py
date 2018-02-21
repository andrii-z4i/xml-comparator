from .comparator import Comparator


class AttrComparator(Comparator):
    def __init__(self, logger):
        super(AttrComparator, self).__init__(logger)
        self._check_value = True
        self._attr_comparator_policy = None

    def set_check_values(self, flag):
        self._check_value = flag

    def set_attr_comparator_policy(self, comparator_policy):
        self._attr_comparator_policy = comparator_policy

    def _process_keys(self, attr_keys):
        keys = attr_keys
        if self._attr_comparator_policy:
            _filtered = filter(lambda x: self._attr_comparator_policy.should_compare(x), attr_keys)
            keys = [_key for _key in _filtered]
        else:
            self._print_debug_information("No attr comparator policy")

        return keys

    def _check_for_len(self, left_keys, right_keys):
        if len(left_keys) != len(right_keys):
            self._print_debug_information("Keys' len are different")
            return False
        return True

    def _check_keys(self, left_keys, right_keys):
        if left_keys != right_keys:
            self._print_debug_information("Keys are different")
            return False
        return True

    def _check_key_values(self, keys, left_element_attrs, right_element_attrs):
        if not self._check_value:
            self._print_debug_information("Skipping to check values")
            return True

        _result = True
        self._print_debug_information("Check values by keys")
        for key in keys:
            _result = _result and left_element_attrs[key] == right_element_attrs[key]
        return _result

    def _compare(self, left, right):
        self._print_debug_information("Compare %s and %s" % (left.attrib, right.attrib))

        _left_attr_keys = sorted(left.attrib.keys())
        _right_attr_keys = sorted(right.attrib.keys())

        _left_attr_keys = self._process_keys(_left_attr_keys)
        _right_attr_keys = self._process_keys(_right_attr_keys)

        if not self._check_for_len(_left_attr_keys, _right_attr_keys):
            return False

        if not self._check_keys(_left_attr_keys, _right_attr_keys):
            return False

        return self._check_key_values(_left_attr_keys, left.attrib, right.attrib)