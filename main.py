import csv
import datefinder
import glob
import os
import pandas as pd
for filename in glob.glob('tables\*.csv'):
   with open(os.path.join(os.getcwd(), filename), 'r') as file:
        file_reader = csv.reader(file, delimiter=",")
        row1 = next(file_reader)
        IncorrectCounter = 0
        Voidcount = 0
        print (row1)
        print('В первой строке в файле', filename)
        for x in row1:
            if x == "":
                Voidcount = Voidcount + 1
        print("Пустых значений:",Voidcount)

        out = []
        repCount= len(row1)-len(set(row1))
        print("Повторяющихся значений:",repCount)
        for a in row1:
            # a generator will be returned by the datefinder module. I'm typecasting it to a list. Please read the note of caution provided at the bottom.

            if list(datefinder.find_dates(a)):
                IncorrectCounter=+1
            if a.isnumeric():
                IncorrectCounter=+1
        print("Некорректных значений", IncorrectCounter)
