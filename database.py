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

THANK YOU for using this program      
            
    """)
    input("press any key to continue...")


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
        db["people"] = {}

    help()
    return name1, 0, {}, {}


def load_hist():
    if not os.path.exists("mnyDB"):
        os.mkdir("mnyDB")
    with shelve.open(FILE) as db:
        name = db["name"]
        current = db["current"]
        history = db["history"]
        people = db["people"]
    return name, current, history, people


def undo():
    name, current, history, people = load_hist()
    p = history

    def undoo():
        # q = last transaction date
        q = list(p.keys())[len(p.keys()) - 1]
        # r = last date-> last transaction.reason
        r = list(p[q].keys())[len(p[q].keys()) - 1]
        # s = last transaction => [200,"+20"]
        s = p[q][r]
        # changing current's value
        current = s[0] - int(s[1])
        # removing last transaction
        p[q].popitem()
        return current

    try:
        current = undoo()
    except IndexError:
        p.popitem()
        current = undoo()

    return current, history


def clear_balance():
    with shelve.open(FILE) as db:
        db["current"] = 0
        db["history"] = {}
        exit()
    print("Balance : 0 \nHistory cleared")


def save(current, history, people):
    with shelve.open(FILE) as db:
        db["current"] = current
        db["history"] = history
        db["people"] = people


def show_rich():
    name, current, history, people = load_hist()

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
    name, current, history, people = load_hist()
    print(".\__₹_₹__/.".center(41))
    table = PrettyTable(["Date", "Flow", "Bal", "Reason"])
    table.max_table_width = 40
    table.align = 'l'
    table._max_width = {"Date": 6,
                        "Flow": 4,
                        "Bal": 4,
                        "Reason": 14
                        }

    for date, transactions in history.items():
        table.add_row([date, '____', '____', '______________'])
        for reason, money in transactions.items():
            table.add_row(['', money[1], str(money[0]), reason])

    print(table)


def show_people(people):
    table_people = PrettyTable(["Date", "Name", "₹", "?", ])
    table_people.max_table_width = 40
    table_people.align = "l"
    table_people._max_width = {"Date": 6,
                               "Name": 6,
                               "₹": 4,
                               "?": 12
                               }

    for name, transaction in people.items():
        table_people.add_row([transaction[2],
                              name,
                              transaction[0],
                              transaction[1],

                              ])
    print(table_people)


def export_history():
    # Loading contents from db
    name, current, history, people = load_hist()

    # appending the "transaction" history too
    table = PrettyTable(["Date", "Flow", "Bal", "Reason"])
    table.align = 'l'
    table._max_width = {"Reason": 17}

    for date, transactions in history.items():
        table.add_row([date, '', '', ''])
        for reason, money in transactions.items():
            table.add_row(['', money[1], str(money[0]), reason])
            with open(rf"{os.path.abspath('Money_history.txt')}",
                      'w',
                      encoding="utf8") as fp:
                fp.write(str(table))

    # appending the "owe" history too

    table_people = PrettyTable(["Name", "$", "?", "Date"])
    table_people.align = "l"

    for name, transaction in people.items():
        table_people.add_row([name, transaction[0], transaction[1], transaction[2], ])
        with open(rf"{os.path.abspath('Owe_history.txt')}",
                  'w',
                  encoding="utf8") as fp:
            fp.write(str(table_people))
