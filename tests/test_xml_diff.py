from unittest import TestCase
from diff.xml_diff import XmlComparator
from diff.comparators.type_comparator import TypeComparator
from diff.comparators.text_comparator import TextComparator
from tests import logging_configuration as lc

class TestXmlDiff(TestCase):

    def test_parse_file(self):
        _type_comparator = TypeComparator(lc.get_logger('type'))
        _text_comparator = TextComparator(lc.get_logger('text'))
        _type_comparator.set_next_comparator(_text_comparator)
        c = XmlComparator('C:\\Users\\z4i\\projects\\investigations\\content.xml',
                          'C:\\Users\\z4i\\projects\\investigations\\content2.xml',
                          _type_comparator,
                          lc.get_logger('comparator'))
        c.parse()
        self.assertTrue(c.is_parsed)
        self.assertFalse(c.compare(depth=9))
