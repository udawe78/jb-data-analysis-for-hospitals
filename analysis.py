import pandas as pd
from os import listdir

pd.set_option('display.max_columns', 9)  # 1.

# 2. Read CSV files with datasets from the specified folder
path = 'test/'
files = [path + file for file in listdir(path)]
data = [pd.read_csv(file) for file in files]

# 3. Change the column names. All column names in the sports and prenatal tables
# must match the column names in the general table
for item in data[1:]:
    item.columns = data[0].columns

# 4. Merge the data frames into one
df = pd.concat(data, ignore_index=True)

# 5. Delete the Unnamed: 0 column
df.drop(columns=df.columns[0], inplace=True)

# 6. Delete all the empty rows
df.dropna(axis=0, thresh=1, inplace=True)

# 7. Correct all the gender column values to f and m respectively
df.replace({'gender': {'female': 'f', 'woman': 'f', 'male': 'm', 'man': 'm'}}, inplace=True)

# 8. Replace the NaN values in the gender column of the prenatal hospital with f
df.loc[df['hospital'] == 'prenatal', 'gender'] = df.loc[df['hospital'] == 'prenatal', 'gender'].fillna('f')

# 9. Replace the NaN values in the bmi, diagnosis, blood_test, ecg,
# ultrasound, mri, xray, children, months columns with zeros
cols = ['bmi', 'diagnosis', 'blood_test',
        'ecg', 'ultrasound', 'mri',
        'xray', 'children', 'months']
magic_number = 0
df[cols] = df[cols].fillna(magic_number)

# 10. Print shape of the resulting data frame
print(f'Data shape: {df.shape}')

# 11. Print random 20 rows of the resulting data frame
# for the reproducible output - 'random_state=30'
print(df.sample(n=20, random_state=30))
