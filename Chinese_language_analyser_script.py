import jieba
import sys
from pypinyin import pinyin as Get_Pinyin
import cc_cedict_parser

with open(sys.argv[1]) as f:

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

    def add_translation_and_pinyin(h_set):
        hpe_set = set()
        parsed_dict = cc_cedict_parser.parse_dict()
        while(h_set):
            elem = h_set.pop()
            elem_split = elem.split(' ')
            #okay so this is a terrible algorithm because parsed dicts is a list of dictionarys, and this goes through every single dictionary, checks if the key value traditional is a match
            #
            for item in parsed_dict:
                if item['traditional'] == elem_split[0] or item['simplified'] == elem_split[0]:
                    elem += ',' #anki likes separators other than spaces
                    elem += get_pinyin_from_hanzi(elem) + ','
                    elem += item['english'] + '\n'
                    hpe_set.add(elem)
        return hpe_set

    def get_pinyin_from_hanzi(hanzi):
        pinyin_string = ''
        for pinyin_list in Get_Pinyin(hanzi, errors='ignore'): #pinyin gives us a list of lists
            for specific_pinyin in pinyin_list:
                pinyin_string += specific_pinyin
        return pinyin_string

    def save_generated_set(seg_set, location):
        with open(location, 'w+') as g:
            g.write(" ".join(seg_set))

    def main():
        seg_set = segment_NLP(f)
        seg_set = add_translation_and_pinyin(seg_set)
        save_generated_set(seg_set, sys.argv[2])

if __name__ == "__main__":
    f = open (sys.argv[1], 'r')
    main()
    f.close()

