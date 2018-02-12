from unittest import TestCase
from diff.xml_diff import XmlComparator, get_name_from_tag


class TestXmlComparator(TestCase):

    def test_parse_file(self):
        c = XmlComparator('C:\\Users\\z4i\\projects\\investigations\\content.xml',
                          'C:\\Users\\z4i\\projects\\investigations\\content2.xml')
        c.parse()
        self.assertTrue(c.is_parsed)
        self.assertFalse(c.compare(depth=9))


class TestElementWrapper(TestCase):

    def test_regex(self):
        self.assertEqual(
            'xmap-content', get_name_from_tag('{urn:xmind:xmap:xmlns:content:2.0}xmap-content'))
