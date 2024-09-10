import streamlit as st
from db import create_connection
from bank_operations import register_user, login_user, deposit, withdraw, view_balance, view_transactions, get_account_summary, delete_account

def main():
    connection = create_connection()
    
    st.title("Bank Management System")

    menu = ["Register", "Login", "Deposit", "Withdraw", "Balance Inquiry", "Transaction History", "Account Summary", "Change Password", "Delete Account"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.subheader("Register New Account")
        name = st.text_input("Account Holder Name")
        password = st.text_input("Password", type='password')
        currency = st.selectbox("Currency", ["USD", "EUR", "INR"])
        if st.button("Register"):
            register_user(connection, name, password, currency)
            st.success(f"Account for {name} registered successfully!")

    elif choice == "Login":
        st.subheader("Login to Your Account")
        account_id = st.number_input("Account ID", min_value=1)
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if login_user(connection, account_id, password):
                st.success("Login successful!")
            else:
                st.error("Incorrect account ID or password.")

    elif choice == "Deposit":
        st.subheader("Deposit")
        account_id = st.number_input("Account ID", min_value=1)
        amount = st.number_input("Amount", min_value=0.01)
        if st.button("Deposit"):
            deposit(connection, account_id, amount)
            st.success("Deposit successful!")

    elif choice == "Withdraw":
        st.subheader("Withdraw")
        account_id = st.number_input("Account ID", min_value=1)
        amount = st.number_input("Amount", min_value=0.01)
        if st.button("Withdraw"):
            success = withdraw(connection, account_id, amount)
            if success:
                st.success("Withdrawal successful!")
            else:
                st.error("Insufficient balance!")

    elif choice == "Balance Inquiry":
        st.subheader("Balance Inquiry")
        account_id = st.number_input("Account ID", min_value=1)
        if st.button("Check Balance"):
            balance = view_balance(connection, account_id)
            st.info(f"Current Balance: ${balance}")

    elif choice == "Transaction History":
        st.subheader("Transaction History")
        account_id = st.number_input("Account ID", min_value=1)
        if st.button("View Transactions"):
            transactions = view_transactions(connection, account_id)
            for trans in transactions:
                st.write(f"{trans[0]} of ${trans[1]} on {trans[2]}")

    elif choice == "Account Summary":
        st.subheader("Account Summary")
        account_id = st.number_input("Account ID", min_value=1)
        if st.button("Get Summary"):
            summary = get_account_summary(connection, account_id)
            if summary:
                st.write(f"**Account Holder Name**: {summary['account_holder_name']}")
                st.write(f"**Current Balance**: ${summary['account_balance']}")
                st.write(f"**Total Deposits**: ${summary['total_deposits']}")
                st.write(f"**Total Withdrawals**: ${summary['total_withdrawals']}")
                st.write(f"**Number of Transactions**: {summary['transaction_count']}")
            else:
                st.error("Account not found!")

    elif choice == "Change Password":
        st.subheader("Change Password")
        account_id = st.number_input("Account ID", min_value=1)
        old_password = st.text_input("Old Password", type='password')
        new_password = st.text_input("New Password", type='password')
        if st.button("Change Password"):
            if login_user(connection, account_id, old_password):
                cursor = connection.cursor()
                cursor.execute("UPDATE accounts SET password = %s WHERE account_id = %s", (new_password, account_id))
                connection.commit()
                st.success("Password changed successfully!")
            else:
                st.error("Old password is incorrect.")

    elif choice == "Delete Account":
        st.subheader("Delete Account")
        account_id = st.number_input("Account ID", min_value=1)
        if st.button("Delete Account"):
            delete_account(connection, account_id)
            st.success("Account and transaction history deleted successfully!")

    connection.close()

if __name__ == '__main__':
    main()

