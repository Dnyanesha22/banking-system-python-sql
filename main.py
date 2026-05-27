from auth import user_cred, register_user
from transactions import balance_check, deposit_money, withdraw_money, transfer_money
import os

def main():

    print("\n====================================")
    print("     Sudke Banking Service")
    print("====================================\n")

    print("1. Register (New User)")
    print("2. Login (Existing User)")

    while True:
        try:
            opening = int(input("\nEnter your choice (1-2): "))
            if opening in (1, 2):
                break
        except ValueError:
            print("Enter valid number")

    if opening == 1:
        print(register_user(input("Username: "), input("Password: ")))

    elif opening == 2:
        username = input("Username: ")
        password = input("Password: ")

        if user_cred(username, password) == "success":

            while True:
                print("\n1. Balance\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Exit")

                choice = int(input("Choice: "))

                if choice == 1:
                    print(balance_check(username))

                elif choice == 2:
                    print(deposit_money(username, int(input("Amount: "))))

                elif choice == 3:
                    print(withdraw_money(username, int(input("Amount: "))))

                elif choice == 4:
                    print(transfer_money(username, input("To: "), int(input("Amount: "))))

                elif choice == 5:
                    break

# Run
main()