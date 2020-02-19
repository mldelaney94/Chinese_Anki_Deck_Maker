import jieba
from pypinyin import pinyin
import cc_cedict_parser

f = open('活著 - 第一章.txt', 'r')
jieba.set_dictionary('dict.txt')

def segment_NLP(input_file):
    file_list = []
    for line in f:
        line = line.strip()
        line = line.strip('「」。: ，')
        file_list += jieba.cut(line, cut_all=False) #accurate mode
    seg_set = set()
    for elem in file_list:
        seg_set.add(elem)
    #these are stupid discards I made because I couldn't figure out how to programmatically check its just hanzi yet
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

#takes items from hanzi_set and add to hanzi_pinyin_set (hp_set)
def add_pinyin(h_set):
    hp_set = set()
    while(h_set):
        elem = h_set.pop()
        elem += ' ' #want space between character and pinyin, but not between every pinyin
        pinyin_of_elem = pinyin(elem, errors='ignore')
        
        for pinyin_list in pinyin_of_elem: #pinyin gives us a list of lists
            for specific_pinyin in pinyin_list:
                elem += specific_pinyin

        hp_set.add(elem)
    return hp_set

#take from hp_set and add to hanzi_pinyin_english_set
def add_translation(hp_set):
    parsed_dict = cc_cedict_parser.parse_dict()
    hpe_set = set()
    while(hp_set):
        elem = hp_set.pop()
        elem += ' '
        elem_split = elem.split(' ')
        for item in parsed_dict:
            if item['traditional'] == elem_split[0]:
                elem += item['english']
                hpe_set.add(elem)
    return hpe_set

def add_translation_and_pinyin(h_set):
    hpe_set = set()
    parsed_dict = cc_cedict_parser.parse_dict()
    while(h_set):
        elem = h_set.pop()
        elem_split = elem.split(' ')
        for item in parsed_dict:
            if item['traditional'] == elem_split[0]:
                elem += ' ' #want space between character and pinyin, but not between every pinyin
                for pinyin_list in pinyin(elem, errors='ignore'): #pinyin gives us a list of lists
                    for specific_pinyin in pinyin_list:
                        elem += specific_pinyin + ' '
                elem += item['english']
                hpe_set.add(elem)
        hpe_set.add(elem)
    return hpe_set


def create_anki_deck(seg_set, location):
    with open(location, 'w+') as g:
        g.write(" ".join(seg_set))

seg_set = segment_NLP(f)
seg_set = add_translation_and_pinyin(seg_set)
#seg_set = add_pinyin(seg_set)
#seg_set = add_translation(seg_set)
print(seg_set)

#create_anki_deck(seg_set, 'generic_name.txt')

f.close()
