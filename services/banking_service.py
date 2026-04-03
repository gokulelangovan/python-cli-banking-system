from database.connection import get_connection
from services.logger import logger

class BankingService:

    def __init__(self, customer_repo, account_repo, transaction_repo):
        self.customer_repo = customer_repo
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo


    # -----------------------------
    # Deposit
    # -----------------------------

    def deposit(self, account_number, amount):

        try:
            if amount <= 0:
                raise ValueError("Deposit amount must be positive")

            account = self.account_repo.get_by_account_number(account_number)

            if not account:
                raise ValueError("Account not found")

            new_balance = account["balance"] + amount

            self.account_repo.update_balance(account["id"], new_balance)

            self.transaction_repo.create_transaction(
                account_id=account["id"],
                transaction_type="DEPOSIT",
                amount=amount,
                reference="Cash Deposit"
            )

            logger.info(
                f"Deposit {amount} to {account_number} | new balance: {new_balance}"
            )

            return new_balance

        except Exception as e:
            logger.error(
                f"Deposit failed for {account_number}: {str(e)}"
            )
            raise


    # -----------------------------
    # Withdraw
    # -----------------------------

    def withdraw(self, account_number, amount):

        try:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive")

            account = self.account_repo.get_by_account_number(account_number)

            if not account:
                raise ValueError("Account not found")

            if account["balance"] < amount:
                raise ValueError("Insufficient balance")

            new_balance = account["balance"] - amount

            self.account_repo.update_balance(account["id"], new_balance)

            self.transaction_repo.create_transaction(
                account_id=account["id"],
                transaction_type="WITHDRAW",
                amount=amount,
                reference="Cash Withdrawal"
            )

            logger.info(
                f"Withdraw {amount} from {account_number} | new balance: {new_balance}"
            )

            return new_balance

        except Exception as e:
            logger.error(
                f"Withdraw failed for {account_number}: {str(e)}"
            )
            raise


    # -----------------------------
    # Transfer (Atomic Transaction)
    # -----------------------------

    def transfer(self, sender_acc_no, receiver_acc_no, amount):

        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        if sender_acc_no == receiver_acc_no:
            raise ValueError("Cannot transfer to the same account")

        conn = None

        try:
            conn = get_connection()

            sender = conn.execute(
                "SELECT * FROM accounts WHERE account_number = ?",
                (sender_acc_no,)
            ).fetchone()

            receiver = conn.execute(
                "SELECT * FROM accounts WHERE account_number = ?",
                (receiver_acc_no,)
            ).fetchone()

            if not sender:
                raise ValueError("Sender account not found")

            if not receiver:
                raise ValueError("Receiver account not found")

            if sender["balance"] < amount:
                raise ValueError("Insufficient balance")

            new_sender_balance = sender["balance"] - amount
            new_receiver_balance = receiver["balance"] + amount

            self.account_repo.update_balance(sender["id"], new_sender_balance, conn)

            self.account_repo.update_balance(receiver["id"], new_receiver_balance, conn)  

            self.transaction_repo.create_transaction(
                sender["id"],
                "TRANSFER_OUT",
                amount,
                f"Transfer to {receiver_acc_no}", 
                conn
            )

            self.transaction_repo.create_transaction(
                receiver["id"],
                "TRANSFER_IN",
                amount,
                f"Transfer from {sender_acc_no}",
                conn
            )

            conn.commit()

            logger.info(
                f"Transfer {amount} from {sender_acc_no} to {receiver_acc_no} | "
                f"sender balance: {new_sender_balance} | receiver balance: {new_receiver_balance}"
            )

            return {
                "sender_balance": new_sender_balance,
                "receiver_balance": new_receiver_balance
            }

        except Exception as e:

            if conn:
                conn.rollback()

            logger.error(
                f"Transfer failed {sender_acc_no} -> {receiver_acc_no}: {str(e)}"
            )

            raise

        finally:
            if conn:
                conn.close()

    # -----------------------------
    # Accounts fetch service using Customer_ID
    # -----------------------------

    def get_my_accounts(self, customer_id: int):

        accounts = self.account_repo.get_accounts_by_customer(customer_id)

        return accounts


    # -----------------------------
    # Transactions fetch service using Account_ID
    # -----------------------------

    def get_account_transactions(self, account_id: int):

        return self.transaction_repo.get_transactions_by_account(account_id)