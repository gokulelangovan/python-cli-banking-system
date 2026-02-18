class BankAccount:
    def __init__(self, account_number, owner, balance):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.account_number = account_number
        self.owner = owner
        self.balance = balance

    # ------------------ Core Operations ------------------

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > self.balance:
            raise ValueError("Insufficient funds")

        self.balance -= amount

    # ------------------ Serialization ------------------

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "owner": self.owner,
            "balance": self.balance
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["account_number"],
            data["owner"],
            data["balance"]
        )

    # ------------------ Display ------------------

    def display(self):
        print(f"Account No : {self.account_number}")
        print(f"Owner      : {self.owner}")
        print(f"Balance    : ₹{self.balance:.2f}")
        print("-" * 30)
