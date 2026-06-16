from rich import print # replaces the built-in print
from rich.table import Table

# coloured text
print("[bold green]It works![/bold green]")
print("[bold red]Warning![/bold red]")

#simple table
table = Table(title="Test table")
table.add_column("Name")
table.add_column("Amount")
table.add_row("coffee", "4.5 kr")
table.add_row("lunch", "12.0 kr")

print(table)