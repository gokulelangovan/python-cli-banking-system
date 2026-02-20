# Python CLI Banking System

A structured multi-account command-line banking application built using Python and Object-Oriented Programming principles.

This project evolved from a simple CLI exercise into a stateful backend-style system with layered architecture, transaction logging, and JSON-based persistence.

---

## 🚀 Features

- Create multiple bank accounts
- Auto-generated unique account numbers
- Deposit with validation
- Withdraw with balance checks
- Transfer between accounts
- Transaction history (ledger per account)
- Prevention of negative transactions
- Proper exception propagation
- JSON-based data persistence
- Nested object reconstruction from stored data
- Clean CLI interaction with formatted ledger display
- Layered project structure (UI → Service → Entity)

---

## 🧠 Concepts Demonstrated

- Object-Oriented Programming (OOP)
- Encapsulation and separation of concerns
- Exception handling and propagation
- Layered backend-style architecture
- JSON serialization and deserialization
- State persistence across runs
- Nested data persistence
- Object reconstruction from disk
- Coordinated multi-entity state mutation
- Controlled mutation boundaries
- Input validation discipline

---

## 💾 Data Persistence

The system stores account data in accounts.json.
- Accounts are automatically saved after every mutation (create, deposit, withdraw, transfer)
- Transaction history is persisted as nested data
- Data is restored automatically on program startup
- Account numbers continue correctly after restart
- Ledger entries survive across sessions

---

## 📜 Transaction Ledger

Each account maintains a transaction history including:
- Transaction type (deposit, withdraw, transfer_in, transfer_out)
- Amount
- Balance after transaction
- Timestamp
History is formatted and displayed cleanly through the CLI.

---

## 📁 Project Structure
```
project/
 ├── main.py
 ├── accounts.json (auto-generated)
 └── models/
      ├── bank.py
      └── bank_account.py
```
---

## 🛠 Tech Stack

- Python
- CLI
- JSON
- Git & GitHub

---

## ▶ How to Run

```bash
python main.py
