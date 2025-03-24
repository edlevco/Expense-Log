import sqlite3


# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

def get_connection():
    return sqlite3.connect("finance.db")


def create_category_table():
    expenses = ["Dining Out", 
                "Groceries", 
                "Entertainment", 
                "Rent", 
                "Clothes", 
                "Travel",
                "Transportation",
                "Health / Hygiene",
                "Pay For"]
    
    incomes = ["Work",
              "Pay Back",
              "Gift"]
    
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS CATEGORIES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            name TEXT)
            ''')
    
    for expense in expenses:
        pass # add to table


    for income in incomes:
        pass ## add to table
        


def create_table(name):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create a table using Python
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            balance REAL
        )
        ''')

def add_data(table_name, date, category, amount, balance):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(f'''
        INSERT INTO {table_name} (
            date,
            category,
            amount,
            balance
        ) VALUES (
            {date},
            {category},
            {amount},
            {balance}
        )
        ''')

def get_tables_with_balance_column():
    tables_with_balance = []
    
    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        
        # Step 1: Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")


        print(cursor.fetchall())
        print()


        tables = [row[0] for row in cursor.fetchall()]
        print(tables)
        
        # Step 2: Check each table's columns
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [col[1] for col in cursor.fetchall()]  # col[1] is the column name
            
            if "balance" in columns:
                tables_with_balance.append(table)
    
    return tables_with_balance



