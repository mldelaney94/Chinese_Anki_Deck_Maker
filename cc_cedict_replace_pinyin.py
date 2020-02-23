import sys
from pypinyin import lazy_pinyin, Style

with open('cedict_ts.u8') as file:
    text = file.read()
    lines = text.split('\n')

#define functions

    def parse_lines(lines):
        dictionary = []
        for line in lines:
            if line == '':
                continue

            liness = line.split(' ')
            p_list = lazy_pinyin(liness[0], style=Style.TONE, errors='default')
            p_list.reverse() #will insert in reverse

            s = list(line)
            charCount = 0
            for char in s:
                if char == '[':
                    index = s.index(char)
                    index += 1 #insert/delete at index after '['
                    while s[index] != ']':
                        del(s[index])
                    for pin in p_list:
                        s.insert(index, pin)
                    print(s[index])
            dictionary.append(s)
        return dictionary
        

    def parse_dict():

        #make each line into a dictionary
        print("Parsing dictionary . . .")
        dictionary = parse_lines(lines)
        with open('test.txt', 'w+') as f:
            for line in dictionary:
                to_write = "".join(line) + '\n'
                #print(to_write)
                f.write(to_write)

        return dictionary


if __name__ == "__main__":
    parsed_dict = parse_dict()
    print('Done!')
