from .comparator import Comparator
from re import match, compile


class TextComparator(Comparator):

    def _compare(self, left, right):
        if self.logger:
            self.logger.debug("Compare %s and %s" % (left.text, right.text))
        return left.text == right.text
