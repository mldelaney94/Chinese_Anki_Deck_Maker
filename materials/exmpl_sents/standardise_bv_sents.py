""" The brian_vaughan_sents.txt file has the english, then ';;;' or ';;', then the
pinyin, then a tab, then the hanzi. This simply seeks to make all three parts
tab separated. """

seg_list = []
with open('brian_vaughan_sents.txt', 'r') as f:
    for line in f:
        liness = line.replace(';;;', '\t')
        liness = liness.replace(';;', '\t')

        liness = liness.strip(' ')

        seg_list.append(liness)

with open ('brian_vaughan_sents_special.txt', 'w+') as g:
    for line in seg_list:
        g.write(line)
