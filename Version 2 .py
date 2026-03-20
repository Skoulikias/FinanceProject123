import pandas as pd
import os
import matplotlib.pyplot as plt

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

    print(" Financial Summary ")
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

    print("\n Category Breakdown ")
    for group, total in totals.items():
        print(f"{group}: {total}")       



def ArrangeTheData(df):
    df = df.dropna(subset=["Amount", "Description"])

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce") #when I come back to annotate the whole code dont forget to explain what a NaN is and what error does and how it deletes the mistakes
    df = df.dropna(subset=["Amount"])

    df["Description"] = df["Description"].astype(str).str.strip().str.lower()
    if "Date" in df.columns:
       
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
    return df



def plot_categories(df):
    totals = df.groupby("Group")["Amount"].sum()
    
    totals.plot(kind="bar")
    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.show()

def statistics(df):
    mean = df["Amount"].mean()
    std = df["Amount"].std()
    var = df["Amount"].var()

    print("\n Statistics ")
    print(f"Mean Spending: {mean}")
    print(f"Standard Deviation: {std}")
    print(f"Variance: {var}")

    return mean, std
#Run the all the functions section, to be edited later
df = openexcel(file_path)
df = ArrangeTheData(df)
df = categorize(df, "Description")
print(df["Group"].value_counts())
analyse(df, "Amount")
grouping(df, "Amount")
mean, std = statistics(df)
plot_categories(df)