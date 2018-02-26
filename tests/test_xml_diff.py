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

    def test_compare_using_types_to_skip(self):
        _file_without_extensions_type = '''<?xml version="1.0" encoding="utf-8"?><xmap-content 
        timestamp="1519684001388" version="2.0" xmlns="urn:xmind:xmap:xmlns:content:2.0" 
        xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:svg="http://www.w3.org/2000/svg" 
        xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:xlink="http://www.w3.org/1999/xlink"><sheet 
        id="5e8351d742b62c651c0428d6ba" timestamp="1519684001385"><topic 
        id="7fd07499279a1a4770765aaad0"><title>Scenarios</title><children><topics type="attached"><topic 
        id="7fd07499279a1b9a69df33286e"><title>Dialtone</title><children><topics type="attached"><topic 
        id="7fd07499279a1c6ebf063138ae"><title>behind the jail (80%)</title><children><topics type="attached"><topic 
        id="7fd07499279a1e3ec3a424c5e1" xlink:href="https://domoreexp.visualstudio.com/MSTeams/_queries?id=222450&amp
        ;fullScreen=false&amp;_a=edit"><title>create_one_to_one_call</title></topic><topic 
        id="7fd07499279a16ef56c97bdb2a" xlink:href="https://domoreexp.visualstudio.com/MSTeams/_workitems/edit/221727
        "><title>join_or_create_meetup_from_link</title></topic></topics></children></topic><topic 
        id="7fd07499279a144074424fb3a2"><title>normal one (90%)</title><children><topics type="attached"><topic 
        id="7fd07499279a127ed388340f44"><title>media_connected</title></topic><topic 
        id="7fd07499279a167f621115cf04"><title>create_meetup</title></topic><topic 
        id="7fd07499279a1b6a0d45d88bb7"><title>join_meetup_reply_chain</title></topic><topic 
        id="7fd07499279a1600b48b035e4d"><title>join_scheduled_meetup</title></topic><topic 
        id="7fd07499279a157b1937e10610"><title>call_accept</title></topic></topics></children></topic></topics
        ></children></topic><topic id="fa2e675a4fd514cc5771fc15d9"><title>Optimal</title><children><topics 
        type="attached"><topic id="fa2e675a4fd510903640cf9c21"><title>get_meeting_info</title></topic><topic 
        id="fa2e675a4fd512dfb2efa69f84"><title>get_exchange_meeting_info</title></topic><topic 
        id="fa2e675a4fd518460078d87e9e"><title>start_recording</title></topic><topic 
        id="fa2e675a4fd51a44e17c5cf053"><title>stop_recording???</title></topic></topics></children></topic><topic 
        id="fa2e675a4fd5117b167087e3a1"><title>Core</title><children><topics type="attached"><topic 
        id="fa2e675a4fd51a71bb77c05261"><title>behind the jail (85% threshold)</title><children><topics 
        type="attached"><topic id="fa2e675a4fd51a9316c057a0aa"><title>add_participant</title></topic><topic 
        id="fa2e675a4fd5191d2f636c794c"><title>create_group_call</title></topic><topic 
        id="fa2e675a4fd51c5369f5fff0da"><title>join_group_call</title></topic></topics></children></topic><topic 
        id="fa2e675a4fd51a93c539c22937"><title>normal one (90% threshold)</title><children><topics 
        type="attached"><topic id="fa2e675a4fd51cf49d6b3c027d"><title>screen_sharing_sender_end</title></topic><topic 
        id="fa2e675a4fd51bad4daec953cb"><title>start_video</title></topic><topic 
        id="fa2e675a4fd5130fe1fdfacaf8"><title>stop_video</title></topic><topic 
        id="fa2e675a4fd5108a76d9c696e0"><title>video_stream_rendering</title></topic><topic 
        id="fa2e675a4fd512d36681254169"><title>screen_sharing_sender</title></topic><topic 
        id="fa2e675a4fd51814656bcaa5e4"><title>join_or_create_call_from_link</title></topic><topic 
        id="fa2e675a4fd5185d775441e580"><title>calling_service_init</title></topic><topic 
        id="fa2e675a4fd515baae918c4f66"><title>calling_relay_manager_query_relays_async</title></topic><topic 
        id="fa2e675a4fd5156ee525942dff"><title>ecs_config_request</title></topic><topic 
        id="fa2e675a4fd51a1efb00e4fa1f"><title>add_pstn_participant</title></topic><topic 
        id="fa2e675a4fd51b19a27efc9ec5"><title>call_me_back</title></topic><topic 
        id="fa2e675a4fd51786b8157dfec3"><title>calling_mute_participant</title></topic><topic 
        id="fa2e675a4fd5183ea82634c6be"><title>server_unmute_self</title></topic><topic 
        id="fa2e675a4fd5179d867efb3bfb"><title>calling_mute_all</title></topic></topics></children></topic></topics
        ></children></topic></topics></children></topic><title>Scenarios</title></sheet></xmap-content> '''

        _file_with_extensions_type = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?><xmap-content 
        xmlns="urn:xmind:xmap:xmlns:content:2.0" xmlns:fo="http://www.w3.org/1999/XSL/Format" 
        xmlns:svg="http://www.w3.org/2000/svg" xmlns:xhtml="http://www.w3.org/1999/xhtml" 
        xmlns:xlink="http://www.w3.org/1999/xlink" modified-by="vlads" timestamp="1519679574500" 
        version="2.0"><extensions><extension provider="org.xmind.ui.presentation.stories"/></extensions><sheet 
        id="2ik7rm8o7e9hq3a2glv89mu5s3" modified-by="ankozin" theme="65et4tbn548nr5o54og1bhmv4m" 
        timestamp="1517910735978"><topic id="23flpmdjijals51tsngios4emm" modified-by="z4i" 
        structure-class="org.xmind.ui.map.unbalanced" 
        timestamp="1516718724400"><title>Scenarios</title><extensions><extension 
        provider="org.xmind.ui.map.unbalanced"><content><right-number>1</right-number></content></extension
        ></extensions><children><topics type="attached"><topic id="1g9hctbcnkebo6hp17337hceuu" modified-by="z4i" 
        timestamp="1516718597044"><title>Core</title><children><topics type="attached"><topic 
        id="7p82ng0j6hmn5m0btrelbm7q96" modified-by="z4i" timestamp="1516718607813"><title>behind the jail (85% 
        threshold)</title><children><topics type="attached"><topic id="76n8ln0hlso2fgpks1cbsbdgdq" modified-by="z4i" 
        timestamp="1516718577888"><title>add_participant</title></topic><topic id="4dh9it878f263je0skpgkvtjsq" 
        modified-by="z4i" timestamp="1516718588184"><title>create_group_call</title></topic><topic 
        id="79rlu1r9k810j8d78j2jik9ap9" modified-by="z4i" 
        timestamp="1516718588184"><title>join_group_call</title></topic></topics></children></topic><topic 
        id="340g05u8jhrfe4thilllpdl3rp" modified-by="z4i" timestamp="1516718624530"><title>normal one (90% 
        threshold)</title><children><topics type="attached"><topic id="0ai4cb1g54ojf03aijsfmg4q5m" modified-by="z4i" 
        timestamp="1516718598460"><title>screen_sharing_sender_end</title></topic><topic 
        id="2p1mkup1n3ud093d85tcc9mcog" modified-by="z4i" 
        timestamp="1516718598460"><title>start_video</title></topic><topic id="19iak61tudilcbl11bce3h6a7j" 
        modified-by="z4i" timestamp="1516718598460"><title>stop_video</title></topic><topic 
        id="2n831abrved4fjlaa9fi6pc9sm" modified-by="z4i" 
        timestamp="1516718598460"><title>video_stream_rendering</title></topic><topic id="09qqv53mj5vg2iuab7rioq38mg" 
        modified-by="z4i" timestamp="1516718598460"><title>screen_sharing_sender</title></topic><topic 
        id="16e1m7i3bt27bqcnpaf6q9o62b" modified-by="z4i" 
        timestamp="1516718598460"><title>join_or_create_call_from_link</title></topic><topic 
        id="08duu8ssu2p49n3kka6395on20" modified-by="z4i" 
        timestamp="1516718598460"><title>calling_service_init</title></topic><topic id="3gea736r46bjnjo4ba6t41h1vb" 
        modified-by="z4i" timestamp="1516718598460"><title>calling_relay_manager_query_relays_async</title></topic
        ><topic id="5qk2d4dsf4o03e5sfipsb8sa1k" modified-by="z4i" 
        timestamp="1516718598460"><title>ecs_config_request</title></topic><topic id="2hlle1hutsfedvpfdv4s36dqvd" 
        modified-by="z4i" timestamp="1516718598460"><title>add_pstn_participant</title></topic><topic 
        id="34a822s99q9flrm9dtsjm0pkbe" modified-by="z4i" 
        timestamp="1516718598460"><title>call_me_back</title></topic><topic id="6p663gf3ukpq7fe2u900n9361n" 
        modified-by="z4i" timestamp="1516718598460"><title>calling_mute_participant</title></topic><topic 
        id="42a4tvu1nbqg8oevr9li34664h" modified-by="z4i" 
        timestamp="1516718598460"><title>server_unmute_self</title></topic><topic id="4ekogfooarskbd4tf9543212nv" 
        modified-by="z4i" timestamp="1516718598460"><title>calling_mute_all</title></topic></topics></children
        ></topic></topics></children></topic><topic id="3aairf1djgvpn28q22phnmmmq7" modified-by="ankozin" 
        timestamp="1517910730689"><title>Optimal</title><children><topics type="attached"><topic 
        id="50eskd3p03acofgkkrp4uauohp" modified-by="ankozin" 
        timestamp="1513239274039"><title>get_meeting_info</title></topic><topic id="4pctor3nlsdjk3o9h6k247chq0" 
        modified-by="z4i" timestamp="1515434278282"><title>get_exchange_meeting_info</title></topic><topic 
        id="1bjieqbbccgq2puj0hru7t5cqu" modified-by="ankozin" 
        timestamp="1517910705741"><title>start_recording</title></topic><topic id="41l0gk837oajnvpudfdamn7tjt" 
        modified-by="ankozin" timestamp="1517910735978"><title>stop_recording???</title></topic></topics></children
        ></topic><topic id="21igq2ogn5j00047d4qf90hn7l" modified-by="z4i" 
        timestamp="1516718724400"><title>Dialtone</title><children><topics type="attached"><topic 
        id="055i6romc3me1cm0hnlukuje97" modified-by="z4i" timestamp="1516718712355"><title>behind the jail (
        80%)</title><children><topics type="attached"><topic id="2ir3hdg6b3ea232ha4rcron0fb" 
        modified-by="andriikozin" timestamp="1517825520586"><title>create_one_to_one_call</title><children><topics 
        type="attached"><topic id="0c03473n0shgh2c51apugek80a" modified-by="andriikozin" 
        timestamp="1517825520580"><title>https://domoreexp.visualstudio.com/MSTeams/_queries?id=222450&amp;fullScreen
        =false&amp;_a=edit</title></topic></topics></children></topic><topic id="6k7c1t81c9fhbd5eobiqj1dqdn" 
        modified-by="z4i" timestamp="1517232430563"><title>join_or_create_meetup_from_link</title><children><topics 
        type="attached"><topic id="1tt7gfadf0nda4s7to96eo02vb" modified-by="z4i" 
        timestamp="1517232430555"><title>https://domoreexp.visualstudio.com/MSTeams/_workitems/edit/221727</title
        ></topic></topics></children></topic></topics></children></topic><topic id="45lk3k84qqahq5v4b058bofimc" 
        modified-by="z4i" timestamp="1516718725613"><title>normal one (90%)</title><children><topics 
        type="attached"><topic id="7h41ek121jl1j6iocrvp8dlqnk" modified-by="z4i" 
        timestamp="1516718725587"><title>media_connected</title></topic><topic id="0g29pdps8ae7u5ffefmkn0vgc1" 
        modified-by="z4i" timestamp="1516718725587"><title>create_meetup</title></topic><topic 
        id="0eo71r0f0sinqksqk9m782ekot" modified-by="z4i" 
        timestamp="1516718725587"><title>join_meetup_reply_chain</title></topic><topic 
        id="2ogccs8qb007aeqc1kfbhcm6l7" modified-by="z4i" 
        timestamp="1516718725587"><title>join_scheduled_meetup</title></topic><topic id="7h9evf8nud676lip8nic05os7l" 
        modified-by="z4i" timestamp="1516718725587"><title>call_accept</title></topic></topics></children></topic
        ></topics></children></topic></topics></children></topic><title>Scenarios</title></sheet></xmap-content> '''

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
            _file_without_extensions_type,
            _file_with_extensions_type,
            lc.get_logger('%s.%s' % (__name__, self._testMethodName)))
        _comparator.set_comparator(_type_comparator)
        self.assertTrue(_comparator.compare(depth=9))