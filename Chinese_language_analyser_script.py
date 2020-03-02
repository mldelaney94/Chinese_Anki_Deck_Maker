#This script takes a Chinese text document and creates a list of words in the document. The words definitions, pinyin and word frequency is added
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
        line = line.strip()
        line = line.strip('「」。: ，')
        file_list += jieba.cut(line, cut_all=False) #accurate mode
    seg_set = set()
    for elem in file_list:
        seg_set.add(elem + '\t')
    #these are stupid discards I made because I couldn't figure out how to programmatically check that its just hanzi yet
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
            for attrib in attrib_list:
                if attrib_list.index(attrib) == 0:
                    pass
                elif attrib_list.index(attrib) == 1: #pinyin
                    elem += str(attrib) + '\t'
                else: #english
                    if exclude_surname_definition == 1:
                        if 'surname' in attrib:
                            pass
                        else:
                            elem += str(attrib) + ';'
                    else:
                        elem += str(attrib) + ';'

            hpe_set.add(elem)
    return hpe_set

def add_frequencies(elem, freq):
    elem += str(freq) + '\t'
    return elem

def filter_by_freq(seg_set):
    freq_set = set()
    while(seg_set):
        elem = seg_set.pop()
        ssplit = elem.split('\t')
        freq = zipf_frequency(ssplit[0], 'zh', wordlist='large')
        if freq > lower_freq_bound and freq < upper_freq_bound:
            if add_freq_to_output == 1:
                elem = add_frequencies(elem, freq)
            freq_set.add(elem)
    return freq_set

    
def add_parts_of_speech(seg_set):
    if add_pos_to_output == 0:
        return seg_set
    pynlpir.open()
    pos_set = set()
    while(seg_set):
        elem = seg_set.pop()
        elem_split = elem.split('\t')

        pos = pynlpir.segment(elem[0], pos_tagging=True, pos_names='all', pos_english=True)
        pos = pos[0][1].split(':')
        for part in pos:
            elem += '\t' + part
        pos_set.add(elem)
    
    pynlpir.close()
    return pos_set

def remove_hsk_vocab(seg_set):
    if hsk_filtering == 0:
        return seg_set
    hsk_dict = {}
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

    #seg_set = [elem for elem in seg_set if elem.split()[0] in hsk_dict and hsk_dict[elem.split()[0]] > hsk_level]
    for elem in seg_set:
        hanzi = elem.split('\t')[0]
        if hanzi in hsk_dict and int(hsk_dict[hanzi]) < hsk_level:
            pass
        else:
            seg_set.add(elem)

    return seg_set

def remove_tocfl_vocab(seg_set):
    if tocfl_filtering == 0:
        return seg_set
    tocfl_dict = {}
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

    seg_set = [elem for elem in seg_set if elem.split('\t')[0] in tocfl_dict and int(tocfl_dict[elem.split('\t')[0]]) < tocfl_level]

    return seg_set


def add_newlines(seg_set):
    newline_set = set()
    while(seg_set):
        elem = seg_set.pop()
        elem += '\n'
        newline_set.add(elem)

    return newline_set

def save_generated_set(seg_set, location):
    with open(location, 'w+') as g:
        g.write(" ".join(seg_set))

def main(f):
    zh_dict = cc_cedict_parser.parse_dict(simp_or_trad)
    jieba.set_dictionary('dicts/jieba_dict_large.txt')
    
    seg_set = segment_NLP(f)
    seg_set = filter_by_freq(seg_set)
    seg_set = add_pinyin_and_definition(seg_set, zh_dict)
    seg_set = remove_tocfl_vocab(seg_set)
    seg_set = remove_hsk_vocab(seg_set)
    seg_set = add_parts_of_speech(seg_set)
    seg_set = add_newlines(seg_set)

    save_generated_set(seg_set, sys.argv[2])

if __name__ == "__main__":
    #walk through optional args
    global quiet
    global upper_freq_bound
    global lower_freq_bound
    global simp_or_trad
    global hsk_level
    global hsk_filtering
    global tocfl_level
    global tocfl_filtering
    global add_freq_to_output
    global add_pos_to_output
    global exclude_surname_definition
    exclude_surname_definition = 1
    add_pos_to_output = 0
    hsk_level = 3
    hsk_filtering = 1
    tocfl_level = 1
    tocfl_filtering = 0
    add_freq_to_output = 0
    simp_or_trad = 'trad'
    quiet = False
    upper_freq_bound = 5.0
    lower_freq_bound = 0.0

    f = open (sys.argv[1], 'r')
    main(f)
    f.close()

