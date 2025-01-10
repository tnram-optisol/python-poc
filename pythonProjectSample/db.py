from datetime import datetime

import _sqlite3
import os
from pathlib import Path


from utils.helper_functions import generate_account_number, convert_rows_to_dict

create_account_table = '''
    CREATE TABLE IF NOT EXISTS USER_ACCOUNTS(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        country TEXT NOT NULL,
        account_number TEXT NOT NULL
    )
'''
create_transaction_table = '''
     CREATE TABLE IF NOT EXISTS USER_TRANSACTION(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_type TEXT NOT NULL,
        date DATE NOT NULL,
        amount INTEGER NOT NULL,
        account_number INTEGER,
        FOREIGN KEY (account_number) REFERENCES user_accounts(account_number)
    )
'''
directory = Path.home()
path_folder = 'sqlite3'
database = 'account_details'

if not directory.joinpath(path_folder).exists():
    db = directory.joinpath(path_folder + '/' + database)
else:
    db = directory.joinpath(path_folder + '/' + database)


class Database:
    def __init__(self):
        connection = _sqlite3.connect(db)
        connection.row_factory = _sqlite3.Row
        cursor = connection.cursor()
        self.cursor = cursor
        self.connection = connection
        self.create_tables()

    def create_tables(self):
        try:
            self.cursor.execute(create_account_table)
            self.connection.commit()
            self.cursor.execute(create_transaction_table)
            self.connection.commit()
        except Exception as e:
            print(e)

    def add_user_transaction(self, user_data):
        try:
            create_account_number = generate_account_number()
            add_user = '''
                        INSERT INTO USER_ACCOUNTS (name, phone_number, date_of_birth, country, account_number)
                        VALUES (?, ?, ?, ?, ?)
                    '''
            self.cursor.execute(add_user, (
                user_data['name'], user_data['phone_number'], user_data['date_of_birth'], user_data['country'],
                create_account_number['account_number']))

            self.connection.commit()

            get_user = '''
                        SELECT * FROM USER_ACCOUNTS WHERE account_number = ?
                    '''

            self.cursor.execute(get_user, (create_account_number['account_number'],))

            rows = self.cursor.fetchall()

            result = convert_rows_to_dict(rows)

            return result

        except Exception as e:
            print(e)

    def add_deposit(self, account_number, amount):
        try:
            get_user = '''
                        SELECT * FROM USER_ACCOUNTS WHERE ACCOUNT_NUMBER = ?
                    '''
            self.cursor.execute(get_user, (account_number,))
            user = self.cursor.fetchall()
            date = datetime.now().isoformat()
            if user:
                add_transaction = '''
                                      INSERT INTO USER_TRANSACTION (transaction_type, date, amount, account_number)
                                      VALUES (?, ?, ?, ?)
                                      '''
                self.cursor.execute(add_transaction,
                                    ('deposit', date, amount,
                                     account_number))
                self.connection.commit()
                return self.cursor.fetchall()
            else:
                raise Exception("user account not exists")

        except Exception as e:
           print(e)
