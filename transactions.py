from db import get_connection

def balance_check(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT balance FROM trans.users WHERE username = ?",
            (username,)
        )

        row = cursor.fetchone()
        return row[0] if row else "User not found"

    except Exception as e:
        return f"Error: {e}"

    finally:
        cursor.close()
        conn.close()


def deposit_money(username, money):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM trans.users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if not row:
            return "User not found"

        updated_balance = row[0] + money

        cursor.execute(
            "UPDATE trans.users SET balance = ? WHERE username = ?",
            (updated_balance, username)
        )

        cursor.execute(
            "INSERT INTO trans.transactions (username,TransactionType,Amount,BalanceAfter,date_time) values (?,?,?,?,getdate())",
            (username, 'Deposit', money, updated_balance)
        )

        conn.commit()
        return updated_balance

    except Exception as e:
        return f"Error: {e}"

    finally:
        cursor.close()
        conn.close()


def withdraw_money(username, money):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM trans.users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if not row:
            return "User not found"

        if row[0] >= money:
            updated_balance = row[0] - money

            cursor.execute(
                "UPDATE trans.users SET balance = ? WHERE username = ?",
                (updated_balance, username)
            )

            cursor.execute(
                "INSERT INTO trans.transactions (username,TransactionType,Amount,BalanceAfter,date_time) values (?,?,?,?,getdate())",
                (username, 'Withdraw', money, updated_balance)
            )

            conn.commit()
            return updated_balance
        else:
            return "Low account balance ❌"

    except Exception as e:
        return f"Error: {e}"

    finally:
        cursor.close()
        conn.close()


def transfer_money(from_user, to_user, amount):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        conn.autocommit = False
        cursor = conn.cursor()

        # Sender check
        cursor.execute("SELECT balance FROM trans.users WHERE username = ?", (from_user,))
        sender = cursor.fetchone()

        if not sender:
            return "Sender not found ❌"

        if sender[0] < amount:
            return "Insufficient balance ❌"

        # Receiver check
        cursor.execute("SELECT balance FROM trans.users WHERE username = ?", (to_user,))
        receiver = cursor.fetchone()

        if not receiver:
            return "Receiver not found ❌"

        # Debit sender
        cursor.execute(
            "UPDATE trans.users SET balance = balance - ? WHERE username = ?",
            (amount, from_user)
        )

        cursor.execute("SELECT balance FROM trans.users WHERE username=?", (from_user,))
        sender_balance = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO trans.transactions VALUES (?, ?, ?, ?, getdate())",
            (from_user, 'Transferred out', amount, sender_balance)
        )

        # Credit receiver
        cursor.execute(
            "UPDATE trans.users SET balance = balance + ? WHERE username = ?",
            (amount, to_user)
        )

        cursor.execute("SELECT balance FROM trans.users WHERE username=?", (to_user,))
        receiver_balance = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO trans.transactions VALUES (?, ?, ?, ?, getdate())",
            (to_user, 'Transferred in', amount, receiver_balance)
        )

        conn.commit()
        return f"Transferred {amount} successfully ✅"

    except Exception as e:
        if conn:
            conn.rollback()
        return f"Transaction failed ❌ Error: {e}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
