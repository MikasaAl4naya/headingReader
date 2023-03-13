import csv

import glob
import pprint
import re
import os
from collections import Counter

import dateparser
import stanza as stanza


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
    for x in row1:
            datax =dateparser.parse(x)
            if datax is not None:
                IncorrectCounter+=1
            elif re.match(r"([-+]?(?:\d+(?:.\d)?|.\d+)(?:[eE][-+]?\d+)?)", x):
                IncorrectCounter += 1
    return IncorrectCounter


def regular(row):
    if re.search(r"^-[1-9]\d*$", row):
        return ('NEGATIVE_INTEGER')
    if re.search(r"^((\+7|7|8)+([0-9]){10})$", row):
        return ('NUMBER OF PHONE')
    if re.search(r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d", row):
        return ('DATE')
    if re.search(
            r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",
            row):
        return ('IP_ADDRESS_V6')
        # If positive integer
    if re.search(r"^[1-9]\d*$", row):
        return ('POSITIVE_INTEGER')
    if re.search(r"^[0-9]{4}-[0-9]{3}[0-9xX]$", row):
        return ('ISSN')
    if re.search(r"^(?:ISBN(?:: ?| ))?((?:97[89])?\d{9}[\dx])+$", row):
        return ('ISBN')
    if re.search(
            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9]["
            r"0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", row):
        return ('IP_ADDRESS_V4')
    if re.search(r"^([0-9]{4}\s{1}[0-9]{4}\s{1}[0-9]{4}\s{1}[0-9]{4})$", row):
        return ('BANK_CARD')
    if re.search(r"#[0-9A-Fa-f]{6}", row):
        return ('COLOR')
    if re.search(r"^(-?\d+(\.\d+)?),\s*(-?\d+(\.\d+)?)$", row):
        return ('COORDINATES')
    if re.search(
            r"^((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}["
            r"-\.\s]??\d{4}))$", row):
        return ('PHONE')
    if re.search(r"([+-]?\d+(\.\d+)*)\s?°([CcFf])", row):
        return ('TEMPERATURE')
    if re.search(r"^(0x)?[a-fA-F0-9]+$", row):
        return ('HEXADECIMAL')

    return ('None')
def test_ner(text):
    doc = nlp(text)
    if len(doc.ents) == 0:
        return (regular(text))
    else:
        for ent in doc.ents:
            return(ent.type)

stanza.download("ru")
nlp = stanza.Pipeline(lang="ru", processors="tokenize,ner")
for filename in glob.glob('tables\ipv4.csv'):
    print(str(filename))
    with open(os.path.join(os.getcwd(), filename), 'r') as file:
        file_reader = csv.reader(file, skipinitialspace=True, delimiter=",")
        reader= list(file_reader)
        rows = 10
        max,i=-1000,0
        while i<len(reader):
            if max<len(reader[i]):
                max= len(reader[i])
            i=i+1
        columns = max
        print(rows,columns)
        test_ner_list = [[0 for x in range(columns)] for y in range(rows)]
        j,i = 0,0
        for row in reader:
            for x in row:
                test_ner_list[j][i] = test_ner(x)
                i = i + 1
            i = 0
            j= j+1
            if j ==10:
                break
        pprint.pprint(test_ner_list)
        j, i,count_true,count, min, j_head = 0, 0, 0, 0, 1000, 0
        while j< rows + 1:
            while i<columns:
                if test_ner_list[j][i] == test_ner_list[j+1][i]:
                    count_true=count_true+1
                i = i + 1
            print("Совпадают " +str (count_true)+ ' из '+ str(columns))
            if min >= count_true:
                count = 0
                min = count_true
                j_head=j
            else:
                count= count +1
                if count == 4:
                    print(str(reader[j_head]) + "- заголовок")
                    break
            count_true=0
            i=0
            j=j+1
            if j== 10:
                break
        # print("------------------------------------------------------------------------------------------------------------------------")
        w1, w2, w3 = 2, 1, 1
        IncorCoef, VoidCoef, RepCoef = 0, 0, 0
        row1=reader[0]
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
        print("Вероятность того, что эта строка заголовок равна", ((Coef)/2))



