from fastapi import FastAPI
from models.bank import Bank

app = FastAPI()

bank = Bank("Goku Bank")

@app.get("/")
def home():
    return {"message": "Banking API running"}
    
@app.post("/create-account")
def create_account(owner: str, balance: float):
    acc_no = bank.create_account(owner, balance)
    return {
        "message": "Account created",
        "account_number": acc_no,
        "balance": balance
    }
    
@app.post("/deposit")
def deposit(account_number: int, amount: float):
    new_balance = bank.deposit(account_number, amount)
    return {
        "message": "Deposit successful",
        "new_balance": new_balance
    }

@app.post("/withdraw")
def withdraw(account_number: int, amount: float):
    new_balance = bank.withdraw(account_number, amount)
    return {
        "message": "Withdraw successful",
        "new_balance": new_balance
    }

@app.post("/transfer")
def transfer(sender_account: str, receiver_account: str, amount: float):

    result = service.transfer(sender_account, receiver_account, amount)

    return {
        "message": result
    }
    
from models.utils import (
    clear_bank_data,
    delete_single_statement,
    clear_statements,
    success,
    error,
)

# ------------------ Helper Functions ------------------


def get_float_input_or_cancel(prompt):
    while True:
        value = input(f"{prompt} (0 to cancel): ").strip()

        try:
            amount = float(value)
            if amount == 0:
                print("Operation cancelled.\n")
                return None
            return amount
        except ValueError:
            error("Please enter a valid amount.")


def get_account_or_cancel(bank, prompt="Enter account number", max_attempts=3):
    attempts = 0

    while attempts < max_attempts:
        try:
            acc_no = int(input(f"{prompt} (0 to cancel): ").strip())

            if acc_no == 0:
                print("Operation cancelled.\n")
                return None

            account = bank.get_account(acc_no)

            if account:
                return account
            else:
                error("Account not found.")
                attempts += 1

        except ValueError:
            error("Please enter a valid number.")
            attempts += 1

    print("Too many failed attempts. Returning to menu.\n")
    return None


def get_transfer_accounts(bank, max_attempts=3):
    print("\n--- Transfer Setup ---")

    sender = get_account_or_cancel(
        bank, prompt="Enter sender account number", max_attempts=max_attempts
    )
    if not sender:
        return None, None

    attempts = 0
    while attempts < max_attempts:
        try:
            acc_no = int(input("Enter receiver account number (0 to cancel): ").strip())

            if acc_no == 0:
                print("Transfer cancelled.\n")
                return None, None

            if acc_no == sender.account_number:
                error("Cannot transfer to the same account.")
                attempts += 1
                continue

            receiver = bank.get_account(acc_no)

            if receiver:
                return sender, receiver
            else:
                error("Receiver account not found.")
                attempts += 1

        except ValueError:
            error("Please enter a valid number.")
            attempts += 1

    print("Too many failed attempts. Returning to menu.\n")
    return None, None


