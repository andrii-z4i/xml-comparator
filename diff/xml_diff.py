import xml.etree.ElementTree as ET
from logging import Logger
from .utils import parse_type_from_tag


class XmlComparator(object):
    def __init__(self, file1, file2, comparator, logger=None):
        self._file1 = file1
        self._file2 = file2
        self._parsed_file1 = None
        self._parsed_file2 = None
        self._were_files_parsed = False
        self._logger = logger
        if not comparator:
            raise Exception('Comparator has to be set')
        self._comparator = comparator

    def _print_debug_information(self, message):
        if not self._logger:
            return
        self._logger.debug(message)

    @property
    def is_parsed(self):
        return self._were_files_parsed

    def parse(self):
        self._parsed_file1 = ET.parse(self._file1).getroot()
        self._parsed_file2 = ET.parse(self._file2).getroot()
        self._were_files_parsed = self._parsed_file1 is not None and self._parsed_file2 is not None

    def _compare(self, element_left, element_right, index, depth=None):
        if depth == index:
            return self._compare_elements_if_depth_reached(element_left, element_right)

        _left_sub_elements = self._sort_elements([e for e in element_left])
        _right_sub_elements = self._sort_elements([e for e in element_right])

        _left_length = len(_left_sub_elements)
        _right_length = len(_right_sub_elements)

        if _left_length != _right_length:
            return False

        if not _left_length:
            return self._compare_two_elements(element_left, element_right)

        _index = index + 1
        _results = []
        for (l, r) in zip(_left_sub_elements, _right_sub_elements):
            _results.append(self._compare(l, r, _index, depth))

        return self._single_result(_results)

    def _compare_elements_if_depth_reached(self, element_left, element_right):
        if element_left is not None or element_right is not None:
            return False
        if element_right is None and element_left is None:
            return True
        return self._compare_two_elements(element_left, element_right)

    def _compare_two_elements(self, left_element, right_element):
        return self._comparator.compare(left_element, right_element)

    def _sort_elements(self, sub_elements):
        return sorted(sub_elements, key=lambda e: parse_type_from_tag(e.tag, self._logger) if e.tag else '')

    def _single_result(self, results):
        _false_index = None
        try:
            _false_index = results.index(False)
        except ValueError as _ex:
            _false_index = -1
        _result = True
        if _false_index != -1:
            self._print_debug_information(results)
            _result = False
        return _result

    def compare(self, depth=None):
        """Compare two files up to depth level"""
        index = 0
        _result = self._compare(
            self._parsed_file1, self._parsed_file2, index, depth)
        return _result
