from abc import ABC, abstractmethod


class Comparator(ABC):
    def __init__(self, logger=None):
        self._next_comparator = None
        self._logger = logger

    @property
    def logger(self):
        return self._logger

    def set_next_comparator(self, cmp):
        if not isinstance(cmp, Comparator):
            raise Exception('cmp has to be %s inherited' % self.__class__)
        self._next_comparator = cmp

    @abstractmethod
    def _compare(self, left, right):
        raise NotImplementedError()

    def compare(self, left, right):
        if self._compare(left, right):
            if self._next_comparator:
                return self._next_comparator.compare(left, right)
            return True
        return False
