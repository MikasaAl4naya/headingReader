import csv
import datefinder
import glob
import re
import os
for filename in glob.glob('tables\*.csv'):
   with open(os.path.join(os.getcwd(), filename), 'r') as file:
        file_reader = csv.reader(file, delimiter=",")
        row1 = next(file_reader)
        w1,w2,w3=2,1,1
        IncorrectCounter,IncorCoef,VoidCoef,VoidCount,RepCoef = 0,0,0,0,0
        print(row1)
        print('В первой строке в файле', filename)
        for x in row1:
            if x == "":
                VoidCount = VoidCount + 1
        VoidCoef = VoidCount*0.05
        print("Пустых значений:",VoidCount)
        out = []
        RepCount= len(row1)-len(set(row1))
        RepCoef = RepCount*0.03
        print("Повторяющихся значений:",RepCount)
        for a in row1:
            if re.match('\d+', a) or re.match('/^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$/', a):
                IncorrectCounter=IncorrectCounter+1
        IncorCoef=IncorrectCounter*0.02
        Coef = VoidCoef+ IncorCoef +RepCoef
        print("Некорректных значений", IncorrectCounter)
        print("Вероятность того, что эта строка заголовок равна", 1 -Coef)
