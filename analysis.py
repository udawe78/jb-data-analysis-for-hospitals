import pandas as pd
from os import listdir

pd.set_option('display.max_columns', 8)

# Read CSV files with datasets from the specified folder
path = 'test/'
files = [path + file for file in listdir(path)]
data = [pd.read_csv(file) for file in files]

# Change the column names. All column names in the sports and prenatal tables
# must match the column names in the general table
for item in data[1:]:
    item.columns = data[0].columns

# Merge the data frames into one
df = pd.concat(data, ignore_index=True)

# Delete the Unnamed: 0 column
df.drop(columns=df.columns[0], inplace=True)

# Print random 20 rows of the resulting data frame.
# For the reproducible output - 'random_state=30'
print(df.sample(n=20, random_state=30))
