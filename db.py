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

def get_category_from_dict(expense_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT category FROM WORD_DICT
        WHERE expense_name = ?
        ''', (expense_name,))
        
        result = cursor.fetchone()
        if result:
            return result[0]  # category
        else:
            return None

def create_dict_table():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS WORD_DICT (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_name TEXT,
            category TEXT
            
                       )
''')
        
def add_dict_data(expense_name, category):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO WORD_DICT (expense_name, category)
        VALUES (?, ?)
''', (expense_name, category))




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
    ## "{:.2f}".format(amount)

    expense = float("{:.2f}".format(expense))
    income = float("{:.2f}".format(income))

    return (expense, income)

def get_top_5(dict):
    

    sorted_items = sorted(dict.items(), key = lambda x : x[1], reverse=True )[:5]

    categories = [key for key, value in sorted_items]
    amounts = [value for key, value in sorted_items]

    return (categories, amounts)

def get_total_dict(table_name, type):
    dict = {}

    expenses = get_categories_list(type)

    for expense in expenses:
        dict[expense] = 0
    
    categories = return_data(table_name)

    for category in categories:
        if category[3] == type:
            dict[category[2]] += category[4]


    return dict


def get_plot_data(table_name):
    dates = []
    balances = []
    categories = return_data(table_name)

    new_date = categories[-1][1]

    dates.append(categories[-1][1])
    balances.append(categories[-1][5])

    
    for i in range(len(categories)):
        index = len(categories)-i-1
        date = categories[index][1]
        balance = categories[index][5]

        if not date == new_date:
            dates.append(date)
            balances.append(balance)
            new_date = date


    dates.reverse()
    balances.reverse()

    return dates, balances



    
    

    


    

    

    






    







