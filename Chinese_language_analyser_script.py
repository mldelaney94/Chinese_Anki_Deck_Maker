#This script takes a Chinese text document and creates a list of words in the document. The words definitions, pinyin and word frequency is added
#You can choose to ignore words for import that are above a certain frequency
#Matthew Delaney 2020

import os
import sys
import jieba
import cc_cedict_parser
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
        seg_set.add(elem)
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
        elem_split = elem.split(' ')
        if elem_split[0] in zh_dict:
            attrib_list = zh_dict[elem_split[0]]
            addition = elem_split[0] + '\t'
            for attrib in attrib_list:
                if attrib_list.index(attrib) == 0: #simplified
                    continue
                elif attrib_list.index(attrib) == 1: #pinyin
                    addition += str(attrib) + '\t'
                else:
                    addition += str(attrib) + ';'
            hpe_set.add(addition)
    return hpe_set

def add_frequencies(seg_set):
    freq_set = set()
    while(seg_set):
        elem = seg_set.pop()
        ssplit = elem.split('\t')
        freq = zipf_frequency(ssplit[0], 'zh', wordlist='large')
        elem += '\t' + str(freq)
        freq_set.add(elem)
    return freq_set
    
def add_parts_of_speech(seg_set):
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

def main(f, quiet):
    zh_dict = cc_cedict_parser.parse_dict('trad')
    jieba.set_dictionary('jieba_dict_large.txt')
    
    seg_set = segment_NLP(f)
    seg_set = add_pinyin_and_definition(seg_set, zh_dict)
    seg_set = add_frequencies(seg_set)
    seg_set = add_parts_of_speech(seg_set)
    seg_set = add_newlines(seg_set)

    save_generated_set(seg_set, sys.argv[2])

if __name__ == "__main__":
    #walk through optional args
    quiet = False
    for arg in sys.argv:
        if '-q' in arg:
            quiet = True

    f = open (sys.argv[1], 'r')
    main(f, quiet)
    f.close()

