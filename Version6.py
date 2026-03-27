import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
KEYWORDS = {
    'Income': ['income', 'salary', 'allowance'],
    'Needs': ['rent', 'bills', 'utilities', 'food', 'groceries', 'transport', 'insurance'],
    'Wants': ['shopping', 'entertainment', 'restaurants', 'movies', 'subscriptions'],
    'Savings': ['savings', 'investment'] 
}

file_path = "/Users/greco/Downloads/finance_test_data.xlsx"
def openexcel(file_path): #Function to open the excel file and combine all sheets into one dataframe
    if not os.path.exists(file_path): #Checks if the file exists and if not it will show error message
        raise FileNotFoundError(f"File Not Found: {file_path}")
    
    data = pd.read_excel(file_path,sheet_name=None) #Reads all the sheets in the excel file and stores them in a dictionary
    combined = pd.concat(data.values(), ignore_index=True) #merges all the sheets into one big dataframe

    return combined

def categorize(df, description_column="Description"): #Function to categorize each transaction based specific keywords
    df["Group"] = "Uncategorized"

    for i, row in df.iterrows(): #Loops through each row of the dataframe
        description = str(row[description_column]).lower() #Lowercase so that it matches the dictionary
        for group, words in KEYWORDS.items():
            for word in words:
                if word in description: #If keyword is found it puts them in the correct category
                    df.at[i,"Group"] = group
                    break

            if df.at[i,"Group"] != "Uncategorized": 
                break
    return df

def positive(df):
    df["Amount"] = df["Amount"].abs()
    return df




def analyse(df, column="Amount"): #Function that analyzes income, expenses and savings (basic mathematics)
    income = 0
    expenses = 0

    for i, row in df.iterrows(): #Goes through every row (loop)
        amount = float(row[column]) #Turns the amount into float so that it can do mathematics with it (cant add and substract strings for math)
        group = row["Group"] #Gets the category of the transaction

        if group == "Income":
            income += amount #Accumulates the income
        else:
            expenses += amount #If its not income its expense

    savings = income - expenses #Savings is whatever you have left so income  - expenses (incomes need to be positive of course)

    print(" Financial Summary ")
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expenses}")
    print(f"Savings: {savings}") 
    
def grouping(df, column="Amount"): #Function to show the total of each category and see where the big totals are coming from
    totals = {} #open a dictionary

    for i, row in df.iterrows(): #goes through every frame of the data frame
        group = row["Group"] #gets the category of the transaction
        amount = float(row[column]) #turns it into a float so that we can do math with it

        if group in totals: #If the category already exists its add to the total, if it doesnt it makes a new entry
            totals[group] += amount
        else:
            totals[group] = amount

    print("\n Category Breakdown ")
    for group, total in totals.items(): #goes through the totals dictionary and prints the total of each category
        print(f"{group}: {total}")       



def ArrangeTheData(df): #Function to clean the data and format everything to prevent crashes and errors
    df = df.dropna(subset=["Amount", "Description"]) #Drops rows that have missing values in the Amount or Description columns

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce") #Convert all the amounts into numbers and if it is not a number it becomes NaN which means not a number and it gets disregarded
    df = df.dropna(subset=["Amount"])

    df["Description"] = df["Description"].astype(str).str.strip().str.lower() #cleans the description column so that it can match the dictionary keywords
    if "Date" in df.columns: #checks for a date column and changes it into time frame format so we can use that for further analysis
       
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"]) #removes rows with invalid dates
    return df



def plotdifferentcategories(df): #function to plot the different categories
    totals = df.groupby("Group")["Amount"].sum()
    
    totals.plot(kind="bar") 
    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.show()

def statistics(df): #function to calculate basic statistics
    mean = df["Amount"].mean() #average
    std = df["Amount"].std() #standard deviation (the spread of the data)
    var = df["Amount"].var() #variance (spread squared)

    print("\n Statistics ")
    print(f"Mean Spending: {mean}")
    print(f"Standard Deviation: {std}")
    print(f"Variance: {var}")

    return mean, std


def buildtimeseries(df): #function to build a time series (which is the spending over time)
    df = df.sort_values("Date") #sorts data by date
    
    
    daily = df.groupby("Date")["Amount"].sum()#groups all the data by date and adds the amounts
    
    return daily

def derivatives(timeseries): #function to calculate the rate of change (derivative)
    derivative = timeseries.diff() #diff is the difference between each value and the previous one (deriavtive)
    return derivative

def integrals(timeseries): #function to calculate the cumulative spending (integral)
    cumulative = timeseries.cumsum() #cumsum is cumulative sum which is the integral
    return cumulative


def plottimeseries(ts, derivative, cumulative): #function to plot the last 3 functions which is time series, derivatives and the integrals
    plt.figure()
    ts.plot(label="Spending over Time") #original spending
    derivative.plot(label="Rate of Change over Time") #change in spending
    cumulative.plot(label="Cumulative Spending over Time") #total over time   
    
    plt.legend()
    plt.title("Time-Series Financial Analysis")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.show()
