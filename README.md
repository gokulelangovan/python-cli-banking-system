# Python CLI Banking System

A structured multi-account command-line banking application built using Python and Object-Oriented Programming principles.

This project demonstrates layered architecture, exception propagation, and JSON-based state persistence.

---

## 🚀 Features

- Create multiple bank accounts
- Auto-generated unique account numbers
- Deposit with validation
- Withdraw with balance checks
- Prevention of negative transactions
- Proper exception propagation
- JSON-based data persistence
- Automatic ID continuity after restart
- Clean CLI interaction
- Layered project structure (UI → Service → Entity)

---

## 🧠 Concepts Demonstrated

- Object-Oriented Programming (OOP)
- Encapsulation and separation of concerns
- Exception handling and propagation
- Layered backend-style architecture
- JSON serialization and deserialization
- State persistence across runs
- Controlled mutation boundaries
- Input validation discipline

---

## 💾 Data Persistence

The system stores account data in accounts.json.
- Accounts are automatically saved after every mutation (create, deposit, withdraw)
- Data is restored automatically on program startup
- Account numbers continue correctly after restart
- Persistence logic is handled entirely inside the Bank service layer

---

## 📁 Project Structure

project/
 ├── main.py
 ├── accounts.json (auto-generated)
 └── models/
      ├── bank.py
      └── bank_account.py


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
