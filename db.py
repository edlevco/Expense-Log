import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect("finance.db")


def create_category_table():
    expenses = ["Add New", "Unknown", "Dining Out", "Groceries", "Entertainment", "Rent", 
                "Clothes", "Travel", "Transportation", "Health / Hygiene", "Pay For"]
    
    incomes = ["Add New", "Unknown", "Work", "Pay Back", "Gift"]
    
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS CATEGORIES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            name TEXT
        )
        ''')

        cursor.execute('''SELECT * FROM CATEGORIES''')
        data = cursor.fetchall()
        if len(data) < 1:
            for expense in expenses:
                add_category("expense", expense)

            for income in incomes:
                add_category("income", income)
        

def create_table(name):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            type TEXT,
            amount REAL,
            balance REAL
        )
        ''')


def add_data(table_name, date, category, type, amount, balance):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(f'''
        INSERT INTO {table_name} (date, category, type, amount, balance)
        VALUES (?, ?, ?, ?, ?)
        ''', (date, category, type, amount, balance))


def add_category(type, category):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO CATEGORIES (type, name)
        VALUES (?, ?)
        ''', (type, category))


def get_account_tables():
    tables_with_balance = []

    with sqlite3.connect("finance.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [col[1] for col in cursor.fetchall()]
            if "balance" in columns:
                tables_with_balance.append(table)

    return tables_with_balance

def get_categories_list(type):
    
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM CATEGORIES''')
        categories = cursor.fetchall()
              
        categories = [category[2] for category in categories if category[1] == type]
    
    return categories

def return_data(table_name):

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(f'''SELECT * FROM {table_name}''')
        categories = cursor.fetchall()

        return categories
    
def get_balance(table_name):
    categories = return_data(table_name)

    return categories[-1][5]

def get_total_transactions(table_name, start, end):
    categories = return_data(table_name)

    expense = 0
    income = 0
    # start_date = datetime.strptime(start, "%m/%d/%Y")
    # end_date = datetime.strptime(end, "%m/%d/%Y")

    for category in categories:
        transaction_date = datetime.strptime(category[1], "%m/%d/%Y")
        if start <= transaction_date <= end:
            if category[3] == "expense":
                expense += category[4]
            else:
                income += category[4]
    
    return (expense, income)






    







