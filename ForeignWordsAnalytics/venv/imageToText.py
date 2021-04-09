from PIL import Image
import pytesseract
import codecs
import os, os.path
import re

langs = {
    'лат.' : 'латински',
    'англ.': 'английски',
    'гр.'  : 'гръцки',
    'фр.'  : 'френски',
    'ит.'  : 'италиански',
    'тур.' : 'турски',
    'нем.' : 'немски',
    'исп.' : 'испански',
    'рум.' : 'румънски',
    'ар.'  : 'арабски',
    'рус.' : 'руски',
    'яп.'  : 'японски'
}


fields = {
    'хим.' : 'химия',
    'мед.': 'медицина',
    'разг.': 'разговорен речник',
    'грам.': 'граматика',
    'книж.': 'книжовен речник',
    'геом.': 'геометрия',
    'фил.': 'философия',
    'мит.': 'митология',
    'ист.': 'история',
    'търг.': 'търговия',
    'църк.': 'църковна',
    'зоол.': 'зоология',
    'сп.': 'спорт',
    'печ.': 'печатарство',
    'техн.': 'технологий',
    'остар.': 'архаизми',
    'юр.': 'право',
    'бот.': 'ботаника'
}

def prepare_item(line):
    key_list = list(langs.keys())
    lang_origin = ''
    field_origin = ''

    for lang in key_list:
        # TO CHECK NOT VERY SMART IF YOU HAVE TWO LANGUAGES AS ORIGIN
        # TO CHECK NOT VERY SMART IF YOU HAVE TWO LANGUAGES AS ORIGIN
        # TO CHECK NOT VERY SMART IF YOU HAVE TWO LANGUAGES AS ORIGIN
        if lang in line:
            lang_origin = langs[lang]
            break

    key_list = list(fields.keys())
    for field in key_list:
        #TO CHECK NOT VERY SMART IF YOU HAVE TWO LANGUAGES AS ORIGIN
        #TO CHECK NOT VERY SMART IF YOU HAVE TWO LANGUAGES AS ORIGIN
        #TO CHECK NOT VERY SMART IF YOU HAVE TWO LANGUAGES AS ORIGIN
        if field in line:
           field_origin = fields[field]
           break

    if lang_origin == '':
       lang_origin = 'незнаен'

    if field_origin == '':
       field_origin = 'неидентифицирана'

    return '.#Произход:' + lang_origin + '#Област:' + field_origin + '#'

def extract_data_from_image():
    # simple version for working with CWD
    DIR = 'D:/PythonProjects/venv/images/cut'
    num_of_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    for i in range(num_of_files):

        text = pytesseract.image_to_string(image = r'images/cut/' + str(i+1) + '.jpg', lang='bul')
        splitted = text.splitlines()

        word = ''
        words = []

        previous = next_ = None
        l = len(splitted)
        for index, obj in enumerate(splitted):
            if splitted[index].endswith('-'):
                word = word + splitted[index][ : -1]
            else:
                word = word + splitted[index]
                if index > 0:
                    previous = splitted[index - 1]
                if splitted[index] == '' and previous.endswith('.'):
                   words.append(word)
                   word = ''

        words = ["-".join(line.split(" ", 1)) for line in words]
        # print(*words, sep = '\n')
        with open('dictionaries/' + str(i+1) + '.txt', 'w') as f:
            for item in words:
                k = item.rfind(".")
                item = item.replace(';', ',')

                lang_field = prepare_item(item)

                start = item.find('(')
                end = item.find(')')
                if start != -1 and end != -1:
                    item = item[:start] + item[end + 2:]

                f.write("%s\n" % (item[:k] + lang_field + ";"))

def build_dictionary():
    directory = 'D:/PythonProjects/venv/dictionaries/formatted'

    with open(directory + '/fastCheckWordsFinal.txt', 'w') as outfile:
        # outfile.write('#dictionary\n')
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                    with open(directory + '/' + filename) as infile:
                            outfile.write(infile.read())
            else:
                continue

# def main():
    # extract_data_from_image()
    # build_dictionary()
    # print(prepare_item('хит-(англ. БИ „успех“) нов. Най-хубавото, найлюбимо и търсено модно произведение, изделие и под., сензация, връх;'))
# main()