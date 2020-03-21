""" This program makes a new dictionary with accent pinyin instead of numbered
pinyin. """

REP = {'iang4': 'iàng', 'iang3': 'iăng', 'iang2': 'iáng', 'iang1': 'iāng',
       'iong4': 'iòng', 'iong3': 'iŏng', 'iong2': 'ióng', 'iong1': 'iōng',
       'uang4': 'uàng', 'uang3': 'uăng', 'uang2': 'uáng', 'uang1': 'uāng',
       'iao1': 'iāo', 'iao4': 'iào', 'iao3': 'iăo', 'iao2':'iáo',
       'eng4': 'èng', 'eng3': 'ĕng', 'eng2': 'éng', 'eng1': 'ēng',
       'ang4': 'àng', 'ang3': 'ăng', 'ang2': 'áng', 'ang1': 'āng',
       'ian4': 'iàn', 'ian3': 'iăn', 'ian2': 'ián', 'ian1': 'iān',
       'ong4': 'òng', 'ong3': 'ŏng', 'ong2': 'óng', 'ong1': 'ōng',
       'uan4': 'uàn', 'uan3': 'uăn', 'uan2': 'uán', 'uan1': 'uān',
       'ing4': 'ìng', 'ing3': 'ĭng', 'ing2': 'íng', 'ing1': 'īng',
       'uai1': 'uāi', 'uai4': 'uài', 'uai3': 'uăi', 'uai2': 'uái',
       'ao1': 'āo', 'ao4': 'ào', 'ao3': 'ăo', 'ao2':'áo',
       'ai1': 'āi', 'ai4': 'ài', 'ai3': 'ăi', 'ai2':'ái',
       'au1': 'āu', 'au4': 'àu', 'au3': 'ău', 'au2':'áu',
       'ei1': 'ēi', 'ei2': 'éi', 'ei3': 'ĕi', 'ei4': 'èi',
       'an4': 'àn', 'an3': 'ăn', 'an2': 'án', 'an1': 'ān',
       'en4': 'èn', 'en3': 'ĕn', 'en2': 'én', 'en1': 'ēn',
       'ie4': 'iè', 'ie3': 'iĕ', 'ie2': 'ié', 'ie1': 'iē',
       'iu4': 'iù', 'iu3': 'iŭ', 'iu2': 'iú', 'iu1': 'iū',
       'ia4': 'ià', 'ia3': 'iă', 'ia2': 'iá', 'ia1': 'iā',
       'on4': 'òn', 'on3': 'ŏn', 'on2': 'ón', 'on1': 'ōn',
       'ou4': 'òu', 'ou3': 'ŏu', 'ou2': 'óu', 'ou1': 'ōu',
       'uo4': 'uò', 'uo3': 'uŏ', 'uo2': 'uó', 'uo1': 'uō',
       'ua4': 'uà', 'ua3': 'uă', 'ua2': 'uá', 'ua1': 'uā',
       'in4': 'ìn', 'in3': 'ĭn', 'in2': 'ín', 'in1': 'īn',
       'ui4': 'uì', 'ui3': 'uĭ', 'ui2': 'uí', 'ui1': 'uī',
       'er2': 'ér', 'er3': 'ĕr', 'er4': 'èr',
       'un4': 'ùn', 'un3': 'ŭn', 'un2': 'ún', 'un1': 'ūn',
       'i4': 'ì', 'i3': 'ĭ', 'i2': 'í', 'i1': 'ī',
       'a1': 'ā', 'a4': 'à', 'a3': 'ă', 'a2':'á',
       'e4': 'è', 'e3': 'ĕ', 'e2': 'é', 'e1': 'ē',
       'o4': 'ò', 'o3': 'ŏ', 'o2': 'ó', 'o1': 'ō',
       'u4': 'ù', 'u3': 'ŭ', 'u2': 'ú', 'u1': 'ū',
       'u:4': 'ǜ', 'u:3': 'ǚ', 'u:2': 'ǘ', 'u:1': 'ǖ',
       'iang5': 'iàng',
       'iong5': 'iòng',
       'uang5': 'uàng',
       'iao5': 'iao',
       'eng5': 'eng',
       'ang5': 'ang',
       'ian5': 'ian',
       'ong5': 'ong',
       'uan5': 'uan',
       'ing5': 'ing',
       'uai5': 'uai',
       'ao5': 'ao',
       'ai5': 'ai',
       'au5': 'au',
       'ei5': 'ei',
       'an5': 'an',
       'en5': 'en',
       'ie5': 'ie',
       'iu5': 'iu',
       'ia5': 'ia',
       'on5': 'on',
       'ou5': 'ou',
       'uo5': 'uo',
       'ua5': 'ua',
       'in5': 'in',
       'ui5': 'ui',
       'er5': 'er',
       'un5': 'un',
       'i5': 'i',
       'a5': 'a',
       'e5': 'e',
       'o5': 'o',
       'u5': 'u',
       'u:5': 'ü'
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
