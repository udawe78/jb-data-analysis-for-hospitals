import pandas as pd
from os import listdir
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker


# calculate the share of the patients in the particular hospital
# suffers from certain issues
def what_share(dataset, terms: tuple) -> float:
    hospital, diagnos = terms
    filt = (dataset['hospital'] == hospital) & (dataset['diagnosis'] == diagnos)
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
difference = age_by_hosp.loc['general'] - age_by_hosp.loc['sports']
answers.append(difference['age'])

# 5th QUESTION
# What is the biggest number of t in the blood_test column among all the hospitals?
# How many blood tests were taken?
filter_blood_test = (df['blood_test'] == 't')
btest_by_hosp = df[filter_blood_test].groupby('hospital').aggregate({'blood_test': 'count'})
answers.append(f"{btest_by_hosp['blood_test'].idxmax()}, {btest_by_hosp['blood_test'].max()} blood test")

# all answers of the stage 4
for number, answer in zip(numbers, answers):
    print(f'The answer to the {number} question is {answer}')

# below are the answers to stage 5 questions
answers_2 = list()

# first plot is histogram
fig1, ax1 = plt.subplots()
bins = (0, 15, 35, 55, 70, 80, 100)
ax1.hist(df['age'], bins=bins)
answers_2.append('15-35')

# second plot is pie chart
fig2, ax2 = plt.subplots()
diagnosis = df['diagnosis'].value_counts().index
ax2.pie(df['diagnosis'].value_counts(), labels=diagnosis)
answers_2.append(diagnosis[0])

# third plot is violin-type
fig3, ax3 = plt.subplots()
hospitals = df['hospital'].unique()
samples = [df[df['hospital'] == hospital].height for hospital in hospitals]
ax3.violinplot(samples)
# Optional line
ax3.xaxis.set_major_locator(mticker.FixedLocator([1, 2, 3]))
ax3.set_xticklabels(hospitals)
answers_2.append('It`s because...')

plt.show()

# all answers of the stage 5
for number, answer in zip(numbers[:3], answers_2):
    print(f'The answer to the {number} question: {answer}')