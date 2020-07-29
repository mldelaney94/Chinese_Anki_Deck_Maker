"""This script takes a Chinese text document and creates a list of words in the
document. The words definitions, pinyin and word frequency is added
You can choose to ignore words for import that are above a certain frequency,
or below a certain level on the HSK or TOCFL test
Matthew Delaney 2020"""

import sys
from operator import itemgetter

import jieba
import jieba.posseg as pseg
from more_itertools import unique_everseen
import pynlpir
from wordfreq import zipf_frequency

from materials.cc_cedict_materials import cc_cedict_parser

def segment_NLP(text):
    """ Segments newline separated zh input using Jieba NLP, returns a list of
    lists with the words as their first entries """
    word_list = []
    for line in text:
        word_list += jieba.cut(line, cut_all=False) #accurate mode
    word_list = list(unique_everseen(word_list)) #mimic set uniqueness in list,
    #unknown if list(set(word_list)) is faster but this does keep ordering
    return [[el] for el in word_list] #each word will be its own list with
    #definition and pinyin added as items to the word

def add_pinyin_and_definition(word_list, zh_dict, include_surname_def,
        include_surname_tag):
    """Adds pinyin and definition from zh_dict to entries in hanzi_set. Adds
    english definition as a list of items"""
    #TODO figure out tags vs def
    for word in word_list:
        english_translation_list = []
        if word[0] in zh_dict:
            attrib_list = zh_dict[word[0]]
            for index, attrib in enumerate(attrib_list):
                if index == 0:
                    pass
                elif index == 1: #pinyin
                    word.append(attrib.lower())
                else: #english
                    if not include_surname_def and 'surname' in attrib:
                        pass
                    else:
                        english_translation_list.append(attrib)
            word.append(english_translation_list)
    word_list = [word for word in word_list if len(word) > 2] #removes all
    #words that where not found in the dictionary
    return word_list

def filter_by_freq(word_list, lower_freq_bound, upper_freq_bound,
        add_freq_to_output):
    """Filters words based on their relative frequency and adds frequency info
    to the wordlist"""
    filtered_word_list = []
    for word in word_list:
        freq = zipf_frequency(word[0], 'zh', wordlist='large', minimum=0.0)
        if lower_freq_bound <= freq <= upper_freq_bound:
            if add_freq_to_output:
                word.append(freq)
            filtered_word_list.append(word)
    return filtered_word_list

def add_parts_of_speech(word_list, add_parts_of_speech):
    """Parts of speech such as noun, verb will be added to entries where available"""
    if not add_parts_of_speech:
        return word_list
    pynlpir.open()
    for word in word_list:
        pos = pynlpir.segment(word[0], pos_tagging=True, pos_names='all',
                              pos_english=True)
        pos = pos[0][1].split(':')
        word.append(pos)
    pynlpir.close()
    return word_list

def remove_hsk_vocab(word_list, hsk_level, simp_or_trad):
    """Filters HSK vocab"""
    hsk_dict = {}
    hsk_removed_list = []
    if simp_or_trad == 'trad':
        with open('materials/HSK_materials/HSK_1-6_trad.txt', 'r') as h:
            for line in h:
                liness = line.split()
                hsk_dict[liness[0]] = liness[1]
    else:
        with open('materials/HSK_materials/HSK_1-6_simp.txt', 'r') as h:
            for line in h:
                liness = line.split()
                hsk_dict[liness[0]] = liness[1]
    for word in word_list:
        hanzi = word[0]
        if hanzi in hsk_dict and int(hsk_dict[hanzi]) <= hsk_level:
            pass
        else:
            hsk_removed_list.append(word)
    return hsk_removed_list

def remove_tocfl_vocab(word_list, tocfl_level, simp_or_trad):
    """filters TOCFL vocab"""
    tocfl_dict = {}
    tocfl_removed_list = []
    if simp_or_trad == 'trad':
        with open('materials/TOCFL_materials/TOCFL_1-5_trad.txt', 'r') as h:
            for line in h:
                liness = line.split()
                tocfl_dict[liness[0]] = liness[1]
    else:
        with open('materials/TOCFL_materials/TOCFL_1-5_simp.txt', 'r') as h:
            for line in h:
                liness = line.split()
                tocfl_dict[liness[0]] = liness[1]
    for word in word_list:
        hanzi = word[0]
        if hanzi in tocfl_dict and int(tocfl_dict[hanzi]) <= tocfl_level:
            pass
        else:
            tocfl_removed_list.append(word)
    return tocfl_removed_list

