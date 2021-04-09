from nltk.tokenize import TweetTokenizer
from PyBulStem.bulstem import stem, MIN_WORD_LEN
import os
import collections



translates = dict()
finalDictionary = ""
tknzr = TweetTokenizer()


def fastCheck(sList, is_unique = True):
  foreignList = []
  dictionary = ""
  f1 = open("ForeignWordsAnalytics/venv/dictionaries/formatted/fastCheckWordsFinal.txt")
  text = f1.read()
  f1.close()

  for row in text.split(";"):
    for col in row.split("-"):
      # if "#" in col:
         foreignList.append(col)

#   print(foreignList)

  for i in range(0, len(foreignList) - 1, 2):
    translates[foreignList[i]] = foreignList[i+1]

#   print(translates)

  for s in sList:
    # print(s)
    for item in translates.keys():
      if stem(s.strip()) == stem(item.strip()) and \
              ((((item.strip() + "-" + translates[item].strip()) not in dictionary) and \
                      is_unique) or not is_unique):
        dictionary = dictionary + item.strip() + "-" + translates[item].strip() + "&"
    
    last_char_index = dictionary.rfind("&")
    new_dictionary = dictionary[:last_char_index] + "," + dictionary[last_char_index+1:]
  # print(dictionary)
  return new_dictionary

# def process(name, text):
#     sList = []
#     list = tknzr.tokenize(text)
#     for word in list:
#         sList.append(word)

#     finalDictionary = fastCheck(sList, False)

#     foreignRate = len(finalDictionary.splitlines())/len(sList)

#     finalDictionary = fastCheck(sList, True)

#     foreignRateUnique = len(finalDictionary.splitlines())/len(sList)

#     filename = name.replace('dataset', 'matches') + '_matches.txt'
#     # print(filename[:filename.rfind('/'):])
#     if not os.path.exists(filename[:filename.rfind('/'):]):
#         os.makedirs(filename[:filename.rfind('/')])
#     with open(filename, 'w+') as f:
#         f.write(finalDictionary)

#     metrics = '#unique foreign words rate-' + str("{:.4f}".format(foreignRateUnique)) + ';' \
#         + '\n#not unique foreign words rate-' + str("{:.4f}".format(foreignRate)) + ';\n'

#     metrics = metrics + group_by_lang_field(finalDictionary)
#     filename = name.replace('dataset', 'matches') + '_metrics.txt'
#     print(filename[:filename.rfind('/'):])
#     if not os.path.exists(filename[:filename.rfind('/'):]):
#         os.makedirs(filename[:filename.rfind('/')])
#     with open(filename, 'w+') as f:
#         f.write(metrics)
#     return metrics

# def group_by_lang_field(finalDictionary):
#     prevnl = -1
#     metrics_lang = '#Произход:\n'
#     metrics_field = '#Област:\n'
#     while True:
#         nextnl = finalDictionary.find('\n', prevnl + 1)
#         if nextnl < 0: break
#         line =  finalDictionary[prevnl + 1:nextnl]
#         line_lang = line[line.rfind('#Произход'):line.rfind('#Област')]
#         line_field = line[line.rfind('#Област'):line.rfind('#')]

#         if line_lang not in metrics_lang:
#             metrics_lang = metrics_lang + line_lang + '-' + str(finalDictionary.count(line_lang)) + ';\n'

#         if line_field not in metrics_field:
#             metrics_field = metrics_field + line_field + '-' + str(finalDictionary.count(line_field)) + ';\n'
#         prevnl = nextnl

#     return metrics_lang + metrics_field

def get_words_from_dict(text):
    sList = []
    list = tknzr.tokenize(text)
    for word in list:
        sList.append(word)

    finalDictionary = fastCheck(sList, True)
    return finalDictionary
