import csv
import datetime

with open("media.csv", encoding='utf-8') as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter=",")
    row1 = next(file_reader)
    dataCounter = 0
    z = True
    count = 0
    for x in row1:
        if x == "":
            count = count + 1
    if count != 0:
        z = False
        print("Есть пустые значения")
    else:
        print("Пустых значений нет")
    if z:
        if len(set(row1)) != len(row1):
            z = False
            print("Есть одинаковые значение")
        else:
            print("Все значение уникальны")

    if z:
        for a in row1:
            d = a
            if len(d.split('.')) == 3:
                if datetime.datetime.strptime(d, '%d.%m.%Y'):
                    dataCounter = +1
        if dataCounter != 0:
            z = False
            print("Есть некорректные значения")
