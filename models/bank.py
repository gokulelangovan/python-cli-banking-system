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
        if not sender:
            raise ValueError("Sender account not found")

        receiver = self.get_account(to_acc)
        if not receiver:
            raise ValueError("Receiver account not found")

        if from_acc == to_acc:
            raise ValueError("Cannot transfer to the same account")

        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        if sender.balance < amount:
            raise ValueError("Insufficient funds in sender account")

        # Perform transfer
        sender.withdraw(amount)
        receiver.deposit(amount)

        self.save_accounts()

        return sender.balance, receiver.balance