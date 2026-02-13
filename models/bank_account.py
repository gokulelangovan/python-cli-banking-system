class BankAccount:
	def __init__(self, owner, balance):
		self.owner = owner
		self.balance = balance

	def deposit(self, amount):
		self.balance += amount

	def withdraw(self, amount):
		if amount > self.balance:
			print("Insufficient funds")
		else:
			self.balance -= amount
	
	def display(self):
		print("Owner:", self.owner)
		print("Balance:", self.balance)

	def is_rich(self):
		return self.balance > 1000