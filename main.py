from models.bank import Bank

bank = Bank("Goku Bank")


# ------------------ Helper Functions ------------------

def success(message):
    print(f"✔ {message}")


def error(message):
    print(f"✖ {message}")


def get_int_input(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        raise ValueError("Please enter a valid number.")


def get_float_input(prompt):
    try:
        return float(input(prompt).strip())
    except ValueError:
        raise ValueError("Please enter a valid amount.")


# ------------------ Main Program ------------------

print(f"\n---------- WELCOME TO {bank.bank_name.upper()} ----------")

while True:
    print("\n1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. View Transaction History")
    print("6. Display All Accounts")
    print("7. Export Account Statement")
    print("8. Exit")

    choice = input("Choose an option: ").strip()

    # 🔹 CREATE ACCOUNT
    if choice == "1":
    # Loop until account creation succeeds
        while True:
            try:
                owner = input("Enter owner name: ").strip()
                balance = float(input("Enter initial balance: "))

                acc_no = bank.create_account(owner, balance)
                success(f"Account created. Account No: {acc_no} | Balance: ₹{balance:.2f}")
                break

            except ValueError as e:
                error(e)

    # 🔹 DEPOSIT
    elif choice == "2":
        try:
            acc_no = get_int_input("Enter account number: ")
            amount = get_float_input("Enter deposit amount: ")
            new_balance = bank.deposit(acc_no, amount)
            success(f"Deposit successful. Updated Balance (Acc {acc_no}): ₹{new_balance:.2f}")
        except ValueError as e:
            error(e)

    # 🔹 WITHDRAW
    elif choice == "3":
        try:
            acc_no = get_int_input("Enter account number: ")
            amount = get_float_input("Enter withdraw amount: ")
            new_balance = bank.withdraw(acc_no, amount)
            success(f"Withdraw successful. Updated Balance (Acc {acc_no}): ₹{new_balance:.2f}")
        except ValueError as e:
            error(e)

    # 🔹 TRANSFER
    elif choice == "4":
        try:
            while True:
                from_acc = get_int_input("Enter sender account number: ")
                if bank.get_account(from_acc):
                    break
                error("Sender account not found. Try again.")

            while True:
                to_acc = get_int_input("Enter receiver account number: ")
                if not bank.get_account(to_acc):
                    error("Receiver account not found. Try again.")
                    continue
                if to_acc == from_acc:
                    error("Cannot transfer to same account.")
                    continue
                break

            amount = get_float_input("Enter transfer amount: ")

            sender_balance, receiver_balance = bank.transfer(from_acc, to_acc, amount)

            success("Transfer successful.")
            print(f"   Sender (Acc {from_acc})   → ₹{sender_balance:.2f}")
            print(f"   Receiver (Acc {to_acc}) → ₹{receiver_balance:.2f}")

        except ValueError as e:
            error(e)

    # 🔹 VIEW TRANSACTION HISTORY
    elif choice == "5":
        try:
            acc_no = get_int_input("Enter account number: ")
            account = bank.get_account(acc_no)

            if not account:
                error("Account not found.")
            elif not account.transactions:
                error("No transactions found.")
            else:
                print(f"\n--- Transaction History (Account {acc_no}) ---\n")

                for index, txn in enumerate(account.transactions, start=1):
                    txn_type = txn["type"].replace("_", " ").title()
                    amount = txn["amount"]
                    balance_after = txn["balance_after"]
                    timestamp = txn["timestamp"]

                    print(
                        f"{index}. [{timestamp}] "
                        f"{txn_type:<12} "
                        f"₹{amount:.2f} → Balance: ₹{balance_after:.2f}"
                    )

                print("-" * 50)

        except ValueError as e:
            error(e)

    # 🔹 DISPLAY ALL ACCOUNTS
    elif choice == "6":
        if not bank.accounts:
            error("No accounts found.")
        else:
            bank.display_all_accounts()

    # 🔹 EXPORT STATEMENT (Single + Multiple)
    elif choice == "7":
        print("\n1. Export Single Account")
        print("2. Export Multiple Accounts")

        sub_choice = input("Choose option: ").strip()

        # Single
        if sub_choice == "1":
            try:
                acc_no = get_int_input("Enter account number: ")
                file_name = bank.export_statement(acc_no)
                success(f"Statement exported → {file_name}")
            except ValueError as e:
                error(e)

        # Multiple
        elif sub_choice == "2":
            raw_input_accounts = input("Enter account numbers separated by comma: ").strip()

            try:
                account_numbers = [
                    int(acc.strip()) for acc in raw_input_accounts.split(",")
                ]

                for acc_no in account_numbers:
                    try:
                        file_name = bank.export_statement(acc_no)
                        success(f"Statement exported → {file_name}")
                    except ValueError as e:
                        error(f"Account {acc_no} → {e}")

            except ValueError:
                error("Invalid account list format.")

        else:
            error("Invalid option.")

    # 🔹 EXIT
    elif choice == "8":
        print("Exiting... 👋")
        break

    else:
        error("Invalid choice.")