from typing import List, Any
import re
import statistics
import argparse
import sys


def argument_parsing(arg):
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Program name', type=str)
    parser.add_argument('file', help='Filename that we be used in calculating', type=str)

    return parser.parse_intermixed_args(arg)


def authors_invariant(filename):
    text = ""
    try:
        if '.' not in filename:
            raise TypeError('Not a file name!')
    except TypeError:
        print('Not a file name, terminating..')
        return []

    filename_dup = filename.split(".")

    if filename_dup[1] != 'txt':
        print('Please, enter .txt file and nothing else!')
        return 1

    try:
        with open(filename, encoding="windows-1251") as file:
            text = file.read()
    except:
        print("Can not read this file or it's code not in windows-1251!\nPlease, use the following requirements.")
        return 2

    list_of_pieces = []

    duty_symbols = ['в', 'на','с','за','к','по','из','у','от','для',
                    'во','без','до','о','через','со','при','про','об','ко','над', 'из-за', 'из-под','под','и',
                    'что','но','а','да','хотя','когда','чтобы','если','тоже','или','то есть','зато','будто','не',
                    'как','же','даже','бы','ли','только','вот','то','ни','лишь','ведь','вон','нибудь','уже','либо']

    text = re.split('[^а-яё-]+', text, flags=re.IGNORECASE)
    text = [elem.lower() for elem in text if elem != '-']

    step = 0
    step_t = 0.05 * len(text)
    count_t = 0
    temp_list = []

    for word in text:

        if step != 0 and step < step_t:
            step += 1
            continue

        count_t += 1
        temp_list.append(word)
        if count_t == 16000:
            count_t = 0
            step = 1
            list_of_pieces.append(temp_list)
            temp_list = []

    list_of_invariants = []

    for piece in list_of_pieces:
        list_size = len(piece)
        duty_words_amount = 0
        for word in piece:
            if word in duty_symbols:
                duty_words_amount += 1
        list_of_invariants.append((duty_words_amount/list_size)*100)

    print(list_of_invariants)
    return list_of_invariants


def writing_values():
    with open('result.txt', 'w+', encoding='windows-1251') as file:
        file.write("For this book " + args.file + " authors invariant is ")
        values = authors_invariant(args.file)
        file.write(str(statistics.mean(values)))
        file.write('\n')
        file.write('And those values we got:')
        file.write('\n')
        for value in values:
            file.write(str(value))
            file.write('\n')


if __name__ == '__main__':
    args = argument_parsing(sys.argv)
    writing_values()
