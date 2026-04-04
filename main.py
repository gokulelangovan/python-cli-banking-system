# main.py - correct order

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
# ... all other imports ...

app = FastAPI(title="Goku Bank API 🚀")  # ✅ Only ONE app

from database.connection import get_connection

def init_db():
    with get_connection() as conn:
        conn.executescript("""
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS accounts;
        DROP TABLE IF EXISTS transactions;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            hashed_password TEXT,
            customer_id INTEGER
        );

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT UNIQUE,
            phone TEXT
        );

        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            balance REAL DEFAULT 0,
            type TEXT
        );

        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account INTEGER,
            to_account INTEGER,
            amount REAL,
            reference TEXT
        );
        """)

# 👇 CALL THIS AFTER app creation
init_db()

app.add_middleware(                        # ✅ Middleware right after
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes below...
from schemas.banking_schema import (
    CreateAccountRequest,
    CreateAccountResponse,
    DepositRequest,
    WithdrawRequest,
    TransferRequest
)
from schemas.auth_schema import UserRegister

from services.auth_service import AuthService
from services.user_service import get_customer_id_by_user
from services.auth_dependency import get_current_user
from services.service_factory import get_banking_service

from repositories.customer_repository import CustomerRepository
from repositories.account_repository import AccountRepository
from database.connection import get_connection
auth_service = AuthService()
customer_repo = CustomerRepository()
account_repo = AccountRepository()


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def home():
    return {"message": "Goku Bank API running 🚀"}


# -----------------------------
# Register
# -----------------------------
@app.post("/register")
def register(user: UserRegister):
    try:
        user_id = auth_service.register_user(user.email, user.password)

        return {
            "message": "User created successfully",
            "user_id": user_id
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------
# Login
# -----------------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = auth_service.login_user(
            form_data.username,
            form_data.password
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------
# Create Account
# -----------------------------
@app.post("/create-account", response_model=CreateAccountResponse)
def create_account(
    request: CreateAccountRequest,
    user_id: int = Depends(get_current_user)
):
    try:
        conn = get_connection()

        user = conn.execute(
            "SELECT email FROM users WHERE id=?",
            (user_id,)
        ).fetchone()

        email = user["email"]

        existing_customer = customer_repo.get_by_email(email)

        if existing_customer:
            customer_id = existing_customer["id"]
            
        else:
            customer_id = customer_repo.create_customer(
                request.full_name,
                email,
                request.phone
            )

        conn.execute(
            "UPDATE users SET customer_id=? WHERE id=?",
            (customer_id, user_id)
        )
        conn.commit()

        account_number = account_repo.create_account(
            customer_id,
            request.account_type
        )

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
def deposit(
    request: DepositRequest,
    service=Depends(get_banking_service),
    user_id: int = Depends(get_current_user)
):
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
def withdraw(
    request: WithdrawRequest,
    service=Depends(get_banking_service),
    user_id: int = Depends(get_current_user)
):
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
def transfer(
    request: TransferRequest,
    service=Depends(get_banking_service),
    user_id: int = Depends(get_current_user)
):

    customer_id = get_customer_id_by_user(user_id)

    sender_account = account_repo.get_by_account_number(request.sender_account)

    if not sender_account:
        raise HTTPException(status_code=404, detail="Sender account not found")

    if sender_account["customer_id"] != customer_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return service.transfer(
        request.sender_account,
        request.receiver_account,
        request.amount
    )

# -----------------------------
# My Accounts
# -----------------------------
@app.get("/my-accounts")
def my_accounts(
    service=Depends(get_banking_service),
    user_id: int = Depends(get_current_user)
):

    customer_id = get_customer_id_by_user(user_id)

    if not customer_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer = customer_repo.get_customer_by_id(customer_id)

    accounts = service.get_my_accounts(customer_id)

    return {
        "customer": {
            "name": customer["full_name"],
            "email": customer["email"],
            "phone": customer["phone"]
        },
        "accounts": [dict(a) for a in accounts]
    }
   
# -----------------------------
# My Transactions
# -----------------------------
@app.get("/my-transactions")
def my_transactions(user_id: int = Depends(get_current_user)):
    customer_id = get_customer_id_by_user(user_id)

    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT t.*
            FROM transactions t
            WHERE t.from_account IN (
                SELECT id FROM accounts WHERE customer_id = ?
            )
            OR t.to_account IN (
                SELECT id FROM accounts WHERE customer_id = ?
            )
            ORDER BY t.id DESC
        """, (customer_id, customer_id))

        transactions = [dict(row) for row in cursor.fetchall()]

    return transactions
    
# -----------------------------
# Profile check
# -----------------------------
@app.get("/my-profile")
def my_profile(
    user_id: int = Depends(get_current_user)
):

    customer_id = get_customer_id_by_user(user_id)

    if not customer_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer = customer_repo.get_customer_by_id(customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return dict(customer)