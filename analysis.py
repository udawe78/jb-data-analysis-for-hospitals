import pandas as pd
from os import listdir


def what_share(dataset, hospital, diagnosis):
    filter_hospital = (dataset['hospital'] == hospital)
    filter_diagnosis = (dataset['diagnosis'] == diagnosis)
    share = dataset[filter_hospital & filter_diagnosis].shape[0] / dataset[filter_hospital].shape[0]
    return share


# 1 set option
pd.set_option('display.max_columns', 9)

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

# Below are the answers to 5 questions
# list of the answers
num_answer = ('1st', '2nd', '3rd', '4th', '5th')
answers = list()

# 1st question: which hospital has the highest number of patients?
answers.append(df['hospital'].value_counts().idxmax())

# 2nd and 3rd questions: what share of the patients in the general/sports hospital
#                        suffers from stomach/dislocation-related issues?
#                        Round the result to the third decimal place
conditions = (('general', 'stomach'), ('sports', 'dislocation'))
for item in conditions:
    answers.append(round(what_share(df, item[0], item[1]), 3))

# 4th question: hat is the difference in the median ages of the patients
#               in the general and sports hospitals?
temp_df = df.groupby('hospital').aggregate({'age': 'median'})
answers.append(temp_df.loc['general', 'age'] - temp_df.loc['sports', 'age'])

# 5th question: In which hospital the blood test was taken
#               the most often (there is the biggest number of t
#               in the blood_test column among all the hospitals)?
#               How many blood tests were taken?
filter_blood_test = (df['blood_test'] == 't')
temp_df = df[filter_blood_test].groupby('hospital').aggregate({'blood_test': 'count'})
answers.append(f"{temp_df['blood_test'].idxmax()}, {temp_df['blood_test'].max()} blood test")

# printing answers
for k, item in zip(num_answer, answers):
    print(f'The answer to the {k} question is {item}')
