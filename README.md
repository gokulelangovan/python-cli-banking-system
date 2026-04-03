# 🏦 Goku Bank API

A lightweight **Banking Backend API** built with **FastAPI** that simulates core banking operations such as deposits, withdrawals, transfers, and transaction history.

This project focuses on **clean backend architecture**, modular design, and safe transaction handling.

---

# 🚀 Features

- Create customer accounts
- Deposit money
- Withdraw money with balance validation
- Atomic money transfers between accounts
- Transaction history tracking
- Input validation using **Pydantic**
- Logging for audit and debugging
- Modular backend architecture

---

# 🧠 Tech Stack

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn

---

# 📂 Project Structure

```
goku-bank-api/
│
├── main.py                # FastAPI application entry
│
├── database/
│   ├── connection.py      # SQLite connection handler
│   ├── init_db.py         # Database initialization
│   └── schema.sql         # Database schema
│
├── repositories/          # Data access layer
│   ├── account_repository.py
│   ├── customer_repository.py
│   └── transaction_repository.py
│
├── services/              # Business logic layer
│   ├── banking_service.py
│   └── logger.py
│
├── schemas/               # Request/Response models
│   └── banking_schema.py
│
└── requirements.txt
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd goku-bank-api
```

---

## 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Initialize the database

```bash
python -m database.init_db
```

This creates the SQLite database and tables.

---

## 4️⃣ Run the API server

```bash
python -m uvicorn main:app --reload
```

---

# 📘 API Documentation

FastAPI automatically provides interactive documentation.

Open:

```
http://127.0.0.1:8000/docs
```

You can test endpoints directly from the Swagger UI.

---

# 🔐 Example API Requests

## Create Account

POST `/create-account`

```json
{
  "name": "Gokul",
  "email": "gokul@email.com",
  "phone": "7299169318"
}
```

---

## Deposit Money

POST `/deposit`

```json
{
  "account_number": "ACC1001",
  "amount": 500
}
```

---

## Transfer Money

POST `/transfer`

```json
{
  "sender_account": "ACC1001",
  "receiver_account": "ACC1002",
  "amount": 200
}
```

---

# 📊 Logging

All banking operations are logged.

Example log entry:

```
INFO Deposit 1000 to ACC1001
INFO Withdraw 200 from ACC1001
INFO Transfer 300 from ACC1001 to ACC1002
```

---

# 📚 Learning Objectives

This project demonstrates:

- Clean backend architecture
- Repository & Service layer design
- Transaction safety in financial operations
- API validation with Pydantic
- Logging and debugging practices

---

# 👨‍💻 Author

**Gokul (Pappu 🐼)**  
Backend Developer | Python Enthusiast