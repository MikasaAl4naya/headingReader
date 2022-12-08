import csv
import datefinder
import glob
import re
import os
from collections import Counter
import dateparser
def get_unique_cell(row1):
    count = 0
    row1 = [x.strip(' ') for x in row1]
    for x in Counter(row1).values():
        if x ==1:
            count+=1
    return count


def get_void_cell(row1):
    VoidCount = 0
    row1 = [x.strip(' ') for x in row1]
    for x in row1:
        if x == "":
            VoidCount = VoidCount + 1
    return VoidCount


def get_incorrect_cell(row1):
    IncorrectCounter = 0
    row1 = [x.strip(' ') for x in row1]
    datax = ''
    for x in row1:
            datax =dateparser.parse(x)
            if datax is not None:
                IncorrectCounter+=1
            elif re.match(r"([-+]?(?:\d+(?:.\d)?|.\d+)(?:[eE][-+]?\d+)?)", x):
                IncorrectCounter += 1
    return IncorrectCounter


for filename in glob.glob('tables\*.csv'):
    with open(os.path.join(os.getcwd(), filename), 'r') as file:
        file_reader = csv.reader(file, delimiter=",")
        row1 = next(file_reader)
        w1, w2, w3 = 2, 1, 1
        IncorCoef, VoidCoef, RepCoef = 0, 0, 0
        print(row1)
        print('В первой строке в файле', filename)
        print("Всего количества яйчеек:", len(row1))
        print('Уникальных значений', get_unique_cell(row1))
        print("Пустых значений:",get_void_cell(row1))
        print("Некорректных значений", get_incorrect_cell(row1))
        RepCoef = get_unique_cell(row1)/len(row1) *w1
        VoidCoef = get_void_cell(row1) / len(row1) * w2
        IncorCoef=get_incorrect_cell(row1)/len(row1)*w3
        Coef = RepCoef -(IncorCoef + VoidCoef)
        if Coef<0:
            Coef=0


        print("Вероятность того, что эта строка заголовок равна", Coef)

