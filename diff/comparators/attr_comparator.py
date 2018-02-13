from .comparator import Comparator


class AttrComparator(Comparator):
    def __init__(self, logger):
        super(AttrComparator, self).__init__(logger)
        self._check_value = True

    def set_check_values(self, flag):
        self._check_value = flag

    def _compare(self, left, right):
        self._print_debug_information("Compare %s and %s" % (left.attr, right.attr))

        _left_attr_keys = sorted(left.attr.keys())
        _right_attr_keys = sorted(right.attr.keys())

        if len(_left_attr_keys) != len(_right_attr_keys):
            self._print_debug_information("Keys' len are different")
            return False

        if _left_attr_keys != _right_attr_keys:
            self._print_debug_information("Keys are different")
            return False

        if not self._check_value:
            self._print_debug_information("Skipping to check values")
            return True

        _result = True
        self._print_debug_information("Check values by keys")
        for key in _left_attr_keys:
            _result = _result and left.attr[key] == right.attr[key]
        return _result