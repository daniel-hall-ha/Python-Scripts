#!/usr/bin/env python3
import os, uuid, re, sys
import string, secrets
import datetime
from datetime import datetime
from prettytable import PrettyTable
import sqlite3, getpass
from decimal import Decimal, ROUND_HALF_UP

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "expense_tracker", "database.db")

def user_registration():

    os.system('clear')

    print("REGISTRATION\n")
    print("============\n")
    
    username = get_new_username()
    uid = str(uuid.uuid4())
    secret_key = generate_secret_key()
    table_id = generate_expense_table_id()
    
    os.system('clear')

    print("REGISTRATION SUCCESSFUL!\n")
    print("========================\n")
    print("Here are your username and secret keys to login.")
    print("Make sure you won't lose them as this is one-time access to view.\n")

    display_credentials(username, uid, secret_key)

    store_credentials(username, uid, secret_key, table_id)

    create_personal_expense_table(table_id)

def get_new_username():

    username = input("Enter your name (only English letters with -, _, space are allowed): ")

    while (re.match(r"[^a-zA-Z\-_]", username)):
        username = input("Invalid username. Enter again: ")
    while (len(username) < 8):
        username = input("Username must be at least 8 characters. Enter again: ")

    return username

def generate_secret_key():

    alphabets = string.ascii_letters + string.digits + "!@#$%^&*_+"
    secret_key = ''.join(secrets.choice(alphabets) for _ in range(128))
    
    return secret_key

def generate_expense_table_id():

    alphabets = string.ascii_lowercase + string.digits
    table_id = ''.join(secrets.choice(alphabets) for _ in range(25))

    return table_id

def display_credentials(username, uid, secret_key):

    table = PrettyTable(header=False)

    table.field_names = ["Field 1", "Field 2"]
    table.header = False
    table.add_row(["Username",username], divider=True)
    table.add_row(["Uid", uid], divider=True)
    table.add_row(["Secret Key", secret_key])
    table.align = "l"

    print(table)

def store_credentials(username, uid, secret_key, table_id):

    with sqlite3.connect(file_path) as connection:
        cur = connection.cursor()
        query = "INSERT INTO users (username, uid, secret_key, table_id) VALUES (?, ?, ?, ?)"
        cur.execute(query, (username, uid, secret_key, table_id))
        connection.commit()

