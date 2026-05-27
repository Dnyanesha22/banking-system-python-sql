from db import get_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def user_cred(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        password = hash_password(password)

        cursor.execute(
            "SELECT username FROM trans.users WHERE username = ? AND password = ?",
            (username, password)
        )

        row = cursor.fetchone()

        if row:
            print(f"{username} login successful ✅")
            return 'success'
        else:
            print("Invalid username or password ❌")
            return 'fail'

    except Exception as e:
        print("Error during login:", e)
        return 'fail'

    finally:
        cursor.close()
        conn.close()


def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        
        print(username,password)
        # Check if user exists
        cursor.execute(
            "SELECT 1 FROM trans.users WHERE username = ?",
            (username,)
        )
        if cursor.fetchone():
            return "Username already exists ❌"

        # Password validation
        if not (
            any(c.isalpha() for c in password) and
            any(c.isdigit() for c in password) and
            any(not c.isalnum() for c in password)
        ):
            return "Password must include letters, numbers, and special characters ❌"

        hashed_pwd = hash_password(password)

        cursor.execute(
            "INSERT INTO trans.users (username, password, account_created) VALUES (?, ?, getdate())",
            (username, hashed_pwd)
        )

        conn.commit()
        return "Registration successful ✅"

    except Exception as e:
        return f"Error: {e}"

    finally:
        cursor.close()
        conn.close()