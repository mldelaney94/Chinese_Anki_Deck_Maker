""" Unittests for zh_analyser """

import unittest
import zh_analyser
from materials.cc_cedict_materials import cc_cedict_parser

class TestAnalyser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cc_cedict_parser.QUIET = True
        #All of these tests use traditional characters
        cls.zh_dict = cc_cedict_parser.parse_dict('trad')
        cls.hsk_trad_list = []
        with open('materials/HSK_materials/HSK_1-6_trad.txt', 'r') as h:
            for line in h:
                liness = line.split()
                cls.hsk_trad_list.append([liness[0]])
        cls.hsk_simp_list = []
        with open('materials/HSK_materials/HSK_1-6_simp.txt', 'r') as h:
            for line in h:
                liness = line.split()
                cls.hsk_simp_list.append([liness[0]])
        cls.tocfl_trad_list = []
        with open('materials/TOCFL_materials/TOCFL_1-5_trad.txt', 'r') as h:
            for line in h:
                liness = line.split()
                cls.tocfl_trad_list.append([liness[0]])
        cls.tocfl_simp_list = []
        with open('materials/TOCFL_materials/TOCFL_1-5_simp.txt', 'r') as h:
            for line in h:
                liness = line.split()
                cls.tocfl_simp_list.append([liness[0]])

    def setUp(self):
        self.small_word_list = [['你好'], ['給'], ['個'], ['個哥各也頁']]

    def test_add_pinyin_and_definition_normal_small_trad(self):
        """Tests pinyin and definition is added successfully and that unknown
        words are removed successfully"""
        zh_analyser.ADD_FREQ_TO_OUTPUT = 0
        zh_analyser.EXCLUDE_SURNAME_DEFINITION = 0
        self.assertEqual(zh_analyser.add_pinyin_and_definition([['你好'],
            ['給'], ['個'], ['歌個各']], self.zh_dict),
            [['你好', 'nĭ hăo', ['hello', 'hi']],
            ['給', 'gĕi', ['to', 'for', 'for the benefit of', 'to give', 'to allow', 'to do sth (for sb)', '(grammatical equivalent of 被)', '(grammatical equivalent of 把)',
            '(sentence intensifier)', 'to supply', 'to provide']],
            ['個', 'gè', ['individual', 'this', 'that', 'size', 'classifier for people or objects in general']]])

    def test_add_pinyin_and_definition_normal_small_no_surnames(self):
        """Tests pinyin and definition is added successfully and that unknown
        words are removed successfully"""
        zh_analyser.ADD_FREQ_TO_OUTPUT = 0
        zh_analyser.EXCLUDE_SURNAME_DEFINITION = 1
        self.assertEqual(zh_analyser.add_pinyin_and_definition([['丁']],
            self.zh_dict), [['丁', 'dīng', ['fourth of the ten Heavenly Stems 十天干[shí tiān gān]',
                'fourth in order', 'letter "D" or Roman "IV" in list "A, B, C", or "I, II, III" etc',
                'ancient Chinese compass point: 195°', 'butyl', 'cubes (of food)']]])


    def test_filter_by_freq_normal(self):
        zh_analyser.UPPER_FREQ_BOUND = 8.0
        zh_analyser.LOWER_FREQ_BOUND = 0.0
        zh_analyser.FREQ_FILTERING = 1
        zh_analyser.ADD_FREQ_TO_OUTPUT = 1
        self.assertEqual(zh_analyser.filter_by_freq(self.small_word_list),
            [['你好', 3.88], ['給', 6.19], ['個', 6.5],
            ['個哥各也頁', 0.47]])

    def test_filter_by_freq_small_bounds(self):
        zh_analyser.UPPER_FREQ_BOUND = 6.0
        zh_analyser.LOWER_FREQ_BOUND = 3.0
        zh_analyser.FREQ_FILTERING = 1
        zh_analyser.ADD_FREQ_TO_OUTPUT = 1
        self.assertEqual(zh_analyser.filter_by_freq(self.small_word_list),
            [['你好', 3.88]])

    def test_filter_by_freq_small_bounds_no_add_freq_output(self):
        zh_analyser.UPPER_FREQ_BOUND = 6.0
        zh_analyser.LOWER_FREQ_BOUND = 3.0
        zh_analyser.FREQ_FILTERING = 1
        zh_analyser.ADD_FREQ_TO_OUTPUT = 0
        self.assertEqual(zh_analyser.filter_by_freq(self.small_word_list),
            [['你好']])

    def test_filter_by_freq_turned_off(self):
        zh_analyser.FREQ_FILTERING = 0
        zh_analyser.ADD_FREQ_TO_OUTPUT = 0
        self.assertEqual(zh_analyser.filter_by_freq(self.small_word_list),
            self.small_word_list)

    def test_filter_by_freq_add_freq_bounds_no_filtering(self):
        zh_analyser.UPPER_FREQ_BOUND = 6.0
        zh_analyser.LOWER_FREQ_BOUND = 3.0
        zh_analyser.FREQ_FILTERING = 0
        zh_analyser.ADD_FREQ_TO_OUTPUT = 1
        self.assertEqual(zh_analyser.filter_by_freq(self.small_word_list),
            [['你好', 3.88], ['給', 6.19], ['個', 6.5],
            ['個哥各也頁', 0.47]])

    def test_add_parts_of_speech_to_output(self):
        zh_analyser.ADD_POS_TO_OUTPUT = True
        self.assertEqual(zh_analyser.add_parts_of_speech(self.small_word_list), [['你好', ['pronoun', 'personal pronoun']],
                ['給', ['noun']], ['個', ['noun']], ['個哥各也頁', ['noun']]])

    def test_add_parts_of_speech_do_not_add(self):
        zh_analyser.ADD_POS_TO_OUTPUT = False
        self.assertEqual(zh_analyser.add_parts_of_speech(self.small_word_list),
                self.small_word_list)

    def test_sort_by_freq_freq_descending(self):
        """Relies on [1] containing frequency int from 'filter_by_freq'"""
        zh_analyser.FREQ_FILTERING = 0
        zh_analyser.ADD_FREQ_TO_OUTPUT = 1
        self.small_word_list = zh_analyser.filter_by_freq(self.small_word_list)
        self.assertEqual(zh_analyser.sort_by_freq(self.small_word_list, 1),
            [['個', 6.5], ['給', 6.19], ['你好', 3.88], ['個哥各也頁', 0.47]])
    
    def test_sort_by_freq_ascending(self):
        """Relies on [1] containing frequency int from 'filter_by_freq'"""
        zh_analyser.FREQ_FILTERING = 0
        zh_analyser.ADD_FREQ_TO_OUTPUT = 1
        self.small_word_list = zh_analyser.filter_by_freq(self.small_word_list)
        self.assertEqual(zh_analyser.sort_by_freq(self.small_word_list, 0),
            [['個哥各也頁', 0.47], ['你好', 3.88], ['給', 6.19], ['個', 6.5]])

    def test_remove_trad_hsk_vocab_remove_all(self):
        zh_analyser.SIMP_OR_TRAD = 'trad'
        zh_analyser.HSK_LEVEL = 6
        zh_analyser.HSK_FILTERING = 1
        self.assertEqual(zh_analyser.remove_hsk_vocab(self.hsk_trad_list), [])
    
    def test_remove_simp_hsk_vocab_remove_all(self):
        zh_analyser.SIMP_OR_TRAD = 'simp'
        zh_analyser.HSK_LEVEL = 6
        zh_analyser.HSK_FILTERING = 1
        self.assertEqual(zh_analyser.remove_hsk_vocab(self.hsk_simp_list), [])

    def test_remove_trad_tocfl_vocab_remove_all(self):
        zh_analyser.SIMP_OR_TRAD = 'trad'
        zh_analyser.TOCFL_LEVEL = 5
        zh_analyser.TOCFL_FILTERING = 1
        self.assertEqual(zh_analyser.remove_tocfl_vocab(self.tocfl_trad_list), [])
    
    def test_remove_simp_tocfl_vocab_remove_all(self):
        zh_analyser.SIMP_OR_TRAD = 'simp'
        zh_analyser.TOCFL_LEVEL = 5
        zh_analyser.TOCFL_FILTERING = 1
        self.assertEqual(zh_analyser.remove_tocfl_vocab(self.tocfl_simp_list), [])

    def test_remove_trad_hsk_vocab_remove_none(self):
        zh_analyser.SIMP_OR_TRAD = 'trad'
        zh_analyser.HSK_LEVEL = 0
        zh_analyser.HSK_FILTERING = 1
        self.assertEqual(zh_analyser.remove_hsk_vocab(self.hsk_trad_list),
                self.hsk_trad_list)
    
    def test_remove_simp_hsk_vocab_remove_none(self):
        zh_analyser.SIMP_OR_TRAD = 'simp'
        zh_analyser.HSK_LEVEL = 0
        zh_analyser.HSK_FILTERING = 1
        self.assertEqual(zh_analyser.remove_hsk_vocab(self.hsk_simp_list),
                self.hsk_simp_list)

    def test_remove_trad_tocfl_vocab_remove_none(self):
        zh_analyser.SIMP_OR_TRAD = 'trad'
        zh_analyser.TOCFL_LEVEL = 0
        zh_analyser.TOCFL_FILTERING = 1
        self.assertEqual(zh_analyser.remove_tocfl_vocab(self.tocfl_trad_list),
                self.tocfl_trad_list)
    
    def test_remove_simp_tocfl_vocab_remove_none(self):
        zh_analyser.SIMP_OR_TRAD = 'simp'
        zh_analyser.TOCFL_LEVEL = 0
        zh_analyser.TOCFL_FILTERING = 1
        self.assertEqual(zh_analyser.remove_tocfl_vocab(self.tocfl_simp_list),
                self.tocfl_simp_list)

if __name__ == "__main__":
    unittest.main()
