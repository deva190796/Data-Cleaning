import numpy as np
import pandas as pd
path = r"C:\Users\Lenovo\Desktop\DataCleaning\ptwo.csv"
data = pd.read_csv(path)
print(data.info())
data['StudentID'] = data['StudentID'].astype('category')
print(data.info())
data['StudentID'] = data['StudentID'].str.strip()
data['digit'] = data['StudentID'].str.extract('(\\d+)')
print(data['digit'])
data['digit'] = data['digit'].apply(lambda x: x.zfill(4))
print(data['digit'])
data['StudID'] = "S" + data['digit']
print(data['StudID'])
data = data.drop_duplicates(subset = 'StudID',keep = 'first')
print(data['StudID'])

data['StudentID'] = data[['StudID']].rename(columns = {'StudID':"StudentID"})

data['Name'] = data['Name'].astype('category')
data['Name'] = data['Name'].str.strip()
data['Name'] = data['Name'].str.title()
data = data.drop_duplicates(subset = 'Name', keep = 'first')
print(data['Name'])

data['Age'] = data['Age'].astype(int)
data['Age'] = pd.to_numeric(data['Age'],errors = 'coerce')
data.loc[(data['Age'] < 0) | data['Age'] > 100, 'Age'] = np.nan
data['Age'] = data['Age'].fillna(data['Age'].median())
data['Age'] = data['Age'].clip(lower = 15, upper = 25)
data['Age'] = data['Age'].astype(int)

print(data['Age'])

data['Math'] = pd.to_numeric(data['Math'], errors = 'coerce')
data.loc[(data['Math'] < 0) | (data['Math'] > 100), 'Math'] = np.nan
data['Math'] = data['Math'].fillna(data['Math'].median())
data['Math'] = data['Math'].round(1)
data['Math'] = data['Math'].astype(int)
print(data['Math'])

data['Science'] = pd.to_numeric(data['Science'], errors = 'coerce')
data.loc[(data['Science'] < 0) | (data['Science'] > 100), 'Science'] = np.nan
data['Science'] = data['Science'].fillna(data['Science'].median())
data['Science'] = data['Science'].round(1)
data['Science'] = data['Science'].astype(int)
print(data['Science'])

data['English'] = pd.to_numeric(data['English'], errors = 'coerce')#make each column numeric and if any is not numeric then it make as null
data.loc[(data['English'] < 0) | (data['English'] > 100), 'English'] = np.nan
data['English'] = data['English'].fillna(data['English'].median())
data['English'] = data['English'].astype(int)
print(data['English'])

data['Total'] = pd.to_numeric(data['Total'], errors = 'coerce')
data.loc[(data['Total'] < 0 ) | (data['Total'] > 300), 'Total'] = np.nan
data['Total'] = data['Total'].fillna(data['Total'].median())
data['Total'] = data['Total'].round(1)
data['Total'] = data['Total'].astype(int)
print(data['Total'])

data['Percentage'] = pd.to_numeric(data['Percentage'], errors = 'coerce')
data.loc[(data['Percentage'] < 0 ) | (data['Percentage'] > 300), 'Percentage'] = np.nan
data['Percentage'] = data['Percentage'].fillna(data['Percentage'].median())
data['Percentage'] = data['Percentage'].round(1)
data['Percentage'] = data['Percentage'].astype(int)
print(data['Percentage'])

data['Grade'] = data['Grade'].astype('category')
data['Grade'] = data['Grade'].str.strip()
data['Grade'] = data['Grade'].str.lower()

mapping = {'a+':"A+", 'a':"A", "a-" : "A", "b" : "B", "c" : "C", "pass" : "PASS", "fail" : "FAIL", "f" : "FAIL", "excellent" : "A+", "distinction" : "A+" }
data['Grade'] = data['Grade'].replace(mapping)
data['Grade'] = data['Grade'].where(data['Grade'].isin(["A+","A","B","C","PASS","FAIL"]))

print(data['Grade'])

data['EnrollmentDate'] = pd.to_datetime(data['EnrollmentDate'], errors = 'coerce')
median_date = data['EnrollmentDate'].dropna().median()
print("Median enrollment date:", median_date)

data['EnrollmentDate'] = data['EnrollmentDate'].fillna(median_date)

data['EnrollmentDate'] = data['EnrollmentDate'].dt.strftime('%Y-%m-%d')
print(data)

clean_data = data.copy()
print(clean_data.to_excel("student.xlsx"))