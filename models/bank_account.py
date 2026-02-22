from datetime import datetime
class BankAccount:
    def __init__(self, account_number, owner, balance):
        owner = owner.strip()

        if not owner:
            raise ValueError("Owner name cannot be empty.")

        if not all(char.isalpha() or char.isspace() for char in owner):
            raise ValueError("Owner name must contain only letters and spaces.")

        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.account_number = account_number
        self.owner = owner
        self.balance = balance
        self.transactions = []
    # ------------------ Core Operations ------------------

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount
        self.add_transaction("deposit",amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > self.balance:
            raise ValueError("Insufficient funds")

        self.balance -= amount
        self.add_transaction("withdraw",amount)

    # ------------------ Serialization ------------------

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "owner": self.owner,
            "balance": self.balance,
            "transactions": self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(
            data["account_number"],
            data["owner"],
            data["balance"]
        )
        account.transactions = data.get("transactions", [])
        return account

    # ------------------ Transactions -------------------
    
    def add_transaction(self, txn_type, amount):
        transaction = {
            "type" : txn_type,
            "amount": amount,
            "balance_after" : self.balance,
            "timestamp" : datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
           
        self.transactions.append(transaction)
            
    # ------------------ Display ------------------

    def display(self):
        print(f"Account No : {self.account_number}")
        print(f"Owner      : {self.owner}")
        print(f"Balance    : ₹{self.balance:.2f}")
        print("-" * 30)
