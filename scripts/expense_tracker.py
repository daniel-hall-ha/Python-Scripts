#!/usr/bin/env python3
import os, uuid, re, sys
import string, secrets
from cryptography.fernet import Fernet
from prettytable import PrettyTable
import sqlite3, getpass

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "expense_tracker", "database.db")

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

def display_credentials(username, uid, secret_key):

    table = PrettyTable(header=False)

    table.field_names = ["Field 1", "Field 2"]
    table.header = False
    table.add_row(["Username",username], divider=True)
    table.add_row(["Uid", uid], divider=True)
    table.add_row(["Secret Key", secret_key])
    table.align = "l"

    print(table)

def user_registration():

    os.system('clear')

    print("REGISTRATION\n")
    print("============\n")
    
    username = get_new_username()
    uid = ''.join(list(username[x].lower() for x in range(len(username)-1,-1,-1) if str.isalpha(username[x])))+"-"+str(uuid.uuid4())
    secret_key = generate_secret_key()
    
    os.system('clear')

    print("REGISTRATION SUCCESSFUL!\n")
    print("========================\n")
    print("Here are your username and secret keys to login.")
    print("Make sure you won't lose them as this is one-time access to view.\n")

    display_credentials(username, uid, secret_key)

    store_credentials(username, uid, secret_key)

def store_credentials(username, uid, secret_key):

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
                    secret_key TEXT NOT NULL
                    )
        """)
        
    else:

        with sqlite3.connect(file_path) as connection:
            cur = connection.cursor()
            query = "INSERT INTO users (username, uid, secret_key) VALUES (?, ?, ?)"
            cur.execute(query, (username, uid, secret_key))
            connection.commit()

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

def login():

    os.system('clear')
    print("LOGIN\n")
    print("=====\n")

    username = input("Enter username: ")
    uid = input("Enter uid: ")

    if not check_username_uid(username, uid):

        os.system('clear')
        print("OOPS!\n")
        print("=====\n")
        print("User not found!")

        return "Unauthorized"
        
    else:

        os.system('clear')
        print("Welcome " + username + "!\n")
        print("="*(len(username)+9) + "\n")

        secret_key = getpass.getpass("Verify with provided secret key: ")
        if check_secret_key(secret_key, uid):
            return "Success"
        else:
            return "Wrong Passkey"


def main():

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

if __name__ == "__main__":
    main()