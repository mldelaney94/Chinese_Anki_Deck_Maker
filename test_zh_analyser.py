""" Unittests for zh_analyser """

import unittest
import zh_analyser
from materials.cc_cedict_materials import cc_cedict_parser

class TestAnalyser(unittest.TestCase):
    def test_add_pinyin_and_definition_normal_small_trad(self):
        """Tests pinyin and definition is added successfully and that unknown
        words are removed successfully"""
        zh_analyser.ADD_FREQ_TO_OUTPUT = 0
        zh_analyser.EXCLUDE_SURNAME_DEFINITION = 0
        self.assertEqual(zh_analyser.add_pinyin_and_definition([['你好'], ['給'], ['個'], ['歌個各']], zh_dict),
                [['你好', 'nĭ hăo', ['hello', 'hi']],
                ['給', 'gĕi', ['to', 'for', 'for the benefit of', 'to give', 'to allow', 'to do sth (for sb)', '(grammatical equivalent of 被)', '(grammatical equivalent of 把)',
                '(sentence intensifier)', 'to supply', 'to provide']],
                ['個', 'gè', ['individual', 'this', 'that', 'size', 'classifier for people or objects in general']]])


    def test_filter_by_freq_normal(self):
        zh_analyser.UPPER_FREQ_BOUND = 8.0
        zh_analyser.LOWER_FREQ_BOUND = 0.0
        zh_analyser.FREQ_FILTERING = 1
        zh_analyser.ADD_FREQ_TO_OUTPUT = 1
        self.assertEqual(zh_analyser.filter_by_freq(small_word_list),
                [['你好', 3.88], ['給', 6.19], ['個', 6.5],
                ['個哥各也頁', 0.47]])

    def test_filter_by_freq_turned_off(self):
        zh_analyser.FREQ_FILTERING = 0
        self.assertEqual(zh_analyser.filter_by_freq(small_word_list), small_word_list)

    def test_filter_by_freq_

        
if __name__ == "__main__":
    small_word_list = [['你好'], ['給'], ['個'], ['個哥各也頁']]

    zh_dict = cc_cedict_parser.parse_dict('trad') #setupclass was not running
    # until end of tests, so wrote it here as a quickfix
    unittest.main()
