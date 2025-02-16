# import os
import time
import database

# add people table  done!.
# add export table as text file  done!.
# check reason exist problem done!.

DATE = time.strftime("%d_%b_%y", time.localtime())


def check_db_exists():
    try:
        name, current, history, people = database.load_hist()
        print(f"___ Welcome back {name}! ___")
        return name, current, history, people
    except KeyError:
        name, current, history, people = database.create_db()
        print("Created a new Database")
        return name, current, history, people


def check_reason_exist(how, history):
    if how in list(history[DATE].keys()):
        i = 1
        while True:
            new_how = f"{how}({i})"
            if new_how not in history[DATE].keys():
                return new_how
            else:
                i += 1
    return how


def check_date_in_db(history, current, op, x):
    while True:
        how = input("?: ")
        if how != "" and not how.isspace():
            break

    if DATE not in history:
        history[DATE] = {str(how): [current, f"{op}{x}"]}
    else:
        new_how_1 = check_reason_exist(how, history)
        history[DATE].update({str(new_how_1): [current, f"{op}{x}"]})

    return how
    # we need how in give and take section


def check_name_in_db(people, op, x, how):
    while True:
        name = input("name:")
        if name != "" and not name.isspace():
            break

    if name not in people.keys():
        people[name] = [f"{op}{x}", str(how), DATE]
    else:
        owe = eval(f"{people[name][0]}{op}{x}")
        if owe == 0:
            people.pop(name)
        else:
            people[name] = [str(owe), str(how), DATE]


def main():
    name, current, history, people = check_db_exists()

    while True:
        # database.show_rich()
        database.show_pretty()

        x = input("₹: ")

        if x == "":
            print("Please,type '+5'")

        elif x == "q" or x == "quit":
            quit()
        elif x == "clear" or x == "clr":
            database.clear_balance()

        elif x == "u":
            current, history = database.undo()
        elif x == "help":
            database.help()
        elif x == "people":
            database.show_people(people)
            while True:
                x = input("Hit enter to continue! :")
                if x != "`":
                    break
        elif x == "export":
            database.export_history()

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

        elif x[0] == "g":
            money = x.split("g")
            if money[1].isdigit():
                current -= int(money[1])
                how = check_date_in_db(history, current, "-", money[1])
                check_name_in_db(people, "-", money[1], how)
            else:
                print("INVALID!")

        elif x[0] == "t":
            money = x.split("t")
            if money[1].isdigit():
                current += int(money[1])
                how = check_date_in_db(history, current, "+", money[1])
                check_name_in_db(people, "+", money[1], how)
            else:
                print("INVALID!")
        else:
            print("INVALID!")

        database.save(current, history, people)
        # os.system("clear")


main()
