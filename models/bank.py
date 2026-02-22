import json
from .bank_account import BankAccount


class Bank:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.accounts = {}
        self.next_account_number = 1001
        self.file_name = "accounts.json"
        self.load_accounts()

    def __str__(self):
        return f"----------WELCOME to {self.bank_name}----------"

    # ------------------ Persistence ------------------

    def load_accounts(self):
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)

                for acc_data in data:
                    account = BankAccount.from_dict(acc_data)
                    self.accounts[account.account_number] = account

                if self.accounts:
                    self.next_account_number = max(self.accounts.keys()) + 1

        except FileNotFoundError:
            # First run: file does not exist yet
            pass

    def save_accounts(self):
        data = [account.to_dict() for account in self.accounts.values()]

        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    # ------------------ Core Operations ------------------

    def create_account(self, owner, balance):
        acc_no = self.next_account_number
        account = BankAccount(acc_no, owner, balance)

        self.accounts[acc_no] = account
        self.next_account_number += 1

        self.save_accounts()
        return acc_no

    def deposit(self, account_number, amount):
        account = self.get_account(account_number)

        if not account:
            raise ValueError("Account not found")

        account.deposit(amount)
        self.save_accounts()

        return account.balance

    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)

        if not account:
            raise ValueError("Account not found")

        account.withdraw(amount)
        self.save_accounts()

        return account.balance

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def display_all_accounts(self):
        if not self.accounts:
            print("No accounts found.")
        else:
            for account in self.accounts.values():
                account.display()

# ------------------ Transfer Operations ------------------

    def transfer(self, from_acc, to_acc, amount):
        sender = self.get_account(from_acc)
        receiver = self.get_account(to_acc)

        if not sender:
            raise ValueError("Sender account not found")
        if not receiver:
            raise ValueError("Receiver account not found")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if amount > sender.balance:
            raise ValueError("Insufficient funds")

        # Direct balance mutation (not using withdraw/deposit)
        sender.balance -= amount
        receiver.balance += amount

        # Log only transfer events
        sender.add_transaction("transfer_out", amount)
        receiver.add_transaction("transfer_in", amount)

        self.save_accounts()

        return sender.balance, receiver.balance
        
 # ------------------ Export Statement ------------------   

    def export_statement(self, account_number):
        account = self.get_account(account_number)
        
        if not account:
            raise ValueError("Account not found")
            
        if not account.transactions:
            raise ValueError("No transactions found for this account")
            
        file_name = f"statement_{account_number}.txt"
        
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(f"{self.bank_name.upper()} - ACCOUNT STATEMENT\n")
            file.write(f"Account No: {account.account_number}\n")
            file.write(f"Owner: {account.owner}\n")
            file.write("-" * 50 + "\n\n")
            
            for index, txn in enumerate(account.transactions, start=1):
                txn_type = txn["type"].replace("_", " ").title()
                amount = txn["amount"]
                balance_after = txn["balance_after"]
                timestamp = txn["timestamp"]
                
                line = (
                    f"{index}. [{timestamp}] "
                    f"{txn_type:<12}"
                    f"₹{amount:.2f} → Balance: ₹{balance_after:.2f}\n"
                )  
                
                file.write(line)
                
        return file_name

            
            
 