#BEHAVIORAL ANALYSIS
budget = float(input("Enter your budget: "))
def budgetbehavior(ts, derivative, cumulative, budget): #Function to analyze the budget and gives you insight on behavior
    print("\n Budget & Behavioral Analysis ") #Prints the title

    final_spending = cumulative.iloc[-1] #it gets the final cumulative spending which is the total spending at the end of the time series

    if final_spending > budget: #If the spending is bigger than your budget (you have gone above)
        print("You have exceeded your budget.")
    elif final_spending > 0.8 * budget: #If you are close to your budget (more than 80%)
        print("You are close to exceeding your budget.")
    else:
        print("You are within your budget.")

    threshold = derivative.std() * 1.5  #It calculates a threshold that is considered a significant change

    for i in range(1, len(derivative)): #it goes through all the derivatives (results of the rate of change) and checks for signifcant change
        change = derivative.iloc[i] #gets the change
        date = derivative.index[i]#gets the date of the change

        if abs(change) > threshold: #if the change is bigger than the threshold its considered a signifcant change
            if change > 0: #if its positive its a sudden increase, if negatgive its a sudden decrease
                print(f"Sudden increase in spending around {date.date()}")
            else:
                print(f"Sudden decrease in spending around {date.date()}")

    averagetrend = derivative.mean() #it calculates the average trend of the spending

    if averagetrend > 0: #if positive it increases, if its negative it decreases
        print("Your spending trend suggests you may exceed your budget in the future.")
    else:
        print("Your spending trend is stable or decreasing.")


#MONTECARLO SIMULATION
def montecarlo(df, months=12, simulations=10000): #function for montecarlo simulation, 12 months for 1 year and 10 0000 simulations (could add more to make it more accurate but it takes more time to run)
   
    expenses = df[df["Group"] != "Income"].copy() #creates new data frame and only takes expenses and not income (df equals only stuff that isnt income so  it only takes expenses)

    expenses["Amount"] = expenses["Amount"].abs() #In the excel file expenses are negative but we have to make them positive so we take the absolute vaue (montecarlo doesnt work with negative values for this case)

    mean = expenses["Amount"].mean() #calculates the mean
    std = expenses["Amount"].std() #calculates standard deviation

    results = [] #creates empty list

    for _ in range(simulations): #loops through all the different simulations (10 000 times total)
        total = 0 #sets total for every simluation to 0
        for _ in range(months): #loops through each month (12 months because 12 in a year)
            value = np.random.normal(mean, std) #picks a random number and sets it as the value (a normal number for the month that respects the normal distribution so it matches the mean and standard deviation)
            total += max(value, 0)  #adds the value to the total but if its negative it adds 0 so we avoid negative spending
        results.append(total) #after 12 months it adds the total to the result list

    return np.array(results) #turns the results into a numpy array so we can use calculations and plot with it


def plotmontecarlo(results):
    plt.figure(figsize=(10,6))
    plt.hist(results, bins=50)  #plots histogram (this creates the bell curve)
    plt.title("Monte Carlo Simulation - Total Spending")
    plt.xlabel("Total Spending (12 months)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()


df = openexcel(file_path) #load excel data
df = ArrangeTheData(df) #clean and format the data
df = categorize(df, "Description") #categorize the data based on description  and keywords
df = categorize(df, "Description")
df = positive(df)
print(df["Group"].value_counts()) #show how many transactions in ecah category
analyse(df, "Amount") #analyze all the data and show the summary
grouping(df, "Amount") #show the total of each category as an amount
mean, std = statistics(df) #Does the basic statistics
plotdifferentcategories(df) #plots the different categories (graph 1)
expenses_df = df[df["Group"] != "Income"].copy() #creates a new dataframe because we want to calculate only expeneses, if we put income it messes up the graph
expenses_df["Amount"] = expenses_df["Amount"].abs() #turns all the expenses that are negative in the excel into positives so that we can do the calculations
ts = buildtimeseries(expenses_df) #builds the time series of the expenses so that we can do calculations 
derivative = derivatives(ts) #calculates the rate of change of the spending
cumulative = integrals(ts) #calculates the cumulative spending
plottimeseries(ts, derivative, cumulative) #plots the timeseries, derivatives and integrals
budgetbehavior(ts, derivative, cumulative, budget)#analyzes the budget and gives you insights on your behaviour
results = montecarlo(df) #defines results and runs the montecarlo simulation
#Run the Montecarlo simulation and print the results
print("\n Monte Carlo Results ")
print(f"Average total spending: {results.mean():.2f}")
print(f"Max spending: {results.max():.2f}")
print(f"Min spending: {results.min():.2f}")

plotmontecarlo(results)


