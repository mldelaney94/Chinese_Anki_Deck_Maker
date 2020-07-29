from operator import itemgetter

with open('TOCFL_1-5_simp.txt', 'r') as f:
    sorted_list = []
    for line in f:
        line = line.strip()
        sorted_list.append(line.split(' '))
    sorted_list = sorted(sorted_list, key=itemgetter(1))

    with open('TOCFL_simp_sorted.txt', 'w+') as g:
        for word in sorted_list:
            g.write(' '.join(word))
            g.write('\n')

with open('TOCFL_1-5_trad.txt', 'r') as f:
    sorted_list = []
    for line in f:
        line = line.strip()
        sorted_list.append(line.split(' '))
    sorted_list = sorted(sorted_list, key=itemgetter(1))

    with open('TOCFL_trad_sorted.txt', 'w+') as g:
        for word in sorted_list:
            g.write(' '.join(word))
            g.write('\n')

