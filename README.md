# 🏦 CLI Banking System

**Version:** v1.0  
**Status:** Stable Release  
**Architecture:** Layered (CLI → Service → Entity → JSON Persistence)

---

## 📌 Overview

CLI Banking System is a multi-account banking simulation built in Python to demonstrate structured backend architecture, transaction modeling, and persistence handling.

This project evolved from basic scripting into a layered backend-style system with defensive CLI design, restart integrity, and version control discipline.

---

## 🚀 Features

### 🧾 Account Management
- Create multiple accounts
- Auto-generated unique account numbers
- Owner name normalization (`.title()`)
- Delete single account (with confirmation)
- Reset entire system
- No account ID reuse (audit integrity preserved)

### 💰 Transactions
- Deposit
- Withdraw
- Transfer (clean dual-entry ledger model)
- No self-transfer allowed
- No negative amounts allowed
- Insufficient fund protection
- Timestamped transaction entries

### 📜 Transaction History
- View single account history
- View all accounts history
- Clean formatted ledger display

### 📁 Statement Export
- Export single account statement
- Export all accounts statements
- Skips accounts with no transactions

### 💾 Persistence
- JSON-based storage (`accounts.json`)
- Data survives restarts
- Account numbers generated using:
- max(existing_ids) + 1
- Runtime files excluded via `.gitignore`

---

## 🏗 Architecture
CLI Layer (main.py)
↓
Service Layer (Bank)
↓
Entity Layer (BankAccount)
↓
Persistence Layer (JSON)

### Layer Responsibilities

#### CLI Layer
- User interaction
- Retry handling
- Cancel guardrails (0 to cancel)
- Submenu structure
- Output formatting

#### Service Layer (Bank)
- Account coordination
- Deposit / Withdraw / Transfer orchestration
- Persistence handling
- ID continuity control
- Deletion management

#### Entity Layer (BankAccount)
- Business rule validation
- Balance ownership
- Ledger management
- Transaction recording

---

## 🧠 Engineering Principles Applied

- Separation of concerns
- Layered architecture
- Defensive CLI design
- Transaction semantics modeling
- ID continuity (no reuse of deleted IDs)
- Persistence lifecycle awareness
- Version tagging discipline
- Repository hygiene via `.gitignore`

---

## ⚠ Limitations (v1)

- No database backend (JSON only)
- No authentication system
- No concurrency handling
- No soft-delete mechanism
- No automated test suite

---

## 🛣 Roadmap (v2 Planned)

- Replace JSON with SQLite
- Introduce Repository Layer
- Add authentication
- Convert to REST API (FastAPI)
- Add unit testing (pytest)
- Introduce soft-delete support

---

## 🏷 Release Information

**Tag:** `v1.0-cli-banking`  
**Release Type:** Stable CLI Version  

This tag represents a freeze-ready, restart-safe, ledger-consistent version of the system.

---

## ▶ How to Run

```bash
python main.py

```

---

## 📁 Project Structure

```
project/
│
├── main.py
├── README.md
├── Bank_exe.bat
│
└── models/
├── init.py
├── bank.py
├── bank_account.py
└── utils.py
```
Runtime files such as `accounts.json`, `statement_*.txt`, and `__pycache__/` are excluded from version control.

---

## 👨‍💻 Author

***Gokul Elangovan***
[Backend-focused learning project]