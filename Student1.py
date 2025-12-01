#importing the necessary libraries
import numpy as np
import pandas as pd

#loading the dataset
path = r'Student_Messy1.csv'
df = pd.read_csv(path)

#checking column behaviour
print(df['name'].head())#gives top 5 columns
print(df['name'].sample(10))#random values
print(df['name'].isnull().sum())

df['name'] = df['name'].astype(str)
df['name'] = df['name'].str.strip()
df['name'] = df['name'].str.replace(r'\s+',' ',regex = True)
df['name'] = df['name'].str.title()
df['name'] = df['name'].replace([''],np.nan)
print(df['name'])

print(df['id'].head())
print(df['id'].isnull().sum())

df['id'] = df['id'].astype(str)
df['id'] = df['id'].str.strip()
df['id'] = df['id'].replace(['',"None",'NA','na','Nan','NaN','Null'],np.nan)
df['id'] = df['id'].str.extract('(\\d+)',expand = False)
df['id'] = pd.to_numeric(df['id'],errors = 'coerce')
missing_count = df['id'].isna().sum()
df.loc[df['id'].isna(),'id'] = range(10000,10000 + missing_count)
df['id'] = df['id'].astype(int)
df = df.sort_values('id').reset_index(drop = True)
df['id'] = df.index + 1
df['id'] = 'S' + df['id'].astype(str).str.zfill(4)
print(df['id'])

print(df['sub1'].head())
print(df['sub1'].sample(10))
print(df['sub1'].isna().sum())

df['sub1'] = df['sub1'].astype(str).str.strip()
df['sub1'] = df['sub1'].replace(['','NA','Null','?','Na','None','none','AB','N/A','absent','Absent','null'],np.nan)
df["sub1"] = df["sub1"].str.extract(r"(\d+)", expand=False)
df['sub1'] = pd.to_numeric(df['sub1'],errors = 'coerce')
df.loc[df['sub1'] > 100 , 'sub1'] = np.nan
df.loc[df['sub1'] < 0 , 'sub1'] = np.nan
df['sub1'] = df['sub1'].fillna(df['sub1'].median())
df['sub1'] = df['sub1'].astype(int)
print(df['sub1'])

df['sub2'] = df['sub2'].astype(str).str.strip()
df['sub2'] = df['sub2'].replace(['','NA','Null','?','Na','None','none','AB','N/A','absent','Absent','null'],np.nan)
df["sub2"] = df["sub2"].str.extract(r"(\d+)", expand=False)
df['sub2'] = pd.to_numeric(df['sub2'],errors = 'coerce')
df.loc[df['sub2'] > 100 , 'sub2'] = np.nan
df.loc[df['sub2'] < 0 , 'sub2'] = np.nan
df['sub2'] = df['sub2'].fillna(df['sub2'].median())
df['sub2'] = df['sub2'].astype(int)

df['sub3'] = df['sub3'].replace(['','NA','Null','?','Na','None','none','AB','N/A','absent','Absent','null'],np.nan)
df["sub3"] = df["sub3"].str.extract(r"(\d+)", expand=False)
df['sub3'] = pd.to_numeric(df['sub3'],errors = 'coerce')
df.loc[df['sub3'] > 100 , 'sub3'] = np.nan
df.loc[df['sub3'] < 0 , 'sub3'] = np.nan
df['sub3'] = df['sub3'].fillna(df['sub3'].median())
df['sub3'] = df['sub3'].astype(int)
print(df['sub3'])

df['marks'] = df['sub1'] + df['sub2'] + df['sub3']
df['marks'] = df['marks'].astype(int)
print(df['marks'])

df['percentage'] = df['percentage'].astype(str).str.strip()
df['percentage'] = df['percentage'].replace("","%",regex = False)

df["percentage"] = df["percentage"].replace(
    ["", "None", "none", "NaN", "nan", "NA", "na",
     "N/A", "null", "Null", "absent", "incomplete"],
    np.nan
)
df["percentage"] = df["percentage"].str.extract(r"(\d+\.?\d*)", expand=False)
df["percentage"] = pd.to_numeric(df["percentage"], errors="coerce")
df.loc[df["percentage"] > 100, "percentage"] = np.nan
df.loc[df["percentage"] < 0, "percentage"] = np.nan
df["percentage"] = df["marks"] / 3
df["percentage"] = df["percentage"].fillna(df["percentage"].median())
print(df['marks'])

df['result'] = df['result'].astype(str).str.strip()
df['result'] = df['result'].str.lower()
df['result'] = df['result'].replace(['','NA','Null','NA','none'],np.nan)
df["percentage"] = df["percentage"].fillna(df["percentage"].median())
df["result"] = df["result"].replace({
    "pass": "Pass",
    "passed": "Pass",
    "cleared": "Pass",
    "promoted": "Pass",
    
    "fail": "Fail",
    "failed": "Fail",
    "compartment": "Fail",
    "supp": "Fail",
    "supplementary": "Fail"
})
print(df['result'].unique())
df.loc[df["result"].isna(), "result"] = df["percentage"].apply(
    lambda x: "Pass" if x >= 40 else "Fail"
)
print(df['result'])

df["grade"] = df["grade"].astype(str).str.strip().str.lower()
import numpy as np

df["grade"] = df["grade"].replace(
    ["", "none", "nan", "na", "null"],
    np.nan
)
grade_map = {
    "a": "A", "a+": "A", "distinction": "A",

    "b": "B", "b+": "B", "good": "B",

    "c": "C", "average": "C",

    "d": "D", "below avg": "D", "below average": "D",

    "f": "F", "fail": "F", "failed": "F", "poor": "F"
}

df["grade"] = df["grade"].replace(grade_map)
valid_grades = ["A", "B", "C", "D", "F"]
df.loc[~df["grade"].isin(valid_grades), "grade"] = np.nan
print(df['grade'])
df["age"] = df["age"].astype(str).str.strip()

# Replace bad/null values
df["age"] = df["age"].replace(
    ["", "none", "nan", "null", "na"],
    np.nan
)

# Extract ONLY digits
df["age"] = df["age"].str.extract(r"(\d+)", expand=False)

# Convert to numeric
df["age"] = pd.to_numeric(df["age"], errors="coerce")

# Remove unrealistic ages
df.loc[(df["age"] < 14) | (df["age"] > 25), "age"] = np.nan

# Fill missing with median
df["age"] = df["age"].fillna(df["age"].median()).astype(int)


df["course_enrollment_date"] = df["course_enrollment_date"].astype(str).str.strip()

# Replace invalid / null-like values
df["course_enrollment_date"] = df["course_enrollment_date"].replace(
    ["", "none", "nan", "null", "na", "00-00-0000", "not a date"],
    np.nan
)

# Try parsing multiple formats automatically
df["course_enrollment_date"] = pd.to_datetime(
    df["course_enrollment_date"],
    errors="coerce",
    dayfirst=True
)

# Optional: Fill missing with most common date (mode)
df["course_enrollment_date"] = df["course_enrollment_date"].fillna(
    df["course_enrollment_date"].mode()[0]
)

df["random_color"] = df["random_color"].astype(str).str.strip()

df["random_color"] = df["random_color"].replace(
    ["", "none", "null", "nan", "na"],
    np.nan
)

df["random_color"] = df["random_color"].str.lower()
df["device_id"] = df["device_id"].astype(str).str.strip()

df["device_id"] = df["device_id"].replace(
    ["none", "null", "nan", "na", "", "0000", "XXXXXXXX", "id_missing"],
    np.nan
)

Student_Clean = df.copy()
print(Student_Clean.to_excel('Student_Clean1.xlsx'))


