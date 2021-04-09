import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd
from numpy.random import randint
import re

langs = {
    'латински'   : 'latin',
    'английски'  : 'english',
    'гръцки'     : 'greek',
    'френски'    : 'french',
    'италиански' : 'italian',
    'турски'     : 'turkish',
    'немски'     : 'german',
    'испански'   : 'spanish',
    'румънски'   : 'romanian',
    'арабски'    : 'arabic',
    'руски'      : 'russian',
    'японски'    : 'japanese',
    'незнаен'    : 'unknown'
}


fields = {
    'химия' : 'chemistry',
    'медицина' : 'medicine',
    'разговорен речник' : 'slang',
    'граматика' : 'grammarcy',
    'книжовен речник' : 'official language',
    'геометрия' : 'geometry',
    'философия' : 'philosophy',
    'митология' : 'mithology',
    'история' : 'history',
    'търговия' : 'commerce',
    'църковна' : 'church',
    'зоология' : 'zoology',
    'спорт' : 'sport',
    'печатарство' : 'print',
    'технологий' : 'technology',
    'архаизми' : 'archieve',
    'право' : 'law',
    'ботаника' : 'botanics',
    'неидентифицирана' : 'unknown'
}

rootdir = 'matches/'
dirs = []
rates_df = pd.DataFrame(columns=['field', 'unique', 'non_unique'])
langs_df = pd.DataFrame(columns=['field', 'lang', 'count'])
range_df = pd.DataFrame(columns=['field', 'range', 'count'])

def load_file_names(dir):
    folder_names= os.listdir (dir) # get all files' and folders' names in the current directory
    for folder_name in folder_names:  # loop through all the files and folders
        for file_name in os.listdir (dir + '/' + folder_name):
            if folder_name in file_name:
                dirs.append(dir + folder_name + '/' + file_name);
    dirs.sort()

def parse_files_to_df():
    r_count = 0
    l_count = 0
    f_count = 0
    for index, file in enumerate(dirs):
        field_dir = re.search('/(.*)/', file).group(1)
        cur_sec = ''
        with open(file, encoding="utf8") as f:
            current_file = f.read().strip()+'\n'
            prevnl = -1
            while True:
                nextnl = str(current_file).find('\n', prevnl + 1)
                if nextnl < 0: break
                line = str(current_file)[prevnl + 1:nextnl]

                if '#unique foreign words rate-' in line \
                        and 'not' not in line:
                    unique_rate = float(line[line.rfind('-'):].replace(';', ''))


                if '#not unique foreign words rate-' in line:
                    rate = float(line[line.rfind('-'):].replace(';', ''))
                    rates_df.loc[r_count] = [field_dir, abs(unique_rate), abs(rate)]

                    r_count = r_count + 1

                if '#Произход:' in line or '#Област:' in line:
                    cur_sec = line.replace("#", '').replace(':', '')

                if '#' not in line:
                    delimiter = line.rfind('-')
                    if cur_sec == 'Произход':
                        langs_df.loc[l_count] = [field_dir, langs[line[:delimiter]], abs(int(line[delimiter:]))]
                        l_count = l_count + 1
                    if cur_sec == 'Област':
                        range_df.loc[f_count] = [field_dir, fields[line[:delimiter]], abs(int(line[delimiter:]))]
                        f_count = f_count + 1

                prevnl = nextnl

def visualization():
    sns.set()
    rates_df.set_index('field').T.plot(kind='bar', stacked=True)
    plt.show()

    sns.catplot(x="lang", y="count", hue = 'field',
                kind="bar", data=langs_df);
    plt.show()

    sns.catplot(x="range", y="count", hue = 'field',
                kind="bar", data=langs_df);
    plt.show()

def main():
    # rates_df = pd.DataFrame(columns=['field', 'unique', 'non_unique'])
    # for i in range(5):
    #     df.loc[i] = ['name' + str(i)] + list(randint(10, size=2))
    load_file_names(rootdir)
    parse_files_to_df()
    # print(langs_df)
    visualization()
    # print(rates_df)
    # print(langs_df)
    # print(range_df)

main()