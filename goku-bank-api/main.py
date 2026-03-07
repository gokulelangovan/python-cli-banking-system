from fastapi import FastAPI, HTTPException

from repositories.customer_repository import CustomerRepository
from repositories.account_repository import AccountRepository
from repositories.transaction_repository import TransactionRepository

from services.banking_service import BankingService

from schemas.banking_schema import (
    CreateAccountRequest,
    CreateAccountResponse,
    DepositRequest,
    WithdrawRequest,
    TransferRequest
)

app = FastAPI(title="Goku Bank API")


# -----------------------------
# Initialize repositories
# -----------------------------

customer_repo = CustomerRepository()
account_repo = AccountRepository()
transaction_repo = TransactionRepository()

service = BankingService(customer_repo, account_repo, transaction_repo)


# -----------------------------
# Root endpoint
# -----------------------------

@app.get("/")
def home():
    return {"message": "Goku Bank API running"}


# -----------------------------
# Create Customer + Account
# -----------------------------

@app.post("/create-account", response_model=CreateAccountResponse)
def create_account(request: CreateAccountRequest):

    try:
        customer_id = customer_repo.create_customer(
            request.name,
            request.email,
            request.phone
        )

        account_number = account_repo.create_account(customer_id)

        return {
            "message": "Account created successfully",
            "account_number": account_number
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------
# Deposit
# -----------------------------

@app.post("/deposit")
def deposit(request: DepositRequest):

    try:
        new_balance = service.deposit(
            request.account_number,
            request.amount
        )

        return {
            "message": "Deposit successful",
            "new_balance": new_balance
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------
# Withdraw
# -----------------------------

@app.post("/withdraw")
def withdraw(request: WithdrawRequest):

    try:
        new_balance = service.withdraw(
            request.account_number,
            request.amount
        )

        return {
            "message": "Withdrawal successful",
            "new_balance": new_balance
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------
# Transfer
# -----------------------------

@app.post("/transfer")
def transfer(request: TransferRequest):

    try:
        result = service.transfer(
            request.sender_account,
            request.receiver_account,
            request.amount
        )

        return {"message": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@app.get("/transactions/{account_number}")
def get_transactions(account_number: str):

    account = account_repo.get_by_account_number(account_number)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    txns = transaction_repo.get_account_transactions(account["id"])

    return [dict(t) for t in txns]
        
from database.connection import get_connection

@app.get("/accounts")
def get_accounts():

    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM accounts").fetchall()

        return [dict(row) for row in rows]
        
@app.get("/customers")
def customers():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM customers").fetchall()
        return [dict(row) for row in rows]
        
@app.delete("/reset")
def reset_database():
    with get_connection() as conn:
        conn.execute("DELETE FROM accounts")
        conn.execute("DELETE FROM customers")
        conn.execute("DELETE FROM transactions")
    return {"message": "Database reset"}