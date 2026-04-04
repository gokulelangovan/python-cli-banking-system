from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import sqlite3
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

# -----------------------------
# CONFIG
# -----------------------------
SECRET_KEY = "secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -----------------------------
# DB
# -----------------------------
def get_connection():
    conn = sqlite3.connect("bank.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.executescript("""

        DROP TABLE IF EXISTS transactions;
        DROP TABLE IF EXISTS accounts;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS users;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            customer_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            account_number TEXT UNIQUE,
            account_type TEXT,
            balance REAL DEFAULT 0
        );

        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            transaction_type TEXT,
            amount REAL,
            reference TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        """)

# -----------------------------
# APP
# -----------------------------
app = FastAPI(title="Goku Bank API 🚀")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# AUTH HELPERS
# -----------------------------
def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def home():
    return {"message": "Goku Bank API running 🚀"}

# -----------------------------
# REGISTER
# -----------------------------
@app.post("/register")
def register(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email & password required")

    hashed = hash_password(password)

    with get_connection() as conn:
        try:
            cursor = conn.execute(
                "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
                (email, hashed)
            )
            conn.commit()
            return {"message": "User created", "user_id": cursor.lastrowid}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

# -----------------------------
# LOGIN
# -----------------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_connection() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (form_data.username,)
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(status_code=400, detail="Wrong password")

        token = create_token(user["id"])
        return {"access_token": token, "token_type": "bearer"}

# -----------------------------
# CREATE ACCOUNT
# -----------------------------
@app.post("/create-account")
def create_account(data: dict, user_id: int = Depends(get_current_user)):
    name = data.get("full_name")
    phone = data.get("phone")
    acc_type = data.get("account_type", "savings")

    with get_connection() as conn:

        user = conn.execute(
            "SELECT * FROM users WHERE id=?",
            (user_id,)
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        email = user["email"]

        customer = conn.execute(
            "SELECT * FROM customers WHERE email=?",
            (email,)
        ).fetchone()

        if customer:
            customer_id = customer["id"]
        else:
            cursor = conn.execute(
                "INSERT INTO customers (full_name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )
            customer_id = cursor.lastrowid

        conn.execute(
            "UPDATE users SET customer_id=? WHERE id=?",
            (customer_id, user_id)
        )

        account_number = f"ACC{int(datetime.utcnow().timestamp())}"

        cursor = conn.execute(
            "INSERT INTO accounts (customer_id, account_number, account_type) VALUES (?, ?, ?)",
            (customer_id, account_number, acc_type)
        )

        conn.commit()

        return {
            "account_number": account_number
        }

# -----------------------------
# DEPOSIT
# -----------------------------
@app.post("/deposit")
def deposit(data: dict, user_id: int = Depends(get_current_user)):
    acc = data["account_number"]
    amount = data["amount"]

    with get_connection() as conn:
        account = conn.execute(
            "SELECT * FROM accounts WHERE account_number=?",
            (acc,)
        ).fetchone()

        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE account_number=?",
            (amount, acc)
        )

        conn.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, reference) VALUES (?, ?, ?, ?)",
            (account["id"], "deposit", amount, "deposit")
        )

        conn.commit()

    return {"message": "Deposit successful"}

# -----------------------------
# TRANSFER
# -----------------------------
@app.post("/transfer")
def transfer(data: dict, user_id: int = Depends(get_current_user)):
    sender = data["from_account"]
    receiver = data["to_account"]
    amount = data["amount"]

    with get_connection() as conn:

        s = conn.execute(
            "SELECT * FROM accounts WHERE account_number=?",
            (sender,)
        ).fetchone()

        r = conn.execute(
            "SELECT * FROM accounts WHERE account_number=?",
            (receiver,)
        ).fetchone()

        if not s or not r:
            raise HTTPException(status_code=404, detail="Account not found")

        if s["balance"] < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id=?",
            (amount, s["id"])
        )
        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id=?",
            (amount, r["id"])
        )

        conn.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, reference) VALUES (?, ?, ?, ?)",
            (s["id"], "transfer", amount, f"to {receiver}")
        )

        conn.commit()

    return {"message": "Transfer successful"}

# -----------------------------
# MY TRANSACTIONS
# -----------------------------
@app.get("/my-transactions")
def my_transactions(user_id: int = Depends(get_current_user)):

    with get_connection() as conn:

        user = conn.execute(
            "SELECT * FROM users WHERE id=?",
            (user_id,)
        ).fetchone()

        if not user or not user["customer_id"]:
            return []

        accounts = conn.execute(
            "SELECT id FROM accounts WHERE customer_id=?",
            (user["customer_id"],)
        ).fetchall()

        account_ids = [a["id"] for a in accounts]

        if not account_ids:
            return []

        query = f"""
        SELECT * FROM transactions
        WHERE account_id IN ({','.join(['?']*len(account_ids))})
        ORDER BY id DESC
        """

        rows = conn.execute(query, account_ids).fetchall()

    return [dict(r) for r in rows]