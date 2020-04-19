seg_list = []
with open('brian_vaughan_sents.txt', 'r') as f:
    for line in f:
        liness = []
        
        if ';;;' in line:
            continue
        elif ';;' in line:
            liness = line.split(';;')
        
        liness = [elem.strip() for elem in liness]
        line = "\t".join(liness)
        line += '\n'
        
        seg_list.append(line)

with open ('brian_vaughan_sents_special.txt', 'w+') as g:
    for line in seg_list:
        g.write(line)

