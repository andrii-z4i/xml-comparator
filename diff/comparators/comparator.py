from abc import ABC, abstractmethod


class Comparator(ABC):
    def __init__(self, logger=None):
        self._next_comparator = None
        self._logger = logger

    def _print_debug_information(self, message):
        if not self._logger:
            return
        self._logger.debug(message)

    def set_next_comparator(self, cmp):
        if not isinstance(cmp, Comparator):
            raise Exception('cmp has to be %s inherited' % self.__class__)
        self._next_comparator = cmp
        self._print_debug_information('Next comparator has been set')

    @abstractmethod
    def _compare(self, left, right):
        raise NotImplementedError()

    def compare(self, left, right):
        if self._compare(left, right):
            self._print_debug_information('"%s" succeeded' % self.__class__)
            if self._next_comparator:
                self._print_debug_information('Call next comparator "%s"' % self._next_comparator.__class__)
                return self._next_comparator.compare(left, right)
            self._print_debug_information('"%s" returns "True"' % self.__class__)
            return True
        self._print_debug_information('"%s" returns "False"' % self.__class__)
        return False
