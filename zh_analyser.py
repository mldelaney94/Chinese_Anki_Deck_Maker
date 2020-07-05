"""This script takes a Chinese text document and creates a list of words in the
document. The words definitions, pinyin and word frequency is added
You can choose to ignore words for import that are above a certain frequency,
or below a certain level on the HSK or TOCFL test
Matthew Delaney 2020"""

import sys
from operator import itemgetter

import jieba
from more_itertools import unique_everseen
import pynlpir
from wordfreq import zipf_frequency

from materials.cc_cedict_materials import cc_cedict_parser

def segment_NLP(in_file):
    """ Segments zh input using Jieba NLP, returns a list of lists with the
    words as their first entries """
    word_list = []
    with open(in_file, 'r') as g:
        for line in g:
            word_list += jieba.cut(line, cut_all=False) #accurate mode
    word_list = list(unique_everseen(word_list)) #mimic set uniqueness in list,
    #unknown if list(set(word_list)) is faster but this does keep ordering
    word_list = [[el] for el in word_list] #each word will be its own list with
    #definition and pinyin added as items to the word
    return word_list

def add_pinyin_and_definition(word_list, zh_dict):
    """Adds pinyin and definition from zh_dict to entries in hanzi_set. Adds
    english definition as a list of items"""
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
                    if EXCLUDE_SURNAME_DEFINITION and 'surname' in attrib:
                        pass
                    else:
                        english_translation_list.append(attrib)
            word.append(english_translation_list)
    word_list = [word for word in word_list if len(word) > 2] #removes all
    #words that where not found in the dictionary
    return word_list

def filter_by_freq(word_list):
    """Filters words based on their relative frequency, always adds frequency
    to the word list"""
    if not FREQ_FILTERING and not ADD_FREQ_TO_OUTPUT: #TODO figure out freq_filtering - this function has
        #two responsibilities - freq filtering, and then adding freq to word
        return word_list
    filtered_word_list = []
    for word in word_list:
        freq = zipf_frequency(word[0], 'zh', wordlist='large', minimum=0.0)
        if FREQ_FILTERING:
            if LOWER_FREQ_BOUND <= freq <= UPPER_FREQ_BOUND:
                if ADD_FREQ_TO_OUTPUT:
                    word.append(freq)
                filtered_word_list.append(word)
        else:
            if ADD_FREQ_TO_OUTPUT:
                word.append(freq)
            filtered_word_list.append(word)
    return filtered_word_list

def add_parts_of_speech(word_list):
    """Parts of speech such as noun, verb will be added to entries where available"""
    if not ADD_POS_TO_OUTPUT:
        return word_list
    pynlpir.open()
    for word in word_list:
        pos = pynlpir.segment(word[0], pos_tagging=True, pos_names='all',
                              pos_english=True)
        pos = pos[0][1].split(':')
        word.append(pos)
    pynlpir.close()
    return word_list

def remove_hsk_vocab(word_list):
    """Filters HSK vocab"""
    if not HSK_FILTERING:
        return word_list
    hsk_dict = {}
    hsk_removed_list = []
    if SIMP_OR_TRAD == 'trad':
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
        if hanzi in hsk_dict and int(hsk_dict[hanzi]) > HSK_LEVEL:
            pass
        else:
            hsk_removed_list.append(word)
    return hsk_removed_list

def remove_tocfl_vocab(word_list):
    """filters TOCFL vocab"""
    if not TOCFL_FILTERING:
        return word_list
    tocfl_dict = {}
    tocfl_removed_list = []
    if SIMP_OR_TRAD == 'trad':
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
        if hanzi in tocfl_dict and int(tocfl_dict[hanzi]) > TOCFL_LEVEL:
            pass
        else:
            tocfl_removed_list.append(word)
    return tocfl_removed_list

def sort_by_freq(word_list, ascending):
    if not ADD_FREQ_TO_OUTPUT:
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

def main(f):
    """Parses text and applies filters"""
    cc_cedict_parser.QUIET = True
    zh_dict = cc_cedict_parser.parse_dict(SIMP_OR_TRAD)
    jieba.set_dictionary('materials/dicts/jieba_dict_large.txt')

    word_list = segment_NLP(f)
    word_list = filter_by_freq(word_list)
    word_list = remove_tocfl_vocab(word_list)
    word_list = remove_hsk_vocab(word_list)
    word_list = add_pinyin_and_definition(word_list, zh_dict)
    word_list = add_parts_of_speech(word_list)
    word_list = sort_by_freq(word_list, 0)

    save_generated_list(word_list, sys.argv[2])

if __name__ == "__main__":
    #walk through optional args
    global QUIET, UPPER_FREQ_BOUND, LOWER_FREQ_BOUND, SIMP_OR_TRAD, HSK_LEVEL
    global HSK_FILTERING, TOCFL_LEVEL, TOCFL_FILTERING, ADD_FREQ_TO_OUTPUT
    global FREQ_FILTERING, ADD_POS_TO_OUTPUT, EXCLUDE_SURNAME_DEFINITION
    global SORT_BY_FREQ

    SORT_BY_FREQ = 1
    EXCLUDE_SURNAME_DEFINITION = 1
    ADD_POS_TO_OUTPUT = 1
    HSK_LEVEL = 3 #needs to be one above desired lvl of filtering
    HSK_FILTERING = 1
    TOCFL_LEVEL = 6
    TOCFL_FILTERING = 0
    ADD_FREQ_TO_OUTPUT = 0
    FREQ_FILTERING = 1
    SIMP_OR_TRAD = 'simp'
    QUIET = False
    UPPER_FREQ_BOUND = 8.0
    LOWER_FREQ_BOUND = 0.0

    if len(sys.argv) < 3:
        print("Please give the location of the file to be read and the save" +
              "file location, in that order")

    main(sys.argv[1])
