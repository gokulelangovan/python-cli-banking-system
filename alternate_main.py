from models.bank import Bank

bank = Bank("Goku Bank")

print(f"----------WELCOME to {bank.bank_name}----------")

while True:
    print("\n1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Display All Accounts")
    print("5. Exit")

    choice = input("Choose an option: ")

    # 🔹 CREATE ACCOUNT
    if choice == "1":
        try:
            owner = input("Enter owner name: ")
            balance = float(input("Enter initial balance: "))
            acc_no = bank.create_account(owner, balance)
            print(f"Account created successfully. Account Number: {acc_no}")
        except ValueError as e:
            print(e)

    # 🔹 DEPOSIT
    elif choice == "2":
        if not bank.accounts:
            print("No accounts found. Please create an account first.")
            continue

        try:
            acc_no = int(input("Enter account number: "))
            account = bank.get_account(acc_no)

            if not account:
                print("Account not found.")
                continue  # ⬅ immediately go back to menu

            amount = float(input("Enter deposit amount: "))
            bank.deposit(acc_no, amount)
            print("Deposit successful")

        except ValueError as e:
            print(e)

    # 🔹 WITHDRAW
    elif choice == "3":
        if not bank.accounts:
            print("No accounts found. Please create an account first.")
            continue

        try:
            acc_no = int(input("Enter account number: "))
            account = bank.get_account(acc_no)

            if not account:
                print("Account not found.")
                continue  # ⬅ immediately go back to menu

            amount = float(input("Enter withdraw amount: "))
            bank.withdraw(acc_no, amount)
            print("Withdraw successful")

        except ValueError as e:
            print(e)

    # 🔹 DISPLAY
    elif choice == "4":
        if not bank.accounts:
            print("No accounts found. Please create an account first.")
            continue

        bank.display_all_accounts()

    # 🔹 EXIT
    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")
