import csv

import glob
import pprint
import re
import os
from collections import Counter
import pandas as pd
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


# def aggregate_scores(first_row_score, candidates_scores):
#     # Нормализуем оценку первой строки
#     P = first_row_score / len(headers_found)
#
#     # Пройдемся по списку предполагаемых кандидатов и добавим оценку P, если индекс первой строки не указан
#     for candidate in candidates_scores:
#         if 0 not in candidate[0]:
#             candidate[0].insert(0, 0)
#             candidate[1] += P
#         else:
#             candidate[1] = P
#
#     # Добавим в список новый кандидат, если индекс первой строки не был учтен ранее
#     new_candidate = [[0], P]
#     if new_candidate not in candidates_scores:
#         candidates_scores.append(new_candidate)
#
#     # Отсортируем список кандидатов по убыванию оценок
#     candidates_scores.sort(key=lambda x: x[1], reverse=True)
#
#     # Выберем кандидата с максимальной оценкой
#     AGG = candidates_scores[0][0]
#
#     return AGG
def write_total_score(path,  result):

    if not os.path.exists(path):
        os.makedirs(path)
    with open(path, "a", encoding="utf-8") as file:
        file.write(result)
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
        return regular(text)
    else:
        for ent in doc.ents:
            return ent.type

        # Чтение проверочного CSV-файла
file = 'test.csv'
table = pd.DataFrame(pd.read_csv(file))
stanza.download("ru")
nlp = stanza.Pipeline(lang="ru", processors="tokenize,ner")
for filepath in glob.glob('SAUS/*.csv'):
    with open(os.path.join(os.getcwd(), filepath), 'r') as file:
        file_reader = csv.reader(file, skipinitialspace=True, delimiter=",")
        reader = list(file_reader)
        rows = 10
        max_len, i = -1000, 0
        while i < len(reader):
            if max_len < len(reader[i]):
                max_len = len(reader[i])
            i = i + 1
        columns = max_len
        test_ner_list = [[0 for x in range(columns)] for y in range(rows)]
        j, i = 0, 0
        for row in reader:
            for x in row:
                test_ner_list[j][i] = test_ner(x)
                i = i + 1
            i = 0
            j = j + 1
            if j == 10:
                break
        candidate_scores = []
        sample_size, threshold = 10, 0.6
        # Выполняем попарное сравнение определенных меток в ячейках столбца
        headers_found = set()
        for i in range(rows):
            row_scores = []
            row_match_scores = [test_ner_list[i][k] == test_ner_list[0][k] for k in range(columns)]
            row_score = sum(row_match_scores) / len(row_match_scores)
            row_scores.append(row_score)
            # Определяем оценку (ранг) для каждой предполагаемой строковой ячейки
            if row_scores:
                row_max = max(row_scores)
                if row_max >= threshold:
                    headers_found.add(i)
                    new_candidate = [[i], row_max]
                    if new_candidate not in candidate_scores:
                        candidate_scores.append(new_candidate)
        print('candidate_scores:', candidate_scores)
        R=0
        R_list = list()
        filename = os.path.basename(filepath)
        for i in table.index:
            if table['name'][i] == filename[:-4]:
                R+=1
                R_list.append(table['id'][i])
        print(R)
        # Сравнение результатов программы с проверочным файлом
        CH = len(headers_found.intersection(set(range(len(reader[0])))))
        H = len(headers_found)
        HUR = len(headers_found.union(R_list))
        # Оценка качества определения заголовков таблицы после проверки с проверочным файлом
        precision = CH / HUR
        recall = CH / R
        f1 = 0 if (precision + recall) == 0 else (2 * precision * recall) / (precision + recall)
        # Вывод результатов оценки качества определения заголовков
        print(f"Test file: {filename}")
        print(f"Header found: {headers_found}")
        print(f"CH = {CH}, H = {H}, R = {R}")
        print(f"HUR = {HUR}")
        print(f"Precision = {precision:.3f}")
        print(f"Recall = {recall:.3f}")
        print(f"F1 = {f1:.3f}")
        write_total_score('result.txt',filename[:-4]+f', {precision,recall,f1}\n')
        print("------------------------------------------------------------------------------------------------------------------------")
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
        print("Вероятность того, что первая строка заголовок равна", ((Coef)/2))
        # Объединение оценок
        P = Coef
        for i, candidate in enumerate(candidate_scores):
            if candidate[0] == [0]:
                candidate[1] += P
        # Определение лучшего заголовка
        best_candidate = max(candidate_scores, key=lambda x: x[1])
        best_header = reader[best_candidate[0][0]][0]
        best_score = best_candidate[1]
        normalized_score = best_score/(3)
        print('Best header:', best_header)
        print('Score:', round(normalized_score,2))