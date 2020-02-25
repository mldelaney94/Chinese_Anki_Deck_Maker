#A parser for the CC-Cedict. Convert the Chinese-English dictionary into a list of python
    #dictionaries with "traditional","simplified", "pinyin", and "english" keys.

#Make sure that the cedict_ts.u8 file is in the same folder as this file, and that the name matches
#the file name on line 13.

#Before starting, open the CEDICT text file and delete the copyright information at the top.
#Otherwise the program will try to parse it and you will get an error message.

#Characters that are commonly used as surnames have two entries in CC-CEDICT. This program will
#remove the surname entry if there is another entry for the character. If you want to include the
#surnames, simply delete lines 59 and 60.

#This code was written by Franki Allegra in February 2020. Edited by Matthew Delaney February 2020
#https://github.com/rubber-duck-dragon/rubber-duck-dragon.github.io/blob/master/cc-cedict_parser/parser.py

#open CEDICT file

import sys

with open('cedict_modified.txt') as file:
    text = file.read()
    lines = text.split('\n')
    dictionary = {}

#define functions

    #builds a dictionary with a trad or simp character as the key
    def parse_lines(lines, key_is_trad_or_simp):
        for line in lines:
            if line == '':
                continue
            line = line.rstrip('/')
            line = line.split('/')
            english = line[1:]
            if 'surname' in english:
                continue
            pinyin_hanzi = line[0].split('[')
            hanzi = pinyin_hanzi[0]
            hanzi = hanzi.split(' ')
            traditional = hanzi[0]
            simplified = hanzi[1]
            pinyin = pinyin_hanzi[1]
            pinyin = pinyin.rstrip(' ]')
            attrib_list = []
            if key_is_trad_or_simp == 'trad':
                if traditional in dictionary:
                    attrib_list = dictionary[traditional]
                    for part in english:
                        attrib_list.append(part)
                    dictionary[traditional] = attrib_list
                    continue
                else:
                    attrib_list.append(simplified)
                    attrib_list.append(pinyin)
                    for part in english:
                        attrib_list.append(part)
                    dictionary[traditional] = attrib_list
            else:
                if simplified in dictionary:
                    attrib_list = dictionary[simplified]
                    for part in english:
                        attrib_list.append(part)
                    dictionary[simplified] = attrib_list
                    continue
                else:
                    attrib_list.append(traditional)
                    attrib_list.append(pinyin)
                    for part in english:
                        attrib_list.append(part)
                    dictionary[simplified] = attrib_list
        
        return dictionary
        

    def parse_dict(key_is_trad_or_simp):
        #make each line into a dictionary
        print("Parsing dictionary . . .")
        dictionary = parse_lines(lines, key_is_trad_or_simp)
        print("Done")

        return dictionary

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please type 'trad' or 'simp' as first argument depending on how you want the dictionary to be built.")
        exit()
    parsed_dict = parse_dict(sys.argv[1])
    print(parsed_dict)
