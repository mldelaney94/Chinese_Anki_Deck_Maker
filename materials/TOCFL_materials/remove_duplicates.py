with open('TOCFL_simp_sorted.txt', 'r') as f:
    d = {}
    for line in f:
        liness = line.split(' ')
        if liness[0] not in d:
            d[liness[0]] = liness[1]

    with open('rem_dupes_simp.txt', 'w+') as g:
        for key in d:
            strra = key + ' ' + d[key]
            g.write(strra)

with open('TOCFL_trad_sorted.txt', 'r') as f:
    d = {}
    for line in f:
        liness = line.split(' ')
        if liness[0] not in d:
            d[liness[0]] = liness[1]

    with open('rem_dupes_trad.txt', 'w+') as g:
        for key in d:
            strra = key + ' ' + d[key]
            g.write(strra)
