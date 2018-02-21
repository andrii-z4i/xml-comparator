from unittest import TestCase
from xmlscomparator.comparators.type_comparator import TypeComparator
from unittest.mock import Mock


class TestTypeComparator(TestCase):

    def test_regex(self):
        tc = TypeComparator()
        self.assertEqual(
            'xmap-content', tc._get_type_from_tag('{urn:xmind:xmap:xmlns:content:2.0}xmap-content'))

    def test_comparator_not_equal(self):
        tc = TypeComparator()
        _left = Mock(tag='{urn:xmind:xmap:xmlns:content:2.0}xmap-content')
        _right = Mock(tag='{urn:xmind:xmap:xmlns:content:2.0}xmap-content1')
        self.assertFalse(tc.compare(_left, _right))

    def test_comparator_equal(self):
        tc = TypeComparator()
        _left = Mock(tag='{urn:xmind:xmap:xmlns:content:2.0}xmap-content')
        _right = Mock(tag='{urn:xmind:xmap:xmlns:content:2.0}xmap-content')
        self.assertTrue(tc.compare(_left, _right))
