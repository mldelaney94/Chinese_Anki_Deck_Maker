with open('HSK_Official_2012_1-6_Sorted.txt', 'r') as f:
    new_file = []
    for line in f:
        line = line.strip()
        if '（一级' in line:
            line = line.replace('（一级）', ' 1')
        elif '（二级' in line:
            line = line.replace('（二级）', ' 2')
        elif '（三级' in line:
            line = line.replace('（三级）', ' 3')
        elif '（四级' in line:
            line = line.replace('（四级）', ' 4')
        elif '（五级' in line:
            line = line.replace('（五级）', ' 5')
        elif '（六级' in line:
            line = line.replace('（六级）', ' 6')
        line += '\n'
        new_file.append(line)


    to_write = open('HSK_edited.txt', 'w+')
    for part in new_file:
        to_write.write(part)
    to_write.close()
