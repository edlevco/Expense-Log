import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

# Create a table using Python
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    description TEXT,
    amount REAL
)
''')

# Insert a new transaction
cursor.execute("INSERT INTO transactions (date, category, description, amount) VALUES (?, ?, ?, ?)", 
               ("2024-03-14", "Salary", "Paycheck", 2500.00))

# Save (commit) changes and close
conn.commit()
conn.close()

print("✅ Transaction added to database!")


