from unittest import TestCase
from xmlscomparator.xml_diff import create_xml_diff_from_strings
from xmlscomparator.comparators.type_comparator import TypeComparator
from xmlscomparator.comparators.text_comparator import TextComparator
from xmlscomparator.comparators.attr_comparator_policy import AttrComparatorPolicy
from xmlscomparator.comparators.attr_comparator import AttrComparator
from tests import logging_configuration as lc


class TestXmlDiff(TestCase):
    def setUp(self):
        self._string1 = '''<?xml version="1.0" encoding="utf-8"?><xmap-content timestamp="1518966212347" version="2.0" 
        xmlns="urn:xmind:xmap:xmlns:content:2.0" xmlns:fo="http://www.w3.org/1999/XSL/Format" 
        xmlns:svg="http://www.w3.org/2000/svg" xmlns:xhtml="http://www.w3.org/1999/xhtml" 
        xmlns:xlink="http://www.w3.org/1999/xlink"><sheet id="e8ce5ccae982254842c225a9bc" 
        timestamp="1518966212346"><topic id="9d97ff161d84ff380923e88eab"><title>we don't care of this 
        sheet</title></topic><title>first sheet</title></sheet><sheet id="9d97ff161d84fdc62754c41a26" 
        timestamp="1518966212346"><topic id="9d97ff161d84f5602a926e7edc"><title>root node</title><children><topics 
        type="attached"><topic id="98337a9525c4ea88cc2fe378fb" 
        xlink:href="xmind:#e8ce5ccae982254842c225a9bc"><title>redirection to the first 
        sheet</title><marker-refs><marker-ref marker-id="yes"/></marker-refs></topic><topic 
        id="98337a9525c4ef8d2f97663d60" xlink:href="https://xmind.net"><title>second 
        node</title><marker-refs><marker-ref marker-id="yes"/></marker-refs></topic><topic 
        id="98337a9525c4e8589c01243516"><title>topic with notes</title><notes><plain>notes for this 
        topic</plain></notes><marker-refs><marker-ref marker-id="yes"/></marker-refs></topic><topic 
        id="98337a9525c4e428e46c43f11a" xlink:href="file://C:\\Users\\z4i\\projects\\home\\xmind-sdk-python\\logo.jpeg
        "><title>topic with a file</title><marker-refs><marker-ref 
        marker-id="yes"/></marker-refs></topic></topics></children></topic><title>second 
        sheet</title><relationships><relationship end1="98337a9525c4ea88cc2fe378fb" end2="98337a9525c4ef8d2f97663d60" 
        id="98337a9525c4ed0c9cfc61dac6" timestamp="1518966212347"><title>test</title></relationship></relationships
        ></sheet></xmap-content>'''
        self._string2 = '''<?xml version="1.0" encoding="utf-8"?><xmap-content timestamp="1518969107322" version="2.0" 
        xmlns="urn:xmind:xmap:xmlns:content:2.0" xmlns:fo="http://www.w3.org/1999/XSL/Format" 
        xmlns:svg="http://www.w3.org/2000/svg" xmlns:xhtml="http://www.w3.org/1999/xhtml" 
        xmlns:xlink="http://www.w3.org/1999/xlink"><sheet id="f4a44c181f4576a54dbdf0e9e7" 
        timestamp="1518969107321"><topic id="f4a44c181f45734f3759fa0888"><title>we don't care of this 
        sheet</title></topic><title>first sheet</title></sheet><sheet id="f4a44c181f457625320c35f6c0" 
        timestamp="1518969107321"><topic id="f4a44c181f4571c9e1be58b0da"><title>root node</title><children><topics 
        type="attached"><topic id="f4a44c181f45799cc1b19ab040" 
        xlink:href="xmind:#f4a44c181f4576a54dbdf0e9e7"><title>redirection to the first 
        sheet</title><marker-refs><marker-ref marker-id="yes"/></marker-refs></topic><topic 
        id="f4a44c181f457a3e25ef8a098f" xlink:href="https://xmind.net"><title>second 
        node</title><marker-refs><marker-ref marker-id="yes"/></marker-refs></topic><topic 
        id="f4a44c181f4577e3412a79221e"><title>topic with notes</title><notes><plain>notes for this 
        topic</plain></notes><marker-refs><marker-ref marker-id="yes"/></marker-refs></topic><topic 
        id="f4a44c181f45732d612a57f4f5" xlink:href="file://C:\\Users\\z4i\\projects\\home\\xmind-sdk-python\\logo
        .jpeg"><title>topic with a file</title><marker-refs><marker-ref 
        marker-id="yes"/></marker-refs></topic></topics></children></topic><title>second 
        sheet</title><relationships><relationship end1="f4a44c181f45799cc1b19ab040" end2="f4a44c181f457a3e25ef8a098f" 
        id="8cf7f50cf2e36a1c84547ac9b8" timestamp="1518969107322"><title>test</title></relationship></relationships
        ></sheet></xmap-content> '''

    def test_parse_file(self):
        _type_comparator = TypeComparator(lc.get_logger('type'))
        _text_comparator = TextComparator(lc.get_logger('text'))
        _attr_comparator = AttrComparator(lc.get_logger('attr_comparator'))
        _attr_policy = AttrComparatorPolicy(
            lc.get_logger('attr_comparator_policy'))
        _attr_policy.add_attribute_name_to_compare('marker-id')
        _attr_policy.add_attribute_name_to_compare('type')
        _attr_comparator.set_attr_comparator_policy(_attr_policy)
        _attr_comparator.set_check_values(True)
        _text_comparator.set_next_comparator(_attr_comparator)
        _type_comparator.set_next_comparator(_text_comparator)
        _comparator = create_xml_diff_from_strings(
            self._string1,
            self._string2,
            lc.get_logger('%s.%s' % (__name__, self._testMethodName)))
        _comparator.set_comparator(_type_comparator)
        self.assertTrue(_comparator.compare(depth=9))

    def test_compare_different_xmls_without_set_comparator(self):
        _comparator = create_xml_diff_from_strings(
            self._string1,
            self._string2,
            lc.get_logger('%s.%s' % (__name__, self._testMethodName)))
        self.assertTrue(_comparator.compare())
