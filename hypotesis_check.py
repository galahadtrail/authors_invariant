from main import authors_invariant
import scipy.stats as stats
import pandas as pd
import argparse
import sys
import warnings


def argument_parsing(arg):
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Program name', type=str)
    parser.add_argument('fileFirst', help='first Filename that we be used in calculating', type=str)
    parser.add_argument('fileSecond', help='second Filename that we be used in calculating', type=str)
    parser.add_argument('fileThird', help='second Filename that we be used in calculating', type=str)
    parser.add_argument('fileForth', help='second Filename that we be used in calculating', type=str)

    return parser.parse_intermixed_args(arg)


if __name__ == '__main__':
    alpha = 0.1
    args = argument_parsing(sys.argv)

    firstArr = authors_invariant(args.fileFirst)
    secondArr = authors_invariant(args.fileSecond)
    thirdArr = authors_invariant(args.fileThird)
    thirdForth = authors_invariant(args.fileForth)
    stat, p = stats.wilcoxon(firstArr + secondArr, thirdArr[:len(thirdArr)-5] + thirdForth[:len(thirdForth)-2])
    #print(stats.chisquare(thirdArr,secondArr))
    print(stat, p)

    stat, p = stats.shapiro(firstArr + secondArr)
    print(stat, p)
    print('Тест Шапиро - первая и вторая выборка:')
    if p < alpha:
        print('Отклонить гипотезу о нормальности')
        print()
    else:
        print('Принять гипотезу о нормальности')
        print()

    stat, p = stats.shapiro(thirdArr + thirdForth)
    print(stat, p)
    print('Тест Шапиро - третья и четвертая выборка:')
    if p < alpha:
        print('Отклонить гипотезу о нормальности')
        print()
    else:
        print('Принять гипотезу о нормальности')
        print()

    print("Анализ дисперсионного теста (ANOVA) на различия образцов")
    corr, p = stats.f_oneway(firstArr,secondArr,thirdArr,thirdForth)
    print(corr, p)
    if p < alpha:
        print("Отвергаем нулевую гипотезу, средние значения различны")
        print()
    else:
        print("Не получилось отвергнуть нулевую гипотезу, средние значения одинаковы")
        print()

    results = stats.kruskal(firstArr,secondArr,thirdArr,thirdForth)
    print("Kruskal-Wallis H тест на проверку равенства распределений:")
    print(results)
    if results.pvalue < alpha:
        print("Отвергаем нулевую гипотезу, средние значения не равны")
        print()
    else:
        print("Не получилось отвергнуть нулевую гипотезу, средние значения равны")
        print()

    results = stats.ttest_ind(firstArr + secondArr, thirdArr + thirdForth)
    print(results)
    print("Тест Стьюдента на проверку средних значений:")
    if results.pvalue < alpha:
        print("Отвергаем нулевую гипотезу, средние значения не равны")
        print()
    else:
        print("Не получилось отвергнуть нулевую гипотезу, средние значения равны")
        print()

    results = stats.mannwhitneyu(firstArr + secondArr, thirdArr + thirdForth)
    print(results)
    print("Тест Манна - Уитни на проверку равенства распределений:")
    if results.pvalue < alpha:
        print("Отвергаем нулевую гипотезу, распределения не равны")
        print()
    else:
        print("Не получилось отвергнуть нулевую гипотезу, распределения равны")
        print()

    stat, res = stats.kstest(firstArr + secondArr, thirdArr + thirdForth)
    print(stat,res)
    print("Критерий Колмогорова-Смирнова на проверку равенства распределений:")
    if res < alpha:
        print("Отвергаем нулевую гипотезу, распределения не равны")
        print()
    else:
        print("Не получилось отвергнуть нулевую гипотезу, распределения равны")
        print()

    stat, res = stats.ks_2samp(firstArr + secondArr, thirdArr + thirdForth)
    print(stat,res)
    print("Двухвыборочный критерий Колмогорова-Смирнова на проверку равенства распределений:")
    if res < alpha:
        print("Отвергаем нулевую гипотезу, распределения не равны")
        print()
    else:
        print("Не получилось отвергнуть нулевую гипотезу, распределения равны")
        print()
