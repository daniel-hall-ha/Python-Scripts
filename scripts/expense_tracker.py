#!/usr/bin/env python3
import os, uuid, re
import string, secrets
from cryptography.fernet import Fernet
from prettytable import PrettyTable
import sqlite3

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

def user_register():

    os.system('clear')

    print("Registeration")
    print("=============")
    
    username = get_new_username()
    uid = ''.join(list(username[x].lower() for x in range(len(username)-1,-1,-1) if str.isalpha(username[x])))+"-"+str(uuid.uuid4())
    secret_key = generate_secret_key()
    
    os.system('clear')

    print("You are successfully registered!")
    print("================================")
    print("Here are your username and secret keys to login.")
    print("Make sure you won't lose them as this is one-time access to view.")

    display_credentials(username, uid, secret_key)

    store_credentials(username, uid, secret_key)

    return username, uid, secret_key

def store_credentials(username, uid, secret_key):

    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "expense_tracker", "database.db")

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

        connection = sqlite3.connect(file_path)
        cur = connection.cursor()
        query = "INSERT INTO users (username, uid, secret_key) VALUES (?, ?, ?)"
        cur.execute(query, (username, uid, secret_key))
        connection.commit()

def main():
    user_register()

if __name__ == "__main__":
    main()