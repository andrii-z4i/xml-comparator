from .comparator import Comparator
from ..utils import parse_type_from_tag


class TypeComparator(Comparator):
    def _get_type_from_tag(self, tag):
        return parse_type_from_tag(tag)

    def _compare(self, left, right):
        if self.logger:
            self.logger.debug("Compare %s and %s" % (left.tag, right.tag))
        return self._get_type_from_tag(left.tag) == self._get_type_from_tag(right.tag)
