import xml.etree.ElementTree as ET
from re import match, compile

_tag_regexp = compile("(\{.*\})(.*)")

def get_name_from_tag(tag):
    return _tag_regexp.match(tag).group(2)

class XmlComparator(object):
    def __init__(self, file1, file2):
        self._file1 = file1
        self._file2 = file2
        self._parsed_file1 = None
        self._parsed_file2 = None
        self._were_files_parsed = False

    @property
    def is_parsed(self):
        return self._were_files_parsed

    @property
    def xml_tree_file1(self):
        if not self._were_files_parsed:
            raise Exception('Files have to be parsed first')

        return self._parsed_file1

    @property
    def xml_tree_file2(self):
        if not self._were_files_parsed:
            raise Exception('Files have to be parsed first')

        return self._parsed_file2

    def parse(self):
        self._parsed_file1 = ET.parse(self._file1).getroot()
        self._parsed_file2 = ET.parse(self._file2).getroot()
        self._were_files_parsed = self._parsed_file1 is not None and self._parsed_file2 is not None

    def _sort_elements(self, sub_elements):
        return sorted(sub_elements, key=lambda e: get_name_from_tag(e.tag))

    def _compare_two_elements(self, left_element, right_element):
        _left_name = left_element.text
        _right_name = right_element.text
        _result = 1
        if _left_name == _right_name:
            _result = 0
        elif _left_name < _right_name:
            _result = -1
        if _result != 0:
            print('"', _left_name, '" <> "', _right_name, '" => ', _result)
        return _result

    def _compare(self, element_left, element_right, index, depth=None):
        if depth == index:
            if element_left is not None and element_right is None:
                return 1
            if element_left is None and element_right is not None:
                return -1
            if element_right is None and element_left is None:
                return 0
            return self._compare_two_elements(element_left, element_right)

        _left_sub_elements = self._sort_elements([e for e in element_left])
        _right_sub_elements = self._sort_elements([e for e in element_right])

        _left_length = len(_left_sub_elements)
        _right_length = len(_right_sub_elements)

        if _left_length != _right_length:
            return -1 if _left_length < _right_length else 1

        if not _left_length:
            return self._compare_two_elements(element_left, element_right)

        _index = index + 1
        _results = []
        for (l, r) in zip(_left_sub_elements, _right_sub_elements):
            _results.append(self._compare(l, r, _index, depth))

        return self._single_result(_results)

    def _single_result(self, results):
        _less_result = results.count(-1)
        _more_result = results.count(1)
        _result = 0
        if _less_result and not _more_result:
            _result = -1
        elif _more_result and not _less_result:
            _result = 1
        elif _less_result and _more_result:
            if _less_result == _more_result:
                _result = -1
            elif _less_result > _more_result:
                _result = -1
            elif _less_result < _more_result:
                _result = 1
        if _result != 0:
            print(results, '==>', _result)
        return _result

    def compare(self, depth=None):
        """Compare two files up to depth level"""
        index = 0
        _result = self._compare(self._parsed_file1, self._parsed_file2, index, depth)
        return _result


from unittest import TestCase


class TestXmlComparator(TestCase):

    def test_parse_file(self):
        c = XmlComparator('C:\\Users\\z4i\\projects\\investigations\\content.xml',
                          'C:\\Users\\z4i\\projects\\investigations\\content2.xml')
        c.parse()
        self.assertTrue(c.is_parsed)
        print(get_name_from_tag(c.xml_tree_file1.tag))
        for child in c.xml_tree_file1:
            print(get_name_from_tag(child.tag))
        print(c.compare(depth=9))


class TestElementWrapper(TestCase):

    def test_regex(self):
        self.assertEqual('xmap-content', get_name_from_tag('{urn:xmind:xmap:xmlns:content:2.0}xmap-content'))
