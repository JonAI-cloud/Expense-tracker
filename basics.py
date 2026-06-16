
expenses = []

def get_total(expenses):
    total = 0
    for expense in expenses:
        total = total + expense["amount"]
    return total

def add_expense(name, amount, category="general"):
    return {"name": name, "amount": amount, "category": category}

def get_category(amount):
    if amount < 10:
        return "small"
    elif amount <= 50:
        return "medium"
    else:
        return "large"


def print_expenses(expenses):
    for expense in expenses:
        category = get_category(expense["amount"])
        print(f"{expense['name']}: {expense['amount']} kr ({category})")


def main():
    expenses.append(add_expense("coffee", 4.5))
    expenses.append(add_expense("lunch", 12.0))
    expenses.append(add_expense("taxi", 85.0))
    print_expenses(expenses)
    print(f"Total: {get_total(expenses)} kr")

main()



    


