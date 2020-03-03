import os
import jieba
from profilehooks import profile

class SampleClass:
    def remove_hsk_vocab_create_new(seg_set):
        hsk_dict = {}
        hsk_filtered_set = set()
        if simp_or_trad == 'trad':
            with open('../HSK_materials/HSK_1-6_trad.txt', 'r') as h:
                for line in h:
                    liness = line.split()
                    hsk_dict[liness[0]] = liness[1]
        else:
            with open('HSK_materials/HSK_1-6_simp.txt', 'r') as h:
                for line in h:
                    liness = line.split()
                    hsk_dict[liness[0]] = liness[1]

        #seg_set = [elem for elem in seg_set if elem.split()[0] in hsk_dict and int(hsk_dict[elem.split()[0]]) < hsk_level]
        for elem in seg_set:
            hanzi = elem.split('\t')[0]
            if hanzi in hsk_dict and int(hsk_dict[hanzi]) < hsk_level:
                pass
            else:
                hsk_filtered_set.add(elem)

        return hsk_filtered_set

    def remove_hsk_vocab_discard(seg_set):
        hsk_dict = {}
        if simp_or_trad == 'trad':
            with open('../HSK_materials/HSK_1-6_trad.txt', 'r') as h:
                for line in h:
                    liness = line.split()
                    hsk_dict[liness[0]] = liness[1]
        else:
            with open('HSK_materials/HSK_1-6_simp.txt', 'r') as h:
                for line in h:
                    liness = line.split()
                    hsk_dict[liness[0]] = liness[1]

        #seg_set = [elem for elem in seg_set if elem.split()[0] in hsk_dict and int(hsk_dict[elem.split()[0]]) < hsk_level]
        for elem in seg_set:
            hanzi = elem.split('\t')[0]
            if hanzi in hsk_dict and int(hsk_dict[hanzi]) < hsk_level:
                seg_set.discard(elem)

        return seg_set

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

    def main(input_file, a):
        seg_set = SampleClass.segment_NLP(input_file)
        discard_set = SampleClass.remove_hsk_vocab_discard(seg_set)
        add_set = SampleClass.remove_hsk_vocab_create_new(seg_set)


if __name__ == "__main__":
    global hsk_level
    hsk_level = 6
    global simp_or_trad
    simp_or_trad = 'trad'
    jieba.set_dictionary('../dicts/jieba_dict_large.txt')
    if os.path.isfile('C:\\Users\\Matthew\\dev\\Chinese_Anki_Creator\\chap1.txt'):
        with open('C:\\Users\\Matthew\\dev\\Chinese_Anki_Creator\\chap1.txt', 'r') as f:
            classy = SampleClass()
            classy.main(f)
