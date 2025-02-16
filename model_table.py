# IGNORE THIS FILE
#####################  V.1.0.0  #################################

"""
        DATABASE MODEL
       ===============

db = {
    "current": 0,  # current == balance
    "history": {
        "DATE" :{
            "reason1": [current balance: int,  transaction: str],
            "reason2": [current balance: int,  transaction: str]
        },
        "01_Jul_23": {
            "reason11": [10, "+10"],
            "reason12": [5, "-5"],
            "reason13": [20, "+15"],
        },
        "02_Jul_23": {
            "reason21": [10, "-10"],
            "reason22": [13, "+3"],
            "reason23": [20, "+17"],
        },
    },
}

"""
"""
            UI MODEL-rich.table
            ===================

from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="MONEY_MANAGER",
              title_style="bold violet",
              show_header=True,
              )

table.add_column("Date", style="dim", header_style="blue")
table.add_column("Flow", header_style="green")
table.add_column("Balance", header_style="yellow")
table.add_column("Reason", header_style="red")

for date, transactions in db["history"].items():
    table.add_row(f"[bold italic]{date}[/]")
    for reason, money in transactions.items():
        table.add_row("", money[1], str(money[0]), reason)
    table.add_section()

console.print(table)
"""
"""
            UI MODEL-Prettytable
            ===================

table = PrettyTable(["Date", "Flow", "Bal", "Reason"])
table.align = 'l'
table._max_width = {"Reason": 17}

for date, transactions in history.items():

    table.add_row([date, '', '', ''])
    for reason, money in transactions.items():
        table.add_row(['', money[1], str(money[0]), reason])
    # table.add_row(['*', '*', '*', '*'], divider=True)

print(table)
"""
#####################################################################
import time
import database

# add people table
# add export table as text file


DATE = time.strftime("%d_%b_%y", time.localtime())


def check_db_exists():
    try:
        name, current, history = database.load_hist()
        print(f"___ Welcome back {name}! ___")
        return name, current, history
    except KeyError:
        name, current, history = database.create_db()
        print("Created a new Database")
        return name, current, history


def check_date_in_db(history, current, op, x):
    how = input("?: ")

    if DATE not in history:
        history[DATE] = {str(how): [current, f"{op}{x}"]}
    else:
        history[DATE].update({str(how): [current, f"{op}{x}"]})


def main():
    name, current, history = check_db_exists()

    while True:
        database.show_rich()
        database.show_pretty()

        x = input("₹: ")

        if x == "":
            print("Please,type +5")

        elif x == "q" or x == "quit":
            quit()
        elif x == "clear" or x == "clr":
            database.clear_balance()

        elif x == "help":
            database.help()

        elif x.isdigit():
            current += int(x)
            check_date_in_db(history, current, "+", x)

        elif x[0] == "+":
            money = x.split("+")
            if money[1].isdigit():
                current += int(money[1])
                check_date_in_db(history, current, "+", money[1])
            else:
                print("INVALID!")

        elif x[0] == "-":
            money = x.split("-")
            if money[1].isdigit():
                current -= int(money[1])
                check_date_in_db(history, current, "-", money[1])
            else:
                print("INVALID!")
        else:
            print("INVALID!")

        database.save(current, history)


main()
#####################  V.1.0.0  #################################
import os
import shelve
from rich.console import Console
from rich.table import Table
from prettytable import PrettyTable

FILE = "mnyDB/db"


def help():
    print("""
This is a Money-manager program.
This program will record your transactions in a table format.
table contains 4 columns:
    1.Date
    2.Transaction
    3.Balance after transaction
    4.Reason for transaction

User interaction:
    1.
    ₹: "Enter the transaction here"
       "floating numbers are not allowed"
        options:
            5  -->This input will add 5 to the balance
            +5 -->This input will also add 5 to the balance
            -5 -->This input will subtract 5 from the balance

        special options:
            q   or quit  --> quits from the program
            clr or clear --> clear all history and exit the program
            help         --> show help menu

    2.
    ?: "Enter why the transaction happened"

After you fill the required inputs correctly the program will update the table

NB: Make sure your project directory includes
    1.Files:
       main.py     --> python file
       database.py --> python file

    2.python modules:
       time
       shelve
       rich  -->for computers
       prettytable -->for phones

THANK YOU for using this program

    """)


def create_db():
    print("Please enter your name while we create a new database for you!")
    while True:
        name = input("Name : ")

        if name.isspace():
            print("Try again!")
        elif name == "":
            print("Try again!")
        else:
            name1 = name.capitalize()
            break

    with shelve.open(FILE) as db:
        db["name"] = name1
        db["current"] = 0
        db["history"] = {}

    help()
    return name1, 0, {}


def load_hist():
    if not os.path.exists("mnyDB"):
        os.mkdir("mnyDB")
    with shelve.open(FILE) as db:
        name = db["name"]
        current = db["current"]
        history = db["history"]
    return name, current, history


def clear_balance():
    with shelve.open(FILE) as db:
        db["current"] = 0
        db["history"] = {}
        exit()
    print("Balance : 0 \nHistory cleared")


def save(current, history):
    with shelve.open(FILE) as db:
        db["current"] = current
        db["history"] = history


def show_rich():
    name, current, history = load_hist()

    console = Console()
    table = Table(title=".\__[green]₹[/]_[green]₹[/]__/.",
                  title_style="bold red",
                  show_header=True,
                  )

    table.add_column("Date", style="dim", header_style="blue")
    table.add_column("Flow", header_style="green", justify="left")
    table.add_column("Bal", header_style="yellow", justify="center")
    table.add_column("Reason", header_style="red", justify="left")

    for date, transactions in history.items():
        table.add_row(f"[bold italic]{date}[/]")
        for reason, money in transactions.items():
            table.add_row("", money[1], str(money[0]), reason)
        table.add_section()

    console.print(table)


def show_pretty():
    name, current, history = load_hist()
    table = PrettyTable(["Date", "Flow", "Bal", "Reason"])
    table.align = 'l'
    table._max_width = {"Reason": 17}

    for date, transactions in history.items():
        table.add_row([date, '', '', ''])
        for reason, money in transactions.items():
            table.add_row(['', money[1], str(money[0]), reason])
        # table.add_row(['*', '*', '*', '*'], divider=True)

    print(table)


# __________________________________________________________________________
# #####################  V.2.0.0  #################################
# added people section
# addded export as .txt
# created this "unique masterpiece" on 281023_1036p
# __________________________________________________________________________
#
#         DATABASE MODEL
#        ===============
#
# db = {
#     "current": 0,  # current == balance
#     "history": {
#         "DATE" :{
#             "reason1": [current balance: int,  transaction: str],
#             "reason2": [current balance: int,  transaction: str]
#         },
#         "01_Jul_23": {
#             "reason11": [10, "+10"],
#             "reason12": [5, "-5"],
#             "reason13": [20, "+15"],
#         },
#         "02_Jul_23": {
#             "reason21": [10, "-10"],
#             "reason22": [13, "+3"],
#             "reason23": [20, "+17"],
#         },
#     },
#     "people": {
#         "saleem": ["+10", "reason1", "date1"],
#         "saleem1": ["-10", "reason2", "date2"]
#
#     }
# }



