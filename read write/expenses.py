import csv
from rich.table import Table
from rich.console import Console
from datetime import date

#Expense Tracker - command line app to log and manage daily expenses
#Built during week 1 of the engineering learning program

console = Console()

expenses = []

def get_total(expenses):
    """Calculate and return the total amount across all expenses"""
    total = 0
    for expense in expenses:
        total = total + expense["amount"]
    return total

def add_expense(name, amount, category="general"):
    return {"name": name, 
            "amount": amount, 
            "category": category,
            "date": str(date.today()) #date.today give todays date and str makes it into a string
    }

def get_category(amount):
    if amount < 10:
        return "small"
    elif amount <= 50:
        return "medium"
    else:
        return "large"

def print_expenses(expenses):
    table = Table(title="Expenses")
    table.add_column("Date", style="yellow")
    table.add_column("Name", style="cyan")
    table.add_column("Amount", style="green")
    table.add_column("Category", style="magenta")

    for expense in expenses:
        category = get_category(expense["amount"])
        table.add_row(
            expense["date"],
            expense["name"],
            f"{expense['amount']} kr",
            category
        )
    
    console.print(table)

def save_expenses(expenses, filename="expenses.csv"):
    with open(filename, "w", newline="") as f:
        fieldnames = ["name", "amount", "category", "date"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader() # writes "name,amount" as first row
        writer.writerows(expenses) # writes every dict as a row

def load_expenses(filename="expenses.csv"):
    try:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            expenses = []
            for row in reader:
                expenses.append({
                    "name": row["name"],
                    "amount": float(row["amount"]), #convert string to number
                    "category": row["category"],
                    "date": row["date"]
                })
            return expenses
    except FileNotFoundError:
        return[] # no file yet, return empty list

def add_expense_prompt(expenses):
    name = input("Expense name: ")
    try:
        amount = float(input("Amount (kr): "))
    except ValueError:
        print("Invalid amount, please enter a number")
        return
    expenses.append(add_expense(name, amount))
    print(f"Added {name} for {amount} kr")

def print_summary(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    total = get_total(expenses)
    console.print(f"[bold]Total expenses:[/bold] {total} kr")
    console.print(f"[bold]Number of expenses:[/bold] {len(expenses)}")
    console.print(f"[bold]Average:[/bold] {total / len(expenses): .2f} kr")


def delete_expense(expenses):
    name = input("Enter the name of the expense to delete: ")
    for expense in expenses:
        if expense["name"].lower() == name.lower():
            expenses.remove(expense)
            print(f"deleted {name}")
            return
    print(f"No expense called '{name}' found")


def print_expenses_sorted(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    sorted_list = sorted(expenses, key=lambda expense: expense["amount"], reverse = True)
    print_expenses(sorted_list)

def print_expenses_by_category(expenses):
    category = input("Enter category (small / medium / large): ").lower()

    if category not in ["small", "medium", "large"]:
        print("Invalid category. Please enter small, medium or large.")
        return
    
    filtered = [e for e in expenses if get_category(e["amount"]) == category]

    if not filtered:
        print(f"No {category} expenses found.")
        return
    
    print_expenses(filtered)


def save_budget(budget, filename="budget.txt"):
    with open(filename, "w") as f:
        f.write(str(budget))

def load_budget(filename="budget.txt"):
    try:
        with open(filename, "r") as f:
            return float(f.read())
    except FileNotFoundError:
        return None #No budget set yet
    
def check_budget(expenses, budget):
    if budget is None:
        return
    total = get_total(expenses)
    percentage = (total / budget) * 100

    if total > budget:
        console.print(f"[bold red] Over budget! Spent {total:.2f} kr of {budget:.2f} kr ({percentage:.0f}%[/bold red])")
    elif percentage >= 80:
        console.print(f"[bold yellow] Warning: {percentage:.0f}% of budget used ({total:.2f} kr of {budget :.2f} kr)[/bold yellow]")
    else:
        console.print(f"[green]Budget: {total:.2f} kr of {budget:.2f} kr used ({percentage:.0f}%)[/green]")  


def set_budget_prompt():
    try:
        budget = float(input("Enter monthly budget (kr): "))
        save_budget(budget)
        print(f"Budget set to {budget:.2f} kr")
        return budget
    except ValueError:
        print("Invalid amount, please enter a number.")
        return None

def main():
    expenses = load_expenses() #load from file at startup
    budget = load_budget()

    while True:
        console.print("\n[bold cyan]=== Expense Tracker ===[/bold cyan]")
        check_budget(expenses, budget) # shows budget status on every menu
        console.print("[green]1.[/green] Add expense")
        console.print("[green]2.[/green] Delete expense")
        console.print("[green]3.[/green] View all expenses")
        console.print("[green]4.[/green] View summary")
        console.print("[green]5.[/green] View expenses by amount")
        console.print("[green]6.[/green] Sort by category")
        console.print("[green]7.[/green] Set budget")
        console.print("[red]8.[/red] Quit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_expense_prompt(expenses)
            check_budget(expenses, budget) # warns immediately after adding 
        elif choice == "2":
            delete_expense(expenses)
        elif choice == "3":
            print_expenses(expenses)
        elif choice == "4":
            print_summary(expenses)
        elif choice == "5":
            print_expenses_sorted(expenses)
        elif choice == "6":
            print_expenses_by_category(expenses)
        elif choice == "7":
            budget = set_budget_prompt() 

        elif choice == "8":
            save_expenses(expenses)
            print("Expenses saved, Goodbye!")
            break
        
        else:
            print("invalid option, please enter 1-4")
        

main()

