from .comparator import Comparator


class TextComparator(Comparator):

    def _compare(self, left, right):
        self._print_debug_information("Compare %s and %s" % (left.text, right.text))
        return left.text == right.text
