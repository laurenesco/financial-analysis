import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tabulate import tabulate

# Analysis subs
def get_income(df):
    credits = df[df.Amount > 0]
    income = credits.Amount.sum()

    return income

def get_expenses(df):
    debits = df[df.Amount < 0]
    expenses = debits.Amount.sum()

    return expenses

def get_visualization_df(df, groceries):
    if (groceries == 1):
        filtered_df = df[(df['Amount'] < 0) & (df['Category'] != 'Transfer')]
    else:
        filtered_df = df[(df['Amount'] < 0) & (df['Category'] != 'Transfer') & (df['Category'] != 'Groceries')]

    filtered_df.loc[:, 'Amount'] = filtered_df['Amount'].abs()
    spending_by_category = filtered_df.groupby('Category')['Amount'].sum()

    return spending_by_category

def show_pie_chart(spending_df):
    plt.figure(figsize=(6, 6))

    # Create a color map with a number of colors
    num_categories = len(spending_df)

    cmap = plt.get_cmap('tab20')
    colors = cmap(range(num_categories))
    
    plt.pie(spending_df, labels=spending_df.index, colors=colors, startangle=250)
    plt.axis('equal')
    plt.title('Spending Distribution by Category')
    plt.show()

def print_stats(income_df, expense_df, account_name):
    print("\n")
    print("{} Pay: ${:.2f}".format(account_name, income_df))
    print("{} Expense: ${:.2f}".format(account_name, expense_df))
    print("{} Net: ${:.2f}".format(account_name, income_df + expense_df))
    print("\n\n")
    return

# Data preprocessing subs
def rename_categories(df):
    df.loc[:, 'Category'] = df['Category'].astype('object')
    
    # Renaming
    df.loc[df['Category'] == 'Rental Car & Taxi', 'Category'] = 'Uber'
    
    # Consolidating
    df.loc[df['Category'] == 'Paycheck', 'Category'] = 'Income'
    df.loc[df['Category'] == 'Interest Income', 'Category'] = 'Income'
    df.loc[df['Category'] == 'Mortgage & Rent', 'Category'] = 'Bills & Utilities'
    df.loc[df['Category'] == 'Credit Card Payment', 'Category'] = 'Bills & Utilities'
    df.loc[df['Category'] == 'Utilities', 'Category'] = 'Bills & Utilities'
    df.loc[df['Category'] == 'Financial', 'Category'] = 'Bills & Utilities'
    df.loc[df['Category'] == 'Pet Food & Supplies', 'Category'] = 'Pets'
    df.loc[df['Category'] == 'Service & Parts', 'Category'] = 'Auto & Transport'
    df.loc[df['Category'] == 'Clothing', 'Category'] = 'Shopping'
    df.loc[df['Category'] == 'Sporting Goods', 'Category'] = 'Shopping'
    df.loc[df['Category'] == 'Amusement', 'Category'] = 'Entertainment'
    df.loc[df['Category'] == 'Books', 'Category'] = 'Hobbies'
    df.loc[df['Category'] == 'Television', 'Category'] = 'Subscription'
    df.loc[df['Category'] == 'Subscriptions', 'Category'] = 'Subscription'
    df.loc[df['Category'] == 'Food & Dining', 'Category'] = 'Food'
    df.loc[df['Category'] == 'Restaurants', 'Category'] = 'Food'
    df.loc[df['Category'] == 'Fast Food', 'Category'] = 'Fast Food'
    df.loc[df['Category'] == 'Coffee Shops', 'Category'] = 'Fast Food'
    df.loc[df['Category'] == 'Cash', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Business Services', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Fees & Charges', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Movies & Dvds', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Music', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Doctor', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Electronics & Software', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Auto & Transport', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Home Services', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Hotel', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == 'Home', 'Category'] = 'Uncategorized'
    df.loc[df['Category'] == '', 'Category'] = 'Uncategorized'
    
    return df

# Put recurring charges where they belong
def organize_recurring_charges(df):
    df.loc[df['Description'] == 'Southwest Resear Payroll', 'Category'] = 'Income'
    df.loc[df['Description'].str.contains('txtag', case=False, na=False), 'Category'] = 'Bills & Utilities'
    df.loc[df['Description'].str.contains('openai', case=False, na=False), 'Category'] = 'Bills & Utilities'
    df.loc[df['Description'].str.contains('car wash', case=False, na=False), 'Category'] = 'Auto & Transport'
    df.loc[df['Description'].str.contains('sherwood', case=False, na=False), 'Category'] = 'Pets'
    df.loc[df['Description'].str.contains('auravia', case=False, na=False), 'Category'] = 'Medical'
    df.loc[df['Description'] == 'Scratchpay.com', 'Category'] = 'Veterinary'
    df.loc[df['Description'] == 'Google Drive', 'Category'] = 'Subscription'
    df.loc[df['Description'] == 'Google One', 'Category'] = 'Subscription'
    df.loc[df['Description'] == 'Crunchyroll', 'Category'] = 'Subscription'
    df.loc[df['Description'] == 'Apple', 'Category'] = 'Subscription'
    df.loc[df['Description'] == 'Internet Withdrawal', 'Category'] = 'Transfer'
    df.loc[df['Description'] == 'Vee?s Chop Shop', 'Category'] = 'Grooming'    
    df.loc[df['Description'] == 'U-Haul', 'Category'] = 'Moving Costs'
    df.loc[df['Description'] == 'Nintendo', 'Category'] = 'Shopping'
    df.loc[df['Description'] == 'W Loop', 'Category'] = 'Shopping'
    df.loc[df['Description'] == 'Seat Engine', 'Category'] = 'Entertainment'
    df.loc[df['Description'].str.contains('flix', case=False, na=False), 'Category'] = 'Entertainment'
    df.loc[df['Description'] == 'Pi Shop Inc', 'Category'] = 'Hobbies'
    df.loc[df['Description'].str.contains('american food', case=False, na=False), 'Category'] = 'Vending Machine'
    df.loc[df['Description'].str.contains('mcdonald', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('starbucks', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('in-n-out', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('chick-fil-a', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('raising cane', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('bill miller', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('jimmy john', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('pizza', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('chipotle', case=False, na=False), 'Category'] = 'Fast Food'
    df.loc[df['Description'].str.contains('doordash', case=False, na=False), 'Category'] = 'DoorDash'
    df.loc[df['Description'].str.contains('uber eats', case=False, na=False), 'Category'] = 'DoorDash'

    return

def print_fancy(df):
    print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
    return

def print_category(df, category):
    cat_df = df[df['Category'] == category]
    print(tabulate(cat_df, headers="keys", tablefmt="fancy_grid"))

    return