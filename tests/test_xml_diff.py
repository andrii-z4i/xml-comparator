from unittest import TestCase
from diff.xml_diff import XmlComparator
from diff.comparators.type_comparator import TypeComparator
from diff.comparators.text_comparator import TextComparator
import logging

FORMAT = '[%(name)s - %(levelname)s] %(asctime)-15s: %(message)s'


class TestXmlDiff(TestCase):

    def test_parse_file(self):
        logging.basicConfig(format=FORMAT, level=logging.DEBUG)
        _type_comparator = TypeComparator(logging.getLogger('type'))
        _text_comparator = TextComparator(logging.getLogger('text'))
        _type_comparator.set_next_comparator(_text_comparator)
        c = XmlComparator('C:\\Users\\z4i\\projects\\investigations\\content.xml',
                          'C:\\Users\\z4i\\projects\\investigations\\content2.xml',
                          _type_comparator,
                          logging.getLogger('comparator'))
        c.parse()
        self.assertTrue(c.is_parsed)
        self.assertFalse(c.compare(depth=9))
