# ======================V2.1.0=============================
# db = {
#     "current": 0,
#     "history": {"date 1": {"reason": ["balance", "(+)money"]},
#                 "date 2": {"reason": ["balance", "(-)money"]}
#                 },
#     "hist_owe": {"person":money}, # here money not string bcz we do calculations on it
#                                   # 0 means no owe,+ means took, - -->gave
# }


import shelve
import time

NAME = "Sälèém   "
FILE = "moneyDB"
DATE = time.strftime("%d_%b_%y", time.localtime())


def clear_balance():
    with shelve.open(FILE) as db:
        db["current"] = 0
        db["history"] = {}
        exit()
    print("Balance : 0 \nHistory cleared")


def clear_take():
    with shelve.open(FILE) as db:
        db["hist_take"] = {}
    print("Took History cleared")


def clear_give():
    with shelve.open(FILE) as db:
        db["hist_give"] = {}
    print("Gave History cleared")


def owe():
    with shelve.open(FILE) as db:
        print("GIVE MONEY:")
        if db["hist_take"]:
            for person, money in db["hist_take"].items():
                print(f"\t{person} : {money}")
        else:
            print("\tYou don't owe money to anyone")
        print("TAKE MONEY:")
        if db["hist_give"]:
            for person, money in db["hist_give"].items():
                print(f"\t{person} : {money}")
        else:
            print("\tNo one owe's you money")


def print_history():
    with shelve.open(FILE) as db:
        for date, transactions in db["history"].items():
            print("_" * 41)
            print(f"{date:_^41}")
            biggest = len(str(max(transactions.values(), key=len)))
            for reason, money in transactions.items():
                space = (biggest - len(money)) * " "
                if len(money) < biggest:
                    print(f"   {money}{space} : {reason}")
                else:
                    print(f"   {money} : {reason}")


def show():
    print("OPTIONS".center(41, '_'))
    print("SHOW:\n  1.History   2.Owe\nCLEAR:\n  3.balance   4.I gave   5.will take")
    print("_" * 41)
    while True:
        ask = input(" :")
        if ask.isdigit():
            ask = int(ask)
            if 1 <= ask <= 5:
                break
    if ask == 1:
        print_history()
    elif ask == 2:
        owe()
    elif ask == 3:
        clear_balance()
    elif ask == 4:
        clear_give()
    elif ask == 5:
        clear_take()
    else:
        print(":)")


def load_hist():
    with shelve.open(FILE) as db:
        current = db["current"]
        history = db["history"]
        hist_take = db["hist_take"]
        hist_give = db["hist_give"]

    return current, history, hist_take, hist_give


def main():
    current, history, hist_take, hist_give = load_hist()

    print(".\__₹_₹__/.".center(41))
    print("-" * 41)
    print(f"{NAME}{current:^{41 - len(NAME) - len(DATE)}}{DATE}")
    print("-" * 41 + "\n")
    # print("_" * 41+"\n"+"_" * 41+"\n")

    while True:
        x = input("₹: ")
        opt = ["+", "-", "g", "t"]

        if x == "q" or x == "Q":
            print("./__x_x__\.".center(41))
            break

        elif x == "s" or x == "S":
            show()
            print("_" * 41)
            print()

        elif x.isdigit():
            how = input("?: ")
            current += int(x)
            if DATE not in history:
                history[DATE] = {str(how): f"+{x}"}
            else:
                history[DATE].update({str(how): f"+{x}"})

        elif x[0] in opt:
            how = input("?: ")
            for i in opt:
                if i == x[0]:
                    money = x.split(i)
                    if money[1].isdigit():
                        if i == "+":
                            current += int(x)
                            if DATE not in history:
                                history[DATE] = {str(how): f"+{money[1]}"}
                            else:
                                history[DATE].update({str(how): f"+{money[1]}"})
                        elif i == "-":
                            current -= int(money[1])
                            if DATE not in history:
                                history[DATE] = {str(how): f"-{money[1]}"}
                            else:
                                history[DATE].update({str(how): f"-{money[1]}"})
                        elif i == "g":
                            current -= int(money[1])
                            hist_give[str(how)] = money[1]
                        elif i == "t":
                            current += int(money[1])
                            hist_take[str(how)] = money[1]
                    else:
                        print("Invalid command!,Master!.")
        else:
            print("Invalid command!,Master!.")
        with shelve.open(FILE) as db:
            db["current"] = current
            db["history"] = history
            db["hist_take"] = hist_take
            db["hist_give"] = hist_give
        # if x != 's':
        #     os.system("clear")
        print(f"{current:_^{41 + len(NAME) - len(DATE)}}" + "_" * 3 + "\n")


main()
