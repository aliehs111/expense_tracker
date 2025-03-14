import datetime
import csv
import os
print("Current working directory:", os.getcwd()) #to verify where my script is running

expenses = []
categories = ("housing", "household", "utilities", "food", "medical", "entertainment", "investment", "education", "pets", "car", "car maintenance", "gas")
categories_list = list(categories)# for when user adds a category
monthly_budgets = {}
#check if date is correct format
def valid_date(date_str):
   try:
       datetime.datetime.strptime(date_str, "%Y-%m-%d")
       return True
   except ValueError:
      return False

#enter an expense

def add_expense(date, category, amount, description):
   if category not in categories_list:
      print("Invalid Category.  Please choose from these categories:", categories_list)
      return
   #if date is not correct format
   if not valid_date(date):
       print("Invalid Date Format.  Please enter as YYYY-MM-DD")
       return
   #define an expense dictionary once the user input is validated
   expense = {
       "date": date,
       "category": category,
       "amount": amount,
       "description": description
   }

   #add this expense to the current expense list
   expenses.append(expense)
   print("Expense added to tracker")

# view expenses function
def view_expenses():
  if not expenses:
    print("No expenses to display")
    return

#look for expenses to display
  for expense in expenses:
      print("Date:", expense["date"])
      print("Category:", expense["category"])
      print("Amount:", expense["amount"])
      print("Description", expense["description"])
      print("-" * 30)

# budget management-------------------------------------------

#defining the set_monthly_budget function
def set_monthly_budget(category, amount):
    # Check against the categories_list (not the original categories list) in case a user has added categories
    if category not in categories_list:
        print("Invalid Category. Please choose from these categories:", categories_list)
        return
    monthly_budgets[category] = amount
    print(f"Monthly budget for {category} has been set to {amount}")

#defining modify_monthly_budget function
def modify_monthly_budget(category, new_amount):
    global monthly_budgets
    if category in monthly_budgets:
        monthly_budgets[category] = new_amount
        print(f"Budget for {category} modified to {new_amount}.")
    else:
      print("Category '{category}' not found in monthly budgets.  Please choose from {list(monthly_budgets.keys())}")

 #prompt functions to work from main menu - use these for user input then go to actual function to do input verification and to populate the dictionaries with input.
def prompt_add_expense():
  date = input("Enter date (YYY-MM_DD): ")
  category = input ("Enter category: ")
  try:
       amount = float(input("Enter amount: "))
  except ValueError:
    print("Invalid amount.  Please enter a numeric amount with no special characters")
    return
  description = input("Enter description: ")
  add_expense(date, category, amount, description)
   


def prompt_set_monthly_budget_loop():
    global categories_list  # Declare global to update it
    while True:
        print("\nSet Your Monthly Budget")
        print("Select a category to set the budget:")
        for idx, cat in enumerate(categories_list, start=1):
            print(f"{idx}. {cat}")
        print(f"{len(categories_list) + 1}. Add new category")
        print(f"{len(categories_list) + 2}. Done")
        
        choice = input("Enter your choice (number): ").strip()
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if 1 <= choice <= len(categories_list):
            selected_category = categories_list[choice - 1]
        elif choice == len(categories_list) + 1:
            selected_category = input("Enter the new category name: ").strip()
            if selected_category == "":
                print("No category entered. Please try again.")
                continue
            # Check if it already exists, and if not, add it.
            if selected_category not in categories_list:
                categories_list.append(selected_category)
                print(f"New category '{selected_category}' added.")
            else:
                print(f"Category '{selected_category}' already exists.")
        elif choice == len(categories_list) + 2:
            print("Finished setting budgets.")
            break
        else:
            print("Invalid selection. Please try again.")
            continue

        try:
            amount = float(input(f"Enter budget amount for '{selected_category}': ").strip())
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            continue

        set_monthly_budget(selected_category, amount)
        print("\nUpdated Budgets:")
        view_monthly_budget()

        cont = input("\nWould you like to set another budget? (y/n): ").strip().lower()
        if cont != "y":
            break

