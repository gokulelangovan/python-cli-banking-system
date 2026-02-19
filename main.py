from models.bank import Bank

bank = Bank("Goku Bank")

print(f"----------WELCOME to {bank.bank_name}----------")

while True:
    print("\n1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Display All Accounts")
    print("6. Exit")

    choice = input("Choose an option: ")

    # 🔹 CREATE ACCOUNT
    if choice == "1":
        try:
            owner = input("Enter owner name: ")
            balance = float(input("Enter initial balance: "))
            acc_no = bank.create_account(owner, balance)
            print(f"Account created successfully. Account Number: {acc_no} and ${balance:.2f}")
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
                continue

            amount = float(input("Enter deposit amount: "))
            new_balance = bank.deposit(acc_no, amount)
            print(f"Deposit Successful. Updated Balance in Account {acc_no}: ${new_balance:.2f}")

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
                continue

            amount = float(input("Enter withdraw amount: "))
            new_balance = bank.withdraw(acc_no, amount)
            print(f"Withdraw Successful. Updated Balance in Account {acc_no}: ${new_balance:.2f}")

        except ValueError as e:
            print(e)

    # 🔹 Transfer
    elif choice == "4":
        try:
            # Sender validation loop
            while True:
                from_acc = int(input("Enter sender account number: "))
                if bank.get_account(from_acc):
                    break
                print("Sender account not found. Try again.")

            # Receiver validation loop
            while True:
                to_acc = int(input("Enter receiver account number: "))
                if not bank.get_account(to_acc):
                    print("Receiver account not found. Try again.")
                    continue
                if to_acc == from_acc:
                    print("Cannot transfer to same account.")
                    continue
                break

            amount = float(input("Enter transfer amount: "))

            sender_balance, receiver_balance = bank.transfer(from_acc, to_acc, amount)

            print("Transfer Successful.")
            print(f"Sender (Acc {from_acc}) New Balance   : ₹{sender_balance:.2f}")
            print(f"Receiver (Acc {to_acc}) New Balance : ₹{receiver_balance:.2f}")

        except ValueError as e:
            print(e)
            
    # 🔹 DISPLAY
    elif choice == "5":
        if not bank.accounts:
            print("No accounts found. Please create an account first.")
            continue

        bank.display_all_accounts()

    # 🔹 EXIT
    elif choice == "6":
        print("Exiting...")
        break

    else:
        print("Invalid choice.")
