from repositories.customer_repository import CustomerRepository
from repositories.account_repository import AccountRepository
from repositories.transaction_repository import TransactionRepository
from services.banking_service import BankingService

# Initialize repositories
customer_repo = CustomerRepository()
account_repo = AccountRepository()
transaction_repo = TransactionRepository()

# Initialize service
service = BankingService(customer_repo, account_repo, transaction_repo)

# Create customers
cust1_id = customer_repo.create_customer("Goku", "goku@test.com", "1111111111")
cust2_id = customer_repo.create_customer("Alice", "alice@test.com", "2222222222")

# Create accounts
acc1_no = "ACC1001"
acc2_no = "ACC1002"

account_repo.create_account(cust1_id, acc1_no, "SAVINGS")
account_repo.create_account(cust2_id, acc2_no, "SAVINGS")

# Deposit into sender
service.deposit(acc1_no, 1000)

# Transfer money
print(service.transfer(acc1_no, acc2_no, 200))

# Check balances
acc1 = account_repo.get_by_account_number(acc1_no)
acc2 = account_repo.get_by_account_number(acc2_no)

print("Sender Balance:", acc1["balance"])
print("Receiver Balance:", acc2["balance"])