def create_personal_expense_table(table_id):

    connection = sqlite3.connect(file_path)
    cur = connection.cursor()
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_id} (
        id TEXT PRIMARY KEY NOT NULL,
        date TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price DOUBLE NOT NULL,
        quantity INTEGER NOT NULL,
        total_cost DOUBLE NOT NULL,
        remarks TEXT
    )
    """)

def login():

    os.system('clear')
    print("LOGIN\n")
    print("=====\n")

    username = input("Enter username: ")
    uid = input("Enter uid: ")

    if not check_username_uid(username, uid):
        return "Unauthorized"
    else:

        os.system('clear')
        print("Welcome " + username + "!\n")
        print("="*(len(username)+9) + "\n")

        secret_key = getpass.getpass("Verify with provided secret key: ")
        if check_secret_key(secret_key, uid):

            with sqlite3.connect(file_path) as connection:
                cur = connection.cursor()
                query = "SELECT table_id FROM users WHERE username=? AND uid=?"
                cur.execute(query, (username,uid))

            table_id = cur.fetchone()

            return "Success", username, uid, table_id[0]
        else:
            return "Wrong Passkey"
        
def check_username_uid(username, uid):

    with sqlite3.connect(file_path) as connection:
        cur = connection.cursor()
        query = "SELECT username, uid FROM users WHERE username=? AND uid=?"
        cur.execute(query, (username, uid))
        
        return False if cur.fetchone() is None else True

def check_secret_key(secret_key, uid):
        
    with sqlite3.connect(file_path) as connection:
        cur = connection.cursor()
        query = "SELECT secret_key FROM users WHERE uid=? AND secret_key=?"
        cur.execute(query, (uid, secret_key))
        
        return False if cur.fetchone() is None else True

def onboarding(username):

    print(
    f"""WELCOME {username.upper()}!\n
    {"="*(9+len(username.upper()))}\n
    Welcome to your personal expense database.
    Choose one: 
    1. Add expense.
    2. View expense.
    Otherwise, print q to exit.
    """)

    option = input("Your option: ")
    while not option in ["1", "2", "q"]:
        option = input("Your option: ")

    if option == "1":
        return "add"
    elif option == "2":
        return "view"
    else:
        return "quit"

def add_expense_record(username, table_id):
    
    date = get_date()
    id = generate_record_id(username, date)
    title = get_title()
    description = get_description()
    price = get_price()
    quantity = get_quantity()
    total_cost = get_total_cost(price, quantity)
    remarks = get_remarks()

    with sqlite3.connect(file_path) as connection:
        cur = connection.cursor()
        query = f"""INSERT INTO {table_id} (id, date, title, description, price, quantity, total_cost, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cur.execute(query, (id, date, title, description, price, quantity, total_cost, remarks))

def generate_record_id(username, date):

    characters = string.ascii_lowercase + string.digits
    id_suffix = ''.join(secrets.choice(characters) for _ in range(5))

    return username.replace(" ","").lower() + date.replace("-","") + id_suffix

def get_date():

    while True:
        try:
            user_input = input("Date (YYYY-MM-DD): ")
            d = datetime.strptime(user_input, "%Y-%m-%d").date()
            return str(d)
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")

def get_title():

    title = input("Title: ")
    while len(title)<6 or len(title)>25 or re.match(r"[^A-Za-z0-9 ]", title):
        print("Title must be only letters and numbers with min 6 chars and max 24 chars.")
        title = input("Title: ")

    return title

def get_description():

    char_count = 0
    lines = []
    print("Description (Press Enter to save): ")
    while True:
        line = input("")
        if line == "":
            break
        else:
            lines.append(line)

    if sum(len(line) for line in lines) > 1001:
        print("Description must not exceed 1000 characters. Shorten your input and re-enter.")
        get_description()

    return "\n".join(lines)

def get_price():
    
    price = input("Price: $ ")
    while re.match(r"[^0-9.]", price):
        price = input("Invalid Input. Enter again. Price: $")

    return float(price) 

def get_quantity():

    quantity = input("Quantity: ")
    while re.match(r"[^0-9]", quantity):
        quantity = input("Invalid Input. Enter again. Price: $")
    
    return int(quantity)

def get_total_cost(price, quanitity):
     
    price = Decimal(str(price))
    quanitity = Decimal(str(quanitity))
    total = (price*quanitity).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

    print("Total: $ " + str(total))
    return float(total)

def get_remarks():

    remarks = input("Remarks: ")
    while len(remarks)>50:
        print("Remarks must be only letters and numbers with maximum 50 characters.")
        remarks = input("Remarks: ")

def check_source_file():
    
    if not os.path.exists(file_path):
        with open(file_path, "x") as file:
            pass
        file.close()

    connection = sqlite3.connect(file_path)
    cur = connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                uid TEXT NOT NULL,
                secret_key TEXT NOT NULL,
                table_id TEXT NOT NULL
                )
    """)

def display_records(From, To, table_id):
    
    # Extract

    with sqlite3.connect(file_path) as connection:
        cur = connection.cursor()
        query = f"""SELECT date, title, description, price, quantity, total_cost, remarks FROM {table_id} WHERE DATE(date) >= DATE(?) AND DATE(date) <= DATE(?)"""
        cur.execute(query, (From, To))

        expense_list = cur.fetchall()
    
        # Display

    table = PrettyTable()
    table.align = "l"
    table.field_names = ["Date", "Title", "Description", "Price", "Quantity", "Total Cost", "Remarks"]
    table.max_width["Description"] = 40
    table.max_width["Title"] = 25
    for expense in expense_list:
        table.add_row(expense)
    print(table)
    
def main():

    # Check source database
    check_source_file()

    # Login Flow
    while True:

        login_status = login()

        if login_status == "Unauthorized":

            os.system('clear')
            print("OOPS\n")
            print("======\n")
            print("User not found!\n")
            
        elif login_status == "Wrong Passkey":

            os.system('clear')
            print("OOPS\n")
            print("======\n")
            print("Incorrect Secret Key!\n")

        else:

            username, uid, table_id = login_status[1], login_status[2], login_status[3]
            
            break

        print("You may choose one of the following options to proceed.")
        print(" 1 - Go back to login.")
        print(" 2 - Register")
        print(" 3 - Exit\n")

        option = int(input("Your option: "))
        while not option in [1, 2, 3]:
            option = input("Your option: ")

        if option == 1:
            main()

        elif option == 2:
            user_registration()
            proceed = input("\nEnter p to proceed to login screen or q quit: ")
            while not proceed in ["q", "Q", "p", "P"]:
                proceed = input("Enter p to proceed to login screen or q quit: ")

            if proceed in ["q", "Q"]:
                os.system('clear')
                print("Goodbye!")
                sys.exit(0)
            else:
                main()

        elif option == 3:
            os.system('clear')
            print("Goodbye!")
            sys.exit(0)
    
    os.system('clear')

    while True:
        
        onboard = onboarding(username)
        os.system('clear')

        if onboard == "add":

            while True:

                add_expense_record(username, table_id)
                os.system('clear')

                is_continue = input("Would you like to add another one? y/n : ")
                while not is_continue in ["y", "n", "Y", "N"]:
                    is_continue = input("Would you like to add another one? y/n : ")

                if is_continue in ["Y", "y"]:
                    os.system('clear')
                    add_expense_record(username, table_id)
                else:
                    os.system('clear')
                    break
        
        elif onboard == "view":

            os.system('clear')

            print("VIEW EXPENSES")
            print("=============")

            From = input("From YYYY-MM-DD: ")
            To = input("To YYYY-MM-DD: ")

            display_records(From, To, table_id)

            menu = input("Enter q to quit.")
            while not menu == "q":
                menu = input("Enter q to quit.")
            print("Thank You")
            sys.exit(0)

        else:

            print("Thank You")
            sys.exit(0)

if __name__ == "__main__":
    main()