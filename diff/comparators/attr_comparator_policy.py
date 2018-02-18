from .comparator_policy import ComparatorPolicy


class AttrComparatorPolicy(ComparatorPolicy):
    def __init__(self, logger=None):
        super().__init__(logger)
        self._attr_names = []
        self._skip_attr_names = []

    def add_attribute_name_to_compare(self, attr_name):
        self._print_debug_information("Adding '%s' attribute" % attr_name)
        if attr_name not in self._attr_names:
            self._attr_names.append(attr_name)
        else:
            self._print_debug_information("Skipping add '%s' attribute since it exists" % attr_name)

    def add_attribute_name_to_skip_compare(self, attr_name):
        self._print_debug_information("Mark '%s' attribute as skip to compare" % attr_name)
        _attr_in_required_to_check = attr_name in self._attr_names
        _attr_in_skip_to_check = attr_name in self._skip_attr_names
        if not _attr_in_required_to_check and not _attr_in_skip_to_check:
            self._skip_attr_names.append(attr_name)
        else:
            self._print_debug_information(
                "Skipping add '%s' attribute since it exists in attributes to %s" %
                (attr_name, 'check' if _attr_in_required_to_check else 'skip'))

    def should_compare(self, attr_name):
        _attr_in_required_to_check = attr_name in self._attr_names
        _attr_in_skip_to_check = attr_name in self._skip_attr_names
        if len(self._attr_names):
            _result = _attr_in_required_to_check
        elif len(self._skip_attr_names):
            _result = not _attr_in_skip_to_check if _attr_in_skip_to_check else True
        else:
            _result = False
        self._print_debug_information("There is %snecessity to compare '%s' attribute" % ('' if _result else 'no ', attr_name))
        return _result
