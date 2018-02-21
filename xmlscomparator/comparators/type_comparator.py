from .comparator import Comparator
from ..utils import parse_type_from_tag


class TypeComparator(Comparator):
    def _get_type_from_tag(self, tag):
        return parse_type_from_tag(tag)

    def _compare(self, left, right):
        self._print_debug_information("Compare %s and %s" % (left.tag, right.tag))
        return self._get_type_from_tag(left.tag) == self._get_type_from_tag(right.tag)