# ------------------ Main Program ------------------
def run_cli():
    print("\n" + "=" * 50)
    print(f"{f'WELCOME TO {bank.bank_name.upper()}'.center(50)}")
    print("=" * 50)

    while True:
        print("\n1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Display")
        print("6. View Transaction History")
        print("7. Export Account Statement")
        print("8. Manage Data")
        print("9. Exit")

        choice = input("Choose an option: ").strip()

        # 🔹 CREATE ACCOUNT
        if choice == "1":
            while True:
                try:
                    owner = input("Enter owner name: ").strip()

                    balance = get_float_input_or_cancel("Enter initial balance")
                    if balance is None:
                        continue

                    acc_no = bank.create_account(owner, balance)
                    success(
                        f"Account created. Account No: {acc_no} | Balance: ₹{balance:.2f}"
                    )
                    print("-" * 50)
                    print()
                    break

                except ValueError as e:
                    error(e)

        # 🔹 DEPOSIT
        elif choice == "2":
            try:
                account = get_account_or_cancel(bank)
                if not account:
                    continue

                amount = get_float_input_or_cancel("Enter deposit amount")
                if amount is None:
                    continue

                new_balance = bank.deposit(account.account_number, amount)
                success(f"Deposit successful. Updated Balance: ₹{new_balance:.2f}")
                print("-" * 50)
                print()

            except ValueError as e:
                error(e)

        # 🔹 WITHDRAW
        elif choice == "3":
            try:
                account = get_account_or_cancel(bank)
                if not account:
                    continue

                amount = get_float_input_or_cancel("Enter withdraw amount")
                if amount is None:
                    continue

                new_balance = bank.withdraw(account.account_number, amount)
                success(f"Withdraw successful. Updated Balance: ₹{new_balance:.2f}")
                print("-" * 50)
                print()

            except ValueError as e:
                error(e)

        # 🔹 TRANSFER
        elif choice == "4":
            try:
                sender, receiver = get_transfer_accounts(bank)
                if not sender or not receiver:
                    continue

                amount = get_float_input_or_cancel("Enter transfer amount")
                if amount is None:
                    continue

                sender_balance, receiver_balance = bank.transfer(
                    sender.account_number,
                    receiver.account_number,
                    amount,
                )

                success("Transfer successful.")
                print("-" * 50)
                print(f"Sender (Acc {sender.account_number})   → ₹{sender_balance:.2f}")
                print(f"Receiver (Acc {receiver.account_number}) → ₹{receiver_balance:.2f}")
                print()

            except ValueError as e:
                error(e)

        # 🔹 DISPLAY
        elif choice == "5":
            print("\n--- Display Menu ---")
            print("1. Display Single Account")
            print("2. Display All Accounts")
            print("3. Back")

            sub_choice = input("Choose option: ").strip()

            if sub_choice == "1":
                account = get_account_or_cancel(bank)
                if account:
                    account.display()
                    print()

            elif sub_choice == "2":
                if not bank.accounts:
                    error("No accounts found.")
                else:
                    bank.display_all_accounts()
                    print()

            elif sub_choice == "3":
                print()

            else:
                error("Invalid option.")

        # 🔹 VIEW TRANSACTION HISTORY
        elif choice == "6":
            print("\n--- Transaction History ---")
            print("1. View Single Account History")
            print("2. View All Accounts History")
            print("3. Back")

            sub_choice = input("Choose option: ").strip()

            if sub_choice == "1":
                account = get_account_or_cancel(bank)
                if not account:
                    continue

                if not account.transactions:
                    error("No transactions found.")
                else:
                    print(
                        f"\n--- Transaction History (Account {account.account_number}) ---\n"
                    )
                    for index, txn in enumerate(account.transactions, start=1):
                        txn_type = txn["type"].replace("_", " ").title()
                        print(
                            f"{index}. [{txn['timestamp']}] "
                            f"{txn_type:<12} "
                            f"₹{txn['amount']:.2f} → Balance: ₹{txn['balance_after']:.2f}"
                        )
                    print("-" * 50)
                    print()

            elif sub_choice == "2":
                if not bank.accounts:
                    error("No accounts found.")
                else:
                    for acc_no, account in bank.accounts.items():
                        if account.transactions:
                            print(
                                f"\n--- Transaction History (Account {acc_no}) ---\n"
                            )
                            for index, txn in enumerate(
                                account.transactions, start=1
                            ):
                                txn_type = txn["type"].replace("_", " ").title()
                                print(
                                    f"{index}. [{txn['timestamp']}] "
                                    f"{txn_type:<12} "
                                    f"₹{txn['amount']:.2f} → Balance: ₹{txn['balance_after']:.2f}"
                                )
                        else:
                            print(f"\nAccount {acc_no} → No transactions found.")
                    print("-" * 50)
                    print()

            elif sub_choice == "3":
                print()

            else:
                error("Invalid option.")

        # 🔹 EXPORT
        elif choice == "7":
            print("\n--- Export Statements ---")
            print("1. Export Single Account")
            print("2. Export All Accounts")
            print("3. Back")

            sub_choice = input("Choose option: ").strip()

            if sub_choice == "1":
                account = get_account_or_cancel(bank)
                if account:
                    file_name = bank.export_statement(account.account_number)
                    success(f"Statement exported → {file_name}")
                    print("-" * 50)
                    print()

            elif sub_choice == "2":
                if not bank.accounts:
                    error("No accounts found.")
                else:
                    for acc_no in bank.accounts:
                        try:
                            file_name = bank.export_statement(acc_no)
                            success(f"Statement exported → {file_name}")
                        except ValueError as e:
                            error(f"Account {acc_no} → {e}")
                    print("-" * 50)
                    print()

            elif sub_choice == "3":
                print()

            else:
                error("Invalid option.")

        # 🔹 MANAGE DATA
        elif choice == "8":
            while True:
                print("\n--- Manage Data ---")
                print("1. Delete Single Account")
                print("2. Delete ALL Accounts (Reset System)")
                print("3. Delete Single Statement")
                print("4. Delete All Statements")
                print("5. Back")

                sub_choice = input("Choose an option: ").strip()

                if sub_choice == "1":
                    account = get_account_or_cancel(bank)
                    if account:
                        confirm = input(
                            f"Type DELETE {account.account_number} to confirm: "
                        ).strip()

                        if confirm == f"DELETE {account.account_number}":
                            bank.delete_account(account.account_number)
                            success("Account deleted successfully.")
                            print("-" * 50)
                            print()
                        else:
                            print("Confirmation failed.\n")

                elif sub_choice == "2":
                    confirm = input(
                        "Type 'I UNDERSTAND DELETE ALL' to confirm: "
                    ).strip()

                    if confirm == "I UNDERSTAND DELETE ALL":
                        clear_bank_data()
                        success("All bank data cleared.")
                        print("-" * 50)
                        print()
                        break
                    else:
                        print("Confirmation failed.\n")

                elif sub_choice == "3":
                    account = get_account_or_cancel(bank)
                    if account:
                        delete_single_statement(account.account_number)
                        print()

                elif sub_choice == "4":
                    clear_statements()
                    success("All statement files deleted.")
                    print("-" * 50)
                    print()

                elif sub_choice == "5":
                    print()
                    break

                else:
                    error("Invalid option.")

        # 🔹 EXIT
        elif choice == "9":
            print("Exiting... 👋")
            break

        else:
            error("Invalid choice.")
            
if __name__ == "__main__":
    run_cli()