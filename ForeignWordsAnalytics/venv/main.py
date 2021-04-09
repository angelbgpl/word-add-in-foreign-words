import check_text_foreign_words as check
import os
import sys

def process_text_dict(text):
    words_res = check.get_words_from_dict(text)
    return words_res

def main():
    # print(1)
    res = process_text_dict(sys.argv[1])
    text = [ord(c) for c in res]
    print(text)
    # print(sys.argv[1])
    # print(2)
    # process_text_dict(sys.argv[1])

main()
