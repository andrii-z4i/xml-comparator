from abc import  ABC, abstractclassmethod


class ComparatorPolicy(ABC):
    def __init__(self, logger=None):
        self._logger = logger

    def _print_debug_information(self, message):
        if not self._logger:
            return
        self._logger.debug(message)

    @abstractclassmethod
    def should_compare(self, attr):
        return NotImplemented