from models.bank import Bank

bank = Bank("Goku Bank")

while True:
    print("\n1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Display All Accounts")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        try:
            owner = input("Enter owner name: ")
            balance = float(input("Enter initial balance: "))
            acc_no = bank.create_account(owner, balance)
            print(f"Account created successfully. Account Number: {acc_no}")
        except ValueError as e:
            print(e)

    elif choice == "2":
        try:
            acc_no = int(input("Enter account number: "))
            amount = float(input("Enter deposit amount: "))
            bank.deposit(acc_no, amount)
            print("Deposit successful")
        except ValueError as e:
            print(e)

    elif choice == "3":
        try:
            acc_no = int(input("Enter account number: "))
            amount = float(input("Enter withdraw amount: "))
            bank.withdraw(acc_no, amount)
            print("Withdraw successful")
        except ValueError as e:
            print(e)

    elif choice == "4":
        bank.display_all_accounts()

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")
