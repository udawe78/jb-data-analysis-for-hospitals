import pandas as pd
from os import listdir


# calculate the share of the patients in the particular hospital
# suffers from certain issues
def what_share(dataset, terms: tuple) -> float:
    hospital, diagnosis = terms
    filt = (dataset['hospital'] == hospital) & (dataset['diagnosis'] == diagnosis)
    share = dataset[filt].shape[0] / dataset.shape[0]
    return share


# Below are the answers to 9 tasks

# 1. Set option
pd.set_option('display.max_columns', 9)

# 2. Read CSV files with datasets from the specified folder
path = 'test/'
files = [path + file for file in listdir(path)]
tables = [pd.read_csv(file) for file in files]

# 3. Change the column names. All column names in the sports and prenatal tables
# must match the column names in the general table
for table in tables[1:]:
    table.columns = tables[0].columns

# 4. Merge the data frames into one
df = pd.concat(tables, ignore_index=True)
print(type(df))
# 5. Delete the Unnamed: 0 column
df.drop(columns=df.columns[0], inplace=True)

# 6. Delete all the empty rows
df.dropna(axis=0, thresh=1, inplace=True)

# 7. Correct all the gender column values to f and m respectively
df.replace({'gender': {'female': 'f', 'woman': 'f', 'male': 'm', 'man': 'm'}}, inplace=True)

# 8. Replace the NaN values in the gender column of the prenatal hospital with f
filter_prenatal = df['hospital'] == 'prenatal'
df.loc[filter_prenatal, 'gender'] = df.loc[filter_prenatal, 'gender'].fillna('f')

# 9. Replace the NaN values in the bmi, diagnosis, blood_test, ecg,
# ultrasound, mri, xray, children, months columns with zeros
cols = ['bmi', 'diagnosis', 'blood_test',
        'ecg', 'ultrasound', 'mri',
        'xray', 'children', 'months']
magic_number = 0
df[cols] = df[cols].fillna(magic_number)

# Below are the answers to 5 QUESTIONS

numbers = ('1st', '2nd', '3rd', '4th', '5th')
answers = list()

# 1st QUESTION
# Which hospital has the highest number of patients?
answers.append(df['hospital'].value_counts().idxmax())

# 2nd and 3rd QUESTIONS
# What share of the patients in the general/sports hospital
# suffers from stomach/dislocation-related issues?
# Round the result to the third decimal place
conditions = (('general', 'stomach'), ('sports', 'dislocation'))
for condition in conditions:
    answers.append(round(what_share(df, condition), 3))

# 4th QUESTION
# What is the difference in the median ages of the patients
# in the general and sports hospitals?
age_by_hosp = df.groupby('hospital').aggregate({'age': 'median'})
answers.append(age_by_hosp.loc['general', 'age'] - age_by_hosp.loc['sports', 'age'])

# 5th QUESTION
# What is the biggest number of t in the blood_test column among all the hospitals?
# How many blood tests were taken?
filter_blood_test = (df['blood_test'] == 't')
btest_by_hosp = df[filter_blood_test].groupby('hospital').aggregate({'blood_test': 'count'})
answers.append(f"{btest_by_hosp['blood_test'].idxmax()}, {btest_by_hosp['blood_test'].max()} blood test")

# all 5 answers
for number, answer in zip(numbers, answers):
    print(f'The answer to the {number} question is {answer}')