def prompt_modify_monthly_budget():
    if not monthly_budgets:
        print("No budgets have been set yet.")
        return

    # Create a list of the current budget categories
    budget_categories = list(monthly_budgets.keys())
    print("Current Budgets:")
    for idx, cat in enumerate(budget_categories, start=1):
        print(f"{idx}. {cat} : {monthly_budgets[cat]}")

    # Prompt the user to choose a category by number
    try:
        choice = int(input("Enter the number of the category you want to modify: ").strip())
        if choice < 1 or choice > len(budget_categories):
            print("Invalid selection. Please enter a valid number.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    selected_category = budget_categories[choice - 1]

    # Prompt for the new budget amount
    try:
        new_amount = float(input(f"Enter the new budget amount for '{selected_category}': ").strip())
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    # Call the modify function
    modify_monthly_budget(selected_category, new_amount)


def view_monthly_budget():
    print(f"{'Category':<20}{'Amount':>10}")
    for category, amount in monthly_budgets.items():
        print(f"{category:<20}{amount:>10.2f}")


import datetime

def track_monthly_budget():
    # Get current month in "YYYY-MM" format
    current_month = datetime.datetime.now().strftime("%Y-%m")
    
    # Collect categories from expenses for the current month
    expense_categories = {expense["category"] for expense in expenses if expense["date"].startswith(current_month)}
    
    # Combine categories from monthly_budgets and the expenses to get all categories
    all_categories = set(monthly_budgets.keys()) | expense_categories
    
    # Initialize a dictionary to accumulate spent amounts for each category
    spent = {category: 0.0 for category in all_categories}
    
    # Sum expenses for the current month by category
    for expense in expenses:
        if expense["date"].startswith(current_month):
            category = expense["category"]
            spent[category] += expense["amount"]
    header = f"{'Category':<20}{'Spent':<15}{'Budget':<15}{'Percentage':<15}{'Status':<30}"
    print(header)
    print("-" * len(header))
    # Loop through each category and calculate percentage and status
    for category in sorted(all_categories):
        budget = monthly_budgets.get(category, 0.0)
        amount_spent = spent.get(category, 0.0)
        percentage = (amount_spent / budget * 100) if budget > 0 else 0
        if budget > 0:
            difference = budget - amount_spent
            if difference < 0:
                status = f"***Exceeded by ${abs(difference):.2f}***"
            else:
                status = f"Remaining: ${difference:.2f}"
        else:
            status = "**No budget set**"
        print(f"{category:<20}{amount_spent:<15.2f}{budget:<15.2f}{percentage:<15.2f}{status:<30}")

# --------- Expense Saving and Loading Functions ---------

# Set filenames using today's date
today = datetime.datetime.now().strftime("%Y-%m-%d")
expenses_filename = "testexpenses.csv"
budgets_filename = "testbudgets.csv"

def save_expenses(filename, expenses):
    fieldnames = ["date", "category", "amount", "description"]
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        for expense in expenses:
            writer.writerow(expense)
    print(f"Expenses have been saved to {filename}")

def load_expenses(filename):
    loaded_expenses = []
    with open(filename, mode="r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["amount"] = float(row["amount"])
            loaded_expenses.append(row)
    print(f"Expenses loaded from {filename}")
    return loaded_expenses

# --------- Budget Saving and Loading Functions ---------

def save_budgets(filename, monthly_budgets):
    fieldnames = ["category", "budget"]
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for category, budget in monthly_budgets.items():
            writer.writerow({"category": category, "budget": budget})
    print(f"Budgets have been saved to {filename}")

def load_budgets(filename):
    loaded_budgets = {}
    if not os.path.exists(filename):
        print(f"No saved budgets found in {filename}.")
        return loaded_budgets
    with open(filename, mode="r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            loaded_budgets[row["category"]] = float(row["budget"])
    print(f"Budgets loaded from {filename}")
    return loaded_budgets

# --- Load saved data if available ---
if os.path.exists(expenses_filename):
    expenses = load_expenses(expenses_filename)
    print("DEBUG: expenses after load:", expenses)
else:
    print(f"There are no saved expenses found in {expenses_filename}. Please choose from main menu to add expenses")
if os.path.exists(budgets_filename):
    monthly_budgets = load_budgets(budgets_filename)
    print("DEBUG: monthly_budgets after load:", monthly_budgets)
else:
    print(f"There are no saved budgets found in {budgets_filename}. Please set budgets in the main menu.")

if os.path.exists(budgets_filename):
    monthly_budgets = load_budgets(budgets_filename)
    print("DEBUG: monthly_budgets after load:", monthly_budgets)
    # Update categories_list with any categories from the loaded budgets
    for cat in monthly_budgets.keys():
        if cat not in categories_list:
            categories_list.append(cat)
else:
    print(f"There are no saved budgets found in {budgets_filename}. Please set budgets in the main menu.")


#main menu
def main_menu():

  while True:
    print("\nExpense Tracker Main Menu")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Create Monthly Budget")
    print("4. View Monthly Budget")
    print("5. Modify Monthly Budget")
    print("6. Track Monthly Budget")
    print("7. Exit")
    choice = input("Please input the number of the menu option: ").strip().lower()

    if choice == "1":
       prompt_add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        prompt_set_monthly_budget_loop()
    elif choice == "4":
        view_monthly_budget()
    elif choice == '5':
        prompt_modify_monthly_budget()  
    elif choice == "6":
        track_monthly_budget()
    elif choice == "7":
        save_expenses(expenses_filename, expenses)
        save_budgets(budgets_filename, monthly_budgets)
        print("Your data is saved and this program will exit now.")
        exit()
    else:
        print("Invalid Selection. Please choose from numbers 1-6.")

# assure that the fuction with "main" in the name will be the first to execute
if __name__=="__main__":
   main_menu()