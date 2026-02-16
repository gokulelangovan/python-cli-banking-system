from .bank_account import BankAccount

class Bank:
	def __init__(self, bank_name):
		self.bank_name = bank_name
		self.accounts = {}
		self.next_account_number = 1001

	def create_account(self, owner, balance):
		acc_no = self.next_account_number
		account = BankAccount(acc_no, owner, balance)
		self.accounts[acc_no] = account
		self.next_account_number += 1
		return acc_no
	
	def deposit(self, account_number, amount):
		account = self.get_account(account_number)
		if not account:
			raise ValueError("Account not found")
		account.deposit(amount)

	def withdraw(self, account_number, amount):
    		account = self.get_account(account_number)
    		if not account:
        		raise ValueError("Account not found")
    		account.withdraw(amount)

	def get_account(self, account_number):
		return self.accounts.get(account_number)

	def display_all_accounts(self):
        	if not self.accounts:
            		print("No accounts found.")
        	else:
            		for account in self.accounts.values():
                		account.display()
		