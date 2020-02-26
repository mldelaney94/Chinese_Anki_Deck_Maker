total_set = set()
with open('TOCFL_bigrams_L01c.txt', 'r') as l1:
    for line in l1:
        liness = line.split('\t')
        if '/' in liness[0]:
            elem_split = liness[0].split('/')
            elem_split[0] = elem_split[0] + ' 1'
            elem_split[1] = elem_split[1] + ' 1'
            total_set.add(elem_split[0])
            total_set.add(elem_split[1])
        else:
            liness[0] = liness[0] + ' 1'
            total_set.add(liness[0])

with open('TOCFL_bigrams_L02c.txt', 'r') as l2:
    for line in l2:
        liness = line.split('\t')
        if '/' in liness[0]:
            elem_split = liness[0].split('/')
            elem_split[0] = elem_split[0] + ' 2'
            elem_split[1] = elem_split[1] + ' 2'
            total_set.add(elem_split[0])
            total_set.add(elem_split[1])
        else:
            liness[0] = liness[0] + ' 2'
            total_set.add(liness[0])

with open('TOCFL_bigrams_L03c.txt', 'r') as l3:
    for line in l3:
        liness = line.split('\t')
        if '/' in liness[0]:
            elem_split = liness[0].split('/')
            elem_split[0] = elem_split[0] + ' 3'
            elem_split[1] = elem_split[1] + ' 3'
            total_set.add(elem_split[0])
            total_set.add(elem_split[1])
        else:
            liness[0] = liness[0] + ' 3'
            total_set.add(liness[0])

with open('TOCFL_bigrams_L04c.txt', 'r') as l4:
    for line in l4:
        liness = line.split('\t')
        if '/' in liness[0]:
            elem_split = liness[0].split('/')
            elem_split[0] = elem_split[0] + ' 4'
            elem_split[1] = elem_split[1] + ' 4'
            total_set.add(elem_split[0])
            total_set.add(elem_split[1])
        else:
            liness[0] = liness[0] + ' 4'
            total_set.add(liness[0])


with open('TOCFL_bigrams_L05c.txt', 'r') as l5:
    for line in l5:
        liness = line.split('\t')
        if '/' in liness[0]:
            elem_split = liness[0].split('/')
            elem_split[0] = elem_split[0] + ' 5'
            elem_split[1] = elem_split[1] + ' 5'
            total_set.add(elem_split[0])
            total_set.add(elem_split[1])
        else:
            liness[0] = liness[0] + ' 5'
            total_set.add(liness[0])

edited_set = set()
while(total_set):
    elem = total_set.pop()
    elem = elem + '\n'
    edited_set.add(elem)

with open('TOCFL_1-5.txt', 'w+') as n:
    for elem in edited_set:
        n.write(elem)
