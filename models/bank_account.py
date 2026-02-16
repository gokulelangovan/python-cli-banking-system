class BankAccount:
	def __init__(self, account_number, owner, balance):
    		if balance < 0:
        		raise ValueError("Initial balance cannot be negative")

    		self.account_number = account_number
    		self.owner = owner
    		self.balance = balance

	def deposit(self, amount):
		if amount <= 0:
			raise ValueError("Amount must be positive")
		self.balance += amount

	def withdraw(self, amount):
		if amount <= 0:
			raise ValueError("Amount must be positive")
		if amount > self.balance:
			raise ValueError("Insufficient funds")
		self.balance -= amount
	
	def display(self):
		print(f"Account No: {self.account_number}")
		print(f"Owner: {self.owner}")
		print(f"Balance: {self.balance}")
		print("-" * 30)
