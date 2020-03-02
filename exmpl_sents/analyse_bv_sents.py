import jieba
from wordfreq import zipf_frequency
from operator import itemgetter

sorted_sents = []
with open('bv_sents_special.txt', 'r') as f:
    for line in f:
        liness = line.split('\t')
        seg_words = []
        seg_words += jieba.cut(liness[0], cut_all=False) #how generator handles +=?
        total_freq = sum([zipf_frequency(word, 'zh', wordlist='large') for word in seg_words])
        len_seg = sum([1 for word in seg_words])
        total_freq = total_freq / len_seg
        sorted_sents.append((total_freq, line))

sorted_sents.sort(key=itemgetter(0))

with open('bv_sents_freq_sorted.txt', 'w+') as g:
    for tupl in sorted_sents:
        g.write(tupl[1])
