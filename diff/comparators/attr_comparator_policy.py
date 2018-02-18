from .comparator_policy import ComparatorPolicy


class AttrComparatorPolicy(ComparatorPolicy):
    def __init__(self, logger=None):
        super().__init__(logger)
        self._attr_names = []

    def add_attribute_name(self, attr_name):
        self._print_debug_information("Adding '%s' attribute" % attr_name)
        if attr_name not in self._attr_names:
            self._attr_names.append(attr_name)
        else:
            self._print_debug_information("Skipping add '%s' attribute since it exists" % attr_name)

    def should_compare(self, attr):
        self._print_debug_information("Check for necessity to compare '%s' attribute" % attr)
        return attr in self._attr_names
