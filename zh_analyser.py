#This script takes a Chinese text document and creates a list of words in the
#document. The words definitions, pinyin and word frequency is added
#You can choose to ignore words for import that are above a certain frequency
#Matthew Delaney 2020

import sys
import jieba
from cc_cedict_materials import cc_cedict_parser
from wordfreq import zipf_frequency
import pynlpir

def segment_NLP(input_file):
    file_list = []
    for line in f:
        line = line.strip(' 「」。: ，')
        file_list += jieba.cut(line, cut_all=False) #accurate mode
    seg_set = set()
    for elem in file_list:
        seg_set.add(elem + '\t')
    #these are stupid discards I made because I couldn't figure out how to
    #programmatically check that its just hanzi yet
    seg_set.discard('Ａ')
    seg_set.discard('Ｑ')
    seg_set.discard('《')
    seg_set.discard('，')
    seg_set.discard('。')
    seg_set.discard('」')
    seg_set.discard('？')
    seg_set.discard('、')
    seg_set.discard('：')
    seg_set.discard('》')
    seg_set.discard('*')
    seg_set.discard('；')
    seg_set.discard('「')
    seg_set.discard('—')
    seg_set.discard('你給')
    seg_set.discard('Ｊ')
    seg_set.discard(' ')
    return seg_set

def add_pinyin_and_definition (h_set, zh_dict):
    hpe_set = set()
    while(h_set):
        elem = h_set.pop()
        elem_split = elem.split('\t')
        if elem_split[0] in zh_dict:
            attrib_list = zh_dict[elem_split[0]]
            eng_attrib_num = 1
            for index, attrib in enumerate(attrib_list):
                if index == 0:
                    pass
                elif index == 1: #pinyin
                    elem += str(attrib) + '\t'
                else: #english
                    if exclude_surname_definition and 'surname' in attrib:
                        pass
                    else:
                        elem += str(eng_attrib_num) + '. ' + str(attrib) + ';'
                        eng_attrib_num += 1
            elem = elem.strip(';')
            hpe_set.add(elem)
    return hpe_set

def add_frequencies_to_card(elem, freq):
    return elem + str(freq) + '\t'

def filter_by_freq(seg_set):
    if not freq_filtering:
        return seg_set
    freq_set = set()
    while(seg_set):
        elem = seg_set.pop()
        ssplit = elem.split('\t')
        freq = zipf_frequency(ssplit[0], 'zh', wordlist='large')
        if freq > lower_freq_bound and freq < upper_freq_bound:
            if add_freq_to_output:
                elem = add_frequencies_to_card(elem, freq)
            freq_set.add(elem)
    return freq_set

    
def add_parts_of_speech(seg_set):
    if not add_pos_to_output:
        return seg_set
    pynlpir.open()
    pos_set = set()
    while(seg_set):
        elem = seg_set.pop()
        elem_split = elem.split('\t')

        pos = pynlpir.segment(elem[0], pos_tagging=True, pos_names='all',
                                pos_english=True)
        pos = pos[0][1].split(':')
        for part in pos:
            elem += '\t' + part
        pos_set.add(elem)
    
    pynlpir.close()
    return pos_set

def remove_hsk_vocab(seg_set):
    if not hsk_filtering:
        return seg_set
    hsk_dict = {}
    hsk_filtered_set = set()
    if simp_or_trad == 'trad':
        with open('HSK_materials/HSK_1-6_trad.txt', 'r') as h:
            for line in h:
                liness = line.split()
                hsk_dict[liness[0]] = liness[1]
    else:
        with open('HSK_materials/HSK_1-6_simp.txt', 'r') as h:
            for line in h:
                liness = line.split()
                hsk_dict[liness[0]] = liness[1]

    #seg_set = [elem for elem in seg_set if elem.split()[0] in hsk_dict and
    #int(hsk_dict[elem.split()[0]]) < hsk_level]
    for elem in seg_set:
        hanzi = elem.split('\t')[0]
        if hanzi in hsk_dict and int(hsk_dict[hanzi]) < hsk_level:
            pass
        else:
            hsk_filtered_set.add(elem)

    return hsk_filtered_set

def remove_tocfl_vocab(seg_set):
    if not tocfl_filtering:
        return seg_set
    tocfl_dict = {}
    tocfl_filtered_set = set()
    if simp_or_trad == 'trad':
        with open('TOCFL_materials/TOCFL_1-5_trad.txt', 'r') as h:
            for line in h:
                liness = line.split()
                tocfl_dict[liness[0]] = liness[1]
    else:
        with open('TOCFL_materials/TOCFL_1-5_simp.txt', 'r') as h:
            for line in h:
                liness = line.split()
                tocfl_dict[liness[0]] = liness[1]

    for elem in seg_set:
        hanzi = elem.split('\t')[0]
        if hanzi in tocfl_dict and int(tocfl_dict[hanzi]) < tocfl_level:
            pass
        else:
            tocfl_filtered_set.add(elem)

    return tocfl_filtered_set


def add_newlines(seg_set):
    newline_set = [elem + '\n' for elem in seg_set]

    return newline_set

def save_generated_set(seg_set, location):
    with open(location, 'w+') as g:
        g.write("".join(seg_set))

def main(f):
    zh_dict = cc_cedict_parser.parse_dict(simp_or_trad)
    jieba.set_dictionary('dicts/jieba_dict_large.txt')
    
    seg_set = segment_NLP(f)
    seg_set = filter_by_freq(seg_set)
    seg_set = remove_tocfl_vocab(seg_set)
    seg_set = remove_hsk_vocab(seg_set)
    seg_set = add_pinyin_and_definition(seg_set, zh_dict)
    seg_set = add_parts_of_speech(seg_set)
    seg_set = add_newlines(seg_set)

    save_generated_set(seg_set, sys.argv[2])

if __name__ == "__main__":
    #walk through optional args
    global quiet, upper_freq_bound, lower_freq_bound, simp_or_trad, hsk_level
    global hsk_filtering, tocfl_level, tocfl_filtering, add_freq_to_output
    global freq_filtering, add_pos_to_output, exclude_surname_definition

    exclude_surname_definition = 1
    add_pos_to_output = 0
    hsk_level = 7 #needs to be one above desired lvl of filtering
    hsk_filtering = 1
    tocfl_level = 6
    tocfl_filtering = 1
    add_freq_to_output = 1
    freq_filtering = 1
    simp_or_trad = 'trad'
    quiet = False
    upper_freq_bound = 3.0
    lower_freq_bound = 0.0

    f = open (sys.argv[1], 'r')
    main(f)
    f.close()
