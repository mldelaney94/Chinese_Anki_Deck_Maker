""" This program makes a new dictionary with accent pinyin instead of numbered
pinyin.  It checks to see if each line has any of the 170 keys in REP, and
replaces them with the value if so. This, although unperformant, does not need
to be improved as it is only run once.

REP is deliberately structured with the
larger strings first as they would sometimes have overlap with the smaller
strings. For instance ei1 could be mistaken for i1."""

REP = {'iang4': 'iàng', 'iang3': 'iăng', 'iang2': 'iáng', 'iang1': 'iāng', 'iang5': 'iang',
       'iong4': 'iòng', 'iong3': 'iŏng', 'iong2': 'ióng', 'iong1': 'iōng', 'iong5': 'iong',
       'uang4': 'uàng', 'uang3': 'uăng', 'uang2': 'uáng', 'uang1': 'uāng', 'uang5': 'uang',
       'iao1': 'iāo', 'iao4': 'iào', 'iao3': 'iăo', 'iao2': 'iáo', 'iao5': 'iao',
       'eng4': 'èng', 'eng3': 'ĕng', 'eng2': 'éng', 'eng1': 'ēng', 'eng5': 'eng',
       'ang4': 'àng', 'ang3': 'ăng', 'ang2': 'áng', 'ang1': 'āng', 'ang5': 'ang',
       'ian4': 'iàn', 'ian3': 'iăn', 'ian2': 'ián', 'ian1': 'iān', 'ian5': 'ian',
       'ong4': 'òng', 'ong3': 'ŏng', 'ong2': 'óng', 'ong1': 'ōng', 'ong5': 'ong',
       'uan4': 'uàn', 'uan3': 'uăn', 'uan2': 'uán', 'uan1': 'uān', 'uan5': 'uan',
       'ing4': 'ìng', 'ing3': 'ĭng', 'ing2': 'íng', 'ing1': 'īng', 'ing5': 'ing',
       'uai1': 'uāi', 'uai4': 'uài', 'uai3': 'uăi', 'uai2': 'uái', 'uai5': 'uai',
       'ao1': 'āo', 'ao4': 'ào', 'ao3': 'ăo', 'ao2': 'áo', 'ao5': 'ao',
       'ai1': 'āi', 'ai4': 'ài', 'ai3': 'ăi', 'ai2': 'ái', 'ai5': 'ai',
       'au1': 'āu', 'au4': 'àu', 'au3': 'ău', 'au2': 'áu', 'au5': 'au',
       'ei1': 'ēi', 'ei2': 'éi', 'ei3': 'ĕi', 'ei4': 'èi', 'ei5': 'ei',
       'an4': 'àn', 'an3': 'ăn', 'an2': 'án', 'an1': 'ān', 'an5': 'an',
       'en4': 'èn', 'en3': 'ĕn', 'en2': 'én', 'en1': 'ēn', 'en5': 'en',
       'ie4': 'iè', 'ie3': 'iĕ', 'ie2': 'ié', 'ie1': 'iē', 'ie5': 'ie',
       'iu4': 'iù', 'iu3': 'iŭ', 'iu2': 'iú', 'iu1': 'iū', 'iu5': 'iu',
       'ia4': 'ià', 'ia3': 'iă', 'ia2': 'iá', 'ia1': 'iā', 'ia5': 'ia',
       'on4': 'òn', 'on3': 'ŏn', 'on2': 'ón', 'on1': 'ōn', 'on5': 'on',
       'ou4': 'òu', 'ou3': 'ŏu', 'ou2': 'óu', 'ou1': 'ōu', 'ou5': 'ou',
       'uo4': 'uò', 'uo3': 'uŏ', 'uo2': 'uó', 'uo1': 'uō', 'uo5': 'uo',
       'ua4': 'uà', 'ua3': 'uă', 'ua2': 'uá', 'ua1': 'uā', 'ua5': 'ua',
       'in4': 'ìn', 'in3': 'ĭn', 'in2': 'ín', 'in1': 'īn', 'in5': 'in',
       'ui4': 'uì', 'ui3': 'uĭ', 'ui2': 'uí', 'ui1': 'uī', 'ui5': 'ui',
       'er1': 'ēr', 'er2': 'ér', 'er3': 'ĕr', 'er4': 'èr', 'er5': 'er',
       'un4': 'ùn', 'un3': 'ŭn', 'un2': 'ún', 'un1': 'ūn', 'un5': 'un',
       'i4': 'ì', 'i3': 'ĭ', 'i2': 'í', 'i1': 'ī', 'i5': 'i',
       'a1': 'ā', 'a4': 'à', 'a3': 'ă', 'a2': 'á', 'a5': 'a',
       'e4': 'è', 'e3': 'ĕ', 'e2': 'é', 'e1': 'ē', 'e5': 'e',
       'o4': 'ò', 'o3': 'ŏ', 'o2': 'ó', 'o1': 'ō', 'o5': 'o',
       'u4': 'ù', 'u3': 'ŭ', 'u2': 'ú', 'u1': 'ū', 'u5': 'u',
       'u:4': 'ǜ', 'u:3': 'ǚ', 'u:2': 'ǘ', 'u:1': 'ǖ', 'u:5': 'ü',
       }
KEYS = REP.keys()

#define functions

def parse_lines(lines):
    """ Reconstruct the dictionary by search and replacing all pinyin """
    dictionary = []
    for line in lines:
        for key in KEYS:
            if key in line:
                line = line.replace(key, REP[key])
        dictionary.append(line)
    return dictionary

def parse_dict():
    """ Saves the dictionary created by parse_lines """
    print("Parsing dictionary . . .")
    dictionary = []
    with open('cedict_ts.u8', 'r') as f:
        dictionary = parse_lines(f)
    with open('test.txt', 'w+') as f:
        for line in dictionary:
            to_write = "".join(line)
            f.write(to_write)

if __name__ == "__main__":
    parse_dict()
    print('Done!')
