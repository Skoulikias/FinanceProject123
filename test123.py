import pandas as pd
import os

KEYWORDS = {
    'Income': ['income', 'salary', 'allowance'],
    'Needs': ['rent', 'bills', 'utilities', 'food', 'groceries', 'transport', 'insurance'],
    'Wants': ['shopping', 'entertainment', 'restaurants', 'movies', 'subscriptions'],
    'Savings': ['savings', 'investment'] 
}

file_path = "ExcelFileActualNameWhenWeAreReadyToTestIt.xlsx"
def openexcel(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File Not Found: {file_path}")
    
    data = pd.read_excel(file_path,sheet_name=None)
    combined = pd.concat(data.values(), ignore_index=True)

    return combined

def categorize(df, description_column="Description"):
    df["Group"] = "Uncategorized"

    for i, row in df.iterrows():
        description = str(row[description_column]).lower()
        for group, words in KEYWORDS.items():
            for word in words:
                if word in description: 
                    df.at[i,"Group"] = group
                    break

            if df.at[i,"Group"] != "Uncategorized": 
                break
    return df

df = openexcel(file_path)        
df = categorize(df, "Description")
print(df["Group"].value_counts())

def analyse(df, column="Amount"):
    income = 0
    expenses = 0

    for i, row in df.iterrows():
        amount = float(row[column])
        group = row["Group"]

        if group == "Income":
            income += amount
        else:
            expenses += amount

    savings = income - expenses

    print("----- Financial Summary -----")
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expenses}")
    print(f"Savings: {savings}") 
    
def grouping(df, column="Amount"):
    totals = {}

    for i, row in df.iterrows():
        group = row["Group"]
        amount = float(row[column])

        if group in totals:
            totals[group] += amount
        else:
            totals[group] = amount

    print("\n----- Category Breakdown -----")
    for group, total in totals.items():
        print(f"{group}: {total}")       

df = openexcel(file_path)        
df = categorize(df, "Description")

print(df["Group"].value_counts())

analyse(df, "Amount")
grouping(df, "Amount")
