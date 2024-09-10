def register_user(connection, name, password, currency='USD'):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO accounts (account_holder_name, password, currency) VALUES (%s, %s, %s)", (name, password, currency))
    connection.commit()

def login_user(connection, account_id, password):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM accounts WHERE account_id = %s AND password = %s", (account_id, password))
    return cursor.fetchone() is not None

def deposit(connection, account_id, amount):
    cursor = connection.cursor()
    cursor.execute("UPDATE accounts SET account_balance = account_balance + %s WHERE account_id = %s", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, transaction_type, transaction_amount) VALUES (%s, 'Deposit', %s)", (account_id, amount))
    connection.commit()

def withdraw(connection, account_id, amount):
    cursor = connection.cursor()
    cursor.execute("SELECT account_balance FROM accounts WHERE account_id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute("UPDATE accounts SET account_balance = account_balance - %s WHERE account_id = %s", (amount, account_id))
        cursor.execute("INSERT INTO transactions (account_id, transaction_type, transaction_amount) VALUES (%s, 'Withdrawal', %s)", (account_id, amount))
        connection.commit()
        return True
    else:
        return False

def view_balance(connection, account_id):
    cursor = connection.cursor()
    cursor.execute("SELECT account_balance FROM accounts WHERE account_id = %s", (account_id,))
    return cursor.fetchone()[0]

def view_transactions(connection, account_id):
    cursor = connection.cursor()
    cursor.execute("SELECT transaction_type, transaction_amount, transaction_date FROM transactions WHERE account_id = %s", (account_id,))
    return cursor.fetchall()

def delete_account(connection, account_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transactions WHERE account_id = %s", (account_id,))
    cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
    connection.commit()

def get_account_summary(connection, account_id):
    cursor = connection.cursor()
    
    # Fetch account holder name and balance
    cursor.execute("SELECT account_holder_name, account_balance FROM accounts WHERE account_id = %s", (account_id,))
    account_info = cursor.fetchone()
    
    if not account_info:
        return None
    
    # Fetch total deposits and withdrawals
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN transaction_type = 'Deposit' THEN transaction_amount ELSE 0 END) AS total_deposits,
            SUM(CASE WHEN transaction_type = 'Withdrawal' THEN transaction_amount ELSE 0 END) AS total_withdrawals,
            COUNT(*) AS transaction_count
        FROM transactions WHERE account_id = %s
    """, (account_id,))
    
    transaction_summary = cursor.fetchone()

    return {
        "account_holder_name": account_info[0],
        "account_balance": account_info[1],
        "total_deposits": transaction_summary[0] or 0.0,
        "total_withdrawals": transaction_summary[1] or 0.0,
        "transaction_count": transaction_summary[2]
    }
