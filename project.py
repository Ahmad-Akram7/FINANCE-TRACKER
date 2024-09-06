import sqlite3

DATABASE_FILE = 'finance_tracker.db'

import sqlite3

def create_database():
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()



def execute_query(query, params=()):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def fetch_query(query, params=()):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def add_transaction(transaction_type, amount, category):
    query = '''
        INSERT INTO transactions (type, amount, category)
        VALUES (?, ?, ?)
    '''
    execute_query(query, (transaction_type, amount, category))
    print(f"Transaction added: {transaction_type}, {amount}, {category}")

def get_report():
    query = '''
        SELECT type, SUM(amount) as total
        FROM transactions
        GROUP BY type
    '''
    results = fetch_query(query)
    income = sum(row[1] for row in results if row[0] == 'income')
    expenses = sum(row[1] for row in results if row[0] == 'expense')
    savings = sum(row[1] for row in results if row[0] == 'savings')

    net_savings = income - expenses

    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Total Savings: ${savings:.2f}")
    print(f"Net Savings: ${net_savings:.2f}")

def main():
    while True:
        print("\nFinance Tracker Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Add Savings")
        print("4. Get Report")
        print("5. Exit")

        choice = input("What would you like to do? Enter the number of your choice: ")

        if choice == '1':
            amount = float(input("Enter the amount of income: "))
            category = input("Enter the category of income (e.g., salary, freelance): ")
            add_transaction('income', amount, category)

        elif choice == '2':
            amount = float(input("Enter the amount of expense: "))
            category = input("Enter the category of expense (e.g., food, rent): ")
            add_transaction('expense', amount, category)

        elif choice == '3':
            amount = float(input("Enter the amount of savings: "))
            category = input("Enter the category of savings (e.g., emergency fund, investment): ")
            add_transaction('savings', amount, category)

        elif choice == '4':
            get_report()

        elif choice == '5':
            print("Exiting the Finance Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
