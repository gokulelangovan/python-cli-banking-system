from models.bank_account import BankAccount

owner = input("Enter account holder name: ")

while True:
    try:
        balance = float(input("Enter amount: "))
        break
    except ValueError:
        print("Invalid number. Try again.")

account = BankAccount(owner, balance)

while True:
    print("\n1. Deposit")
    print("2. Withdraw")
    print("3. Display")
    print("4. Rich status")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        while True:
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid number. Try again.")
        account.deposit(amount)

    elif choice == "2":
        while True:
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid number. Try again.")
        account.withdraw(amount)

    elif choice == "3":
        account.display()

    elif choice == "4":
        if account.is_rich():
            print("Account is rich 💰")
        else:
            print("Account is not rich yet.")

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid Choice")
