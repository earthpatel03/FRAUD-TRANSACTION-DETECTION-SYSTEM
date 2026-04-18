import mysql.connector
from datetime import datetime

# 🔗 DB CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",  
    database="fraud_db"
)

cursor = conn.cursor()

# ================= FUNCTIONS ================= #

# 1. Add Transaction
def add_transaction():
    try:
        user_id = int(input("Enter User ID: "))
        amount = float(input("Enter Amount: "))
        location = input("Enter Location: ")

        txn_time = datetime.now()

        cursor.execute("""
            INSERT INTO transactions (user_id, amount, location, txn_time)
            VALUES (%s, %s, %s, %s)
        """, (user_id, amount, location, txn_time))

        conn.commit()
        txn_id = cursor.lastrowid

        # 🚨 Rule: High Amount
        if amount > 50000:
            cursor.execute("UPDATE transactions SET is_fraud=1 WHERE txn_id=%s", (txn_id,))
            conn.commit()
            print("🚨 High amount fraud detected!")

        print("✅ Transaction Added")

    except Exception as e:
        print("❌ Error:", e)


# 2. Show Report
def show_report():
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE is_fraud=1")
    fraud = cursor.fetchone()[0]

    print("\n📊 REPORT")
    print("Total Transactions:", total)
    print("Fraud Transactions:", fraud)


# 3. View All Transactions
def view_transactions():
    cursor.execute("SELECT * FROM transactions")
    for row in cursor.fetchall():
        print(row)


# 4. View Fraud Transactions
def view_fraud():
    cursor.execute("SELECT * FROM transactions WHERE is_fraud=1")
    for row in cursor.fetchall():
        print(row)


# 5. User Transaction History
def user_history():
    uid = int(input("Enter User ID: "))
    cursor.execute("SELECT * FROM transactions WHERE user_id=%s", (uid,))
    for row in cursor.fetchall():
        print(row)


# 6. Top Fraud Users
def top_fraud_users():
    cursor.execute("""
        SELECT user_id, COUNT(*) as fraud_count
        FROM transactions
        WHERE is_fraud=1
        GROUP BY user_id
        ORDER BY fraud_count DESC
    """)
    for row in cursor.fetchall():
        print("User:", row[0], "| Fraud Count:", row[1])


# 7. Amount Analysis
def amount_analysis():
    cursor.execute("SELECT SUM(amount), AVG(amount), MAX(amount) FROM transactions")
    data = cursor.fetchone()
    print("Total Amount:", data[0])
    print("Average Amount:", data[1])
    print("Max Amount:", data[2])


# 8. Location Fraud Analysis
def location_fraud():
    cursor.execute("""
        SELECT location, COUNT(*)
        FROM transactions
        WHERE is_fraud=1
        GROUP BY location
    """)
    for row in cursor.fetchall():
        print("Location:", row[0], "| Fraud Count:", row[1])


# 9. Add User
def add_user():
    name = input("Enter Name: ")
    city = input("Enter City: ")

    cursor.execute("INSERT INTO users (name, city) VALUES (%s, %s)", (name, city))
    conn.commit()

    print("✅ User Added")


# 10. Delete Transaction
def delete_txn():
    tid = int(input("Enter Transaction ID: "))
    cursor.execute("DELETE FROM transactions WHERE txn_id=%s", (tid,))
    conn.commit()
    print("🗑️ Transaction Deleted")


# ================= MENU ================= #

while True:
    print("\n====== FRAUD DETECTION SYSTEM ======")
    print("1. Add Transaction")
    print("2. Show Report")
    print("3. View All Transactions")
    print("4. View Fraud Transactions")
    print("5. User Transaction History")
    print("6. Top Fraud Users")
    print("7. Amount Analysis")
    print("8. Location Fraud Analysis")
    print("9. Add User")
    print("10. Delete Transaction")
    print("11. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        add_transaction()
    elif choice == '2':
        show_report()
    elif choice == '3':
        view_transactions()
    elif choice == '4':
        view_fraud()
    elif choice == '5':
        user_history()
    elif choice == '6':
        top_fraud_users()
    elif choice == '7':
        amount_analysis()
    elif choice == '8':
        location_fraud()
    elif choice == '9':
        add_user()
    elif choice == '10':
        delete_txn()
    elif choice == '11':
        print("👋 Exiting...")
        break
    else:
        print("❌ Invalid choice")