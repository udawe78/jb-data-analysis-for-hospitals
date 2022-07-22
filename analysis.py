import pandas as pd
from os import listdir

pd.set_option('display.max_columns', 8)

path = 'test/'
files = [path + file for file in listdir(path)]

data = [pd.read_csv(file) for file in files]

for item in data:
    print(item.head(20))
