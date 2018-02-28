import xml.etree.ElementTree as ET
from logging import Logger
from .utils import parse_type_from_tag


class XmlComparator(object):
    def __init__(self, root_left, root_right, logger=None):
        self._root_left = root_left
        self._root_right = root_right
        self._logger = logger
        self._comparator = None
        self._comparison_results = []
        self._types_to_skip = None

    def add_types_to_skip(self, type_name):
        if not self._types_to_skip:
            self._types_to_skip = []

        self._types_to_skip.append(type_name)

    def set_comparator(self, comparator):
        if not comparator:
            raise Exception("Comparator can't be None")
        self._comparator = comparator

    def _print_debug_information(self, message):
        if not self._logger:
            return
        self._logger.debug(message)

    def _compare(self, element_left, element_right, index, depth=None):
        if depth == index:
            return self._compare_elements_if_depth_reached(element_left, element_right)

        _left_sub_elements = self._sort_elements([e for e in element_left])
        _right_sub_elements = self._sort_elements([e for e in element_right])

        _left_sub_elements = [element for element in filter(
            lambda e:
            not self._check_if_type_has_to_be_skipped(parse_type_from_tag(e.tag, self._logger)) if e.tag else True,
            _left_sub_elements
        )]

        _right_sub_elements = [element for element in filter(
            lambda e:
            not self._check_if_type_has_to_be_skipped(parse_type_from_tag(e.tag, self._logger)) if e.tag else True,
            _right_sub_elements
        )]

        _left_length = len(_left_sub_elements)
        _right_length = len(_right_sub_elements)

        if _left_length != _right_length:
            self._print_debug_information("Length is not equal (%d != %d)" % (_left_length, _right_length))
            return False

        if not _left_length:
            return self._compare_two_elements(element_left, element_right)

        _index = index + 1
        _results = []
        for (l, r) in zip(_left_sub_elements, _right_sub_elements):
            self._print_debug_information("Going to compare {%s and %s}" % (l, r))
            _compare_result = self._compare(l, r, _index, depth)
            self._print_debug_information("Result is %s" % _compare_result)
            _results.append(_compare_result)

        _results.append(self._compare_two_elements(element_left, element_right))

        return self._single_result(_results)

    def _compare_elements_if_depth_reached(self, element_left, element_right):
        if element_left is None or element_right is None:
            self._print_debug_information("One of elements is None, returns False")
            return False
        if element_right is None and element_left is None:
            self._print_debug_information("Both elements are None, returns False")
            return True
        return self._compare_two_elements(element_left, element_right)

    def _compare_two_elements(self, left_element, right_element):
        if not self._comparator:
            self._print_debug_information('Skip comparing since no comparator has been set')
            return True

        return self._comparator.compare(left_element, right_element)

    def _sort_elements(self, sub_elements):
        return sorted(sub_elements, key=lambda e: parse_type_from_tag(e.tag, self._logger) if e.tag else '')

    def _check_if_type_has_to_be_skipped(self, type):
        if not self._types_to_skip:
            return False
        return type in self._types_to_skip

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
        self._print_debug_information("Single result is %s" % _result)
        return _result

    def compare(self, depth=None):
        """Compare two files up to depth level"""
        index = 0
        _result = self._compare(
            self._root_left, self._root_right, index, depth)
        return _result


def create_xml_diff_from_files(file1, file2, logger=None):
    if not file1 or not file2:
        raise Exception('Expected files path as parameters')

    with open(file1, 'r') as _f1:
        _lines = _f1.readlines()
        _root1 = ET.fromstringlist(_lines)

    with open(file2, 'r') as _f2:
        _lines = _f2.readlines()
        _root2 = ET.fromstringlist(_lines)

    return XmlComparator(_root1, _root2, logger)

def create_xml_diff_from_strings(string1, string2, logger=None):
    _root1 = ET.fromstring(string1)
    _root2 = ET.fromstring(string2)
    return XmlComparator(_root1, _root2, logger)