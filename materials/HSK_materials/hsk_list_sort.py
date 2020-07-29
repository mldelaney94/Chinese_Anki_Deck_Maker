from operator import itemgetter

with open('HSK_1-6_simp.txt', 'r') as f:
    sorted_list = []
    for line in f:
        line = line.strip()
        sorted_list.append(line.split(' '))
    sorted_list = sorted(sorted_list, key=itemgetter(1))

    with open('HSK_simp_sorted.txt', 'w+') as g:
        for word in sorted_list:
            g.write(' '.join(word))
            g.write('\n')

with open('HSK_1-6_trad.txt', 'r') as f:
    sorted_list = []
    for line in f:
        line = line.strip()
        sorted_list.append(line.split(' '))
    sorted_list = sorted(sorted_list, key=itemgetter(1))

    with open('HSK_trad_sorted.txt', 'w+') as g:
        for word in sorted_list:
            g.write(' '.join(word))
            g.write('\n')

