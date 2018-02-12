from .comparator import Comparator
from re import match, compile

_tag_regexp = compile("(\{.*\})(.*)")


class TypeComparator(Comparator):
    def _get_type_from_tag(self, tag):
        return _tag_regexp.match(tag).group(2)

    def _compare(self, left, right):
        if self.logger:
            self.logger.debug("Compare %s and %s" % (left.tag, right.tag))
        return self._get_type_from_tag(left.tag) == self._get_type_from_tag(right.tag)
