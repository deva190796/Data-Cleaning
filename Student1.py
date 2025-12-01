
import numpy as np
import pandas as pd

path = r"Student_Messy1.csv"
df = pd.read_csv(path)

df["name"] = df["name"].astype(str)
df["name"] = df["name"].str.strip()
df["name"] = df["name"].str.replace(r"\s+", " ", regex=True)
df["name"] = df["name"].str.title()
df["name"] = df["name"].replace(["", "None", "none", "NaN", "nan", "NA", "na"], np.nan)


df["id"] = df["id"].astype(str).str.strip()
df["id"] = df["id"].replace(
    ["", "None", "NA", "na", "Nan", "NaN", "Null", "null", "nan"],
    np.nan
)

# keep only digits
df["id"] = df["id"].str.extract(r"(\d+)", expand=False)

# to numeric
df["id"] = pd.to_numeric(df["id"], errors="coerce")

# fill missing id with temporary numbers
missing_count = df["id"].isna().sum()
df.loc[df["id"].isna(), "id"] = range(10000, 10000 + missing_count)
df["id"] = df["id"].astype(int)

df = df.sort_values("id").reset_index(drop=True)
df["id"] = df.index + 1
df["id"] = "S" + df["id"].astype(str).str.zfill(4)


def clean_marks_column(df, col):
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace(
        ["", "NA", "Null", "?", "Na", "None", "none", "AB", "N/A",
         "absent", "Absent", "null"],
        np.nan
    )
    # extract digits
    df[col] = df[col].str.extract(r"(\d+)", expand=False)
    # convert to numeric
    df[col] = pd.to_numeric(df[col], errors="coerce")
    # impossible values
    df.loc[df[col] > 100, col] = np.nan
    df.loc[df[col] < 0, col] = np.nan
    # fill with median
    df[col] = df[col].fillna(df[col].median())
    # make integer
    df[col] = df[col].astype(int)
    return df


df = clean_marks_column(df, "sub1")
df = clean_marks_column(df, "sub2")
df = clean_marks_column(df, "sub3")


df["marks"] = df["sub1"] + df["sub2"] + df["sub3"]
df["marks"] = df["marks"].astype(int)

df["percentage"] = df["percentage"].astype(str).str.strip()
df["percentage"] = df["percentage"].str.replace("%", "", regex=False)
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
df["percentage"] = df["percentage"].astype(float)


df["result"] = df["result"].astype(str).str.strip().str.lower()
df["result"] = df["result"].replace(
    ["", "na", "null", "none", "nan"],
    np.nan
)

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

df.loc[~df["result"].isin(["Pass", "Fail"]), "result"] = np.nan

df.loc[df["result"].isna(), "result"] = df["percentage"].apply(
    lambda x: "Pass" if x >= 40 else "Fail"
)


df["grade"] = df["grade"].astype(str).str.strip().str.lower()
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

def grade_from_percentage(p):
    if p >= 75:
        return "A"
    elif p >= 60:
        return "B"
    elif p >= 50:
        return "C"
    elif p >= 40:
        return "D"
    else:
        return "F"

mask_missing_grade = df["grade"].isna() & df["percentage"].notna()
df.loc[mask_missing_grade, "grade"] = df.loc[mask_missing_grade, "percentage"].apply(grade_from_percentage)


df["age"] = df["age"].astype(str).str.strip()
df["age"] = df["age"].replace(
    ["", "none", "nan", "null", "na"],
    np.nan
)

df["age"] = df["age"].str.extract(r"(\d+)", expand=False)
df["age"] = pd.to_numeric(df["age"], errors="coerce")

df.loc[(df["age"] < 14) | (df["age"] > 25), "age"] = np.nan

df["age"] = df["age"].fillna(df["age"].median()).astype(int)


df["study_hrs_per_day"] = df["study_hrs_per_day"].astype(str).str.strip()

df["study_hrs_per_day"] = df["study_hrs_per_day"].replace(
    ["", "none", "nan", "na", "null", "zero"],
    np.nan
)

df["study_hrs_per_day"] = df["study_hrs_per_day"].str.replace("hrs", "", regex=False)
df["study_hrs_per_day"] = df["study_hrs_per_day"].str.replace("hour", "", regex=False)
df["study_hrs_per_day"] = df["study_hrs_per_day"].str.replace("hours", "", regex=False)

df["study_hrs_per_day"] = df["study_hrs_per_day"].str.extract(r"(\d+\.?\d*)", expand=False)
df["study_hrs_per_day"] = pd.to_numeric(df["study_hrs_per_day"], errors="coerce")

df.loc[(df["study_hrs_per_day"] < 0) | (df["study_hrs_per_day"] > 24), "study_hrs_per_day"] = np.nan

df["study_hrs_per_day"] = df["study_hrs_per_day"].fillna(df["study_hrs_per_day"].median())

df["course_enrollment_date"] = df["course_enrollment_date"].astype(str).str.strip()
df["course_enrollment_date"] = df["course_enrollment_date"].replace(
    ["", "none", "nan", "null", "na", "00-00-0000", "not a date"],
    np.nan
)

df["course_enrollment_date"] = pd.to_datetime(
    df["course_enrollment_date"],
    errors="coerce",
    dayfirst=True
)

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
Student_Clean.to_excel("Student_Clean1.xlsx", index=False)
print("Cleaning complete. Saved as Student_Clean1.xlsx")