def sort_by_freq(word_list, ascending, add_freq_to_output):
    if not add_freq_to_output:
        return word_list
    return sorted(word_list, key=itemgetter(1), reverse=ascending)

def save_generated_list(word_list, location):
    with open(location, 'w+') as g:
        for word in word_list:
            for part in word:
                if isinstance(part, list):
                    for elem in part:
                        g.write(str(elem)+'; ')
                    g.write('\t')
                else:
                    g.write(str(part)+'\t')
            g.write('\n')

def analyse(text, sort_by_freq, add_freq_to_output, hsk_level, tocfl_level,
        simp_or_trad, add_parts_of_speech, upper_freq_bound, lower_freq_bound,
        deck_name, zh_input, include_surname_tag, include_surname_def):
    """Parses text and applies filters"""
    cc_cedict_parser.QUIET = True
    zh_dict = cc_cedict_parser.parse_dict(SIMP_OR_TRAD)
    jieba.set_dictionary('materials/dicts/jieba_dict_large.txt')

    word_list = segment_NLP(zh_input)
    word_list = filter_by_freq(word_list, lower_freq_bound, upper_freq_bound, add_freq_to_output)
    word_list = remove_hsk_vocab(word_list, hsk_level, simp_or_trad)
    word_list = remove_tocfl_vocab(word_list, tocfl_level, simp_or_trad)
    word_list = add_pinyin_and_definition(word_list, zh_dict,
            include_surname_def, include_surname_tag)
    word_list = add_parts_of_speech(word_list, add_parts_of_speech)
    word_list = sort_by_freq(word_list, 0, add_freq_to_output)

    save_generated_list(word_list, 'test.txt')

def segment_NLP_test(text):
    """ Segments newline separated zh input using Jieba NLP, returns a list of
    lists with the words as their first entries """
    word_list = []
    word_list = jieba.posseg.lcut(text) #accurate mode
    return word_list

def add_parts_of_speech_test(word_list, add_parts_of_speech):
    if not add_parts_of_speech:
        return word_list
    for word in word_list:
        pos = jieba.posseg.lcut(word[0])
        tag = process_part_of_speech(str(pos[0]).split('/')[1])
        word.append(tag)
    return word_list

def process_part_of_speech(pos):
    """Jieba speech tagging can combine tags in weird ways, this function
    extracts all the different types of tags and returns them as one list"""
    pos_dict = {
            'Ag': 'help', 'a': 'adj', 'ad': 'help', 'an': 'help', 'b':
            'help', 'c': 'conj', 'dg': 'help', 'd': 'adv', 'e': 'exclamation',
            'f': 'noun of locality', 'g': 'morpheme', 'h': 'help', 'i':
            'chengyu', 'j': 'help', 'k': 'help', 'l': 'idiom', 'm': 'numeral',
            'Ng': 'help', 'n': 'noun', 'nr': 'name', 'ns': 'place name',
            'nt': 'help', 'nz': 'help/special', 'o': 'onomatopoeia',
            'p': 'preposition', 'q': 'measure word', 'r': 'pronoun', 's':
            's/f help', 'tg': 'time morpheme', 't': 'time', 'u': 'auxiliary',
            'vg': 'verb morpheme', 'v': 'v', 'vd': 'help', 'vn': 'help', 'w':
            'punctuation', 'x': 'help', 'y': 'modal verb', 'z': 'descriptive word',
            'un': 'unknown'
            }
    if pos in pos_dict:
        return pos_dict[pos]
    
    return 'unknown'

if __name__ == '__main__':
    word_list = segment_NLP('这是，；我的狗狗点一')
    word_list = add_parts_of_speech_test(word_list, 1)
    print(word_list)
