from database.connection import get_connection

class AccountRepository:

    def create_account(self, customer_id):

        with get_connection() as conn:

            last_account = conn.execute(
                "SELECT account_number FROM accounts ORDER BY id DESC LIMIT 1"
            ).fetchone()

            if last_account:
                last_number = int(last_account["account_number"].replace("ACC", ""))
                new_number = last_number + 1
            else:
                new_number = 1001   # first account

            account_number = f"ACC{new_number}"

            conn.execute(
                """
                INSERT INTO accounts (customer_id, account_number, account_type, balance, status)
                VALUES (?, ?, 'SAVINGS', 0, 'ACTIVE')
                """,
                (customer_id, account_number)
            )

            conn.commit()

            return account_number

    def get_by_account_number(self, account_number):

        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM accounts WHERE account_number = ?",
                (account_number,)
            ).fetchone()


    def update_balance(self, account_id, new_balance):

        with get_connection() as conn:
            conn.execute(
                "UPDATE accounts SET balance = ? WHERE id = ?",
                (new_balance, account_id)
            )
            conn.commit()