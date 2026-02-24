import os

# ------------------ Helper Functions ------------------

def success(message):
    print(f"✔ {message}")


def error(message):
    print(f"✖ {message}")


def get_int_input(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        raise ValueError("Please enter a valid number.")


def get_float_input(prompt):
    try:
        return float(input(prompt).strip())
    except ValueError:
        raise ValueError("Please enter a valid amount.")

# ------------------ Deleting Bank Data and statements Functions ------------------

def clear_bank_data(file_path="accounts.json"):
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Bank data cleared")
    else:
        print("No data file found")

def delete_single_statement(account_number):
    filename = f"statement_{account_number}.txt"

    if os.path.exists(filename):
        os.remove(filename)
        print(f"Statement file '{filename}' deleted successfully.")
    else:
        print(f"No statement file found for account {account_number}.") 
 
def clear_statements():
    for file in os.listdir():
        if file.startswith("statement_") and file.endswith(".txt"):
            os.remove(file)
    print("Statements deleted successfully...")