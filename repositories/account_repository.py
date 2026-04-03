from database.connection import get_connection
from datetime import datetime


class AccountRepository:

    def create_account(self, customer_id: int, account_type: str):

        account_number = self.generate_account_number()

        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO accounts
                (customer_id, account_number, account_type, balance, status)
                VALUES (?, ?, ?, 0, 'active')
                """,
                (customer_id, account_number, account_type)
            )

            conn.commit()

        return account_number


    def get_by_account_number(self, account_number):

        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM accounts WHERE account_number = ?",
                (account_number,)
            ).fetchone()


    def get_accounts_by_customer(self, customer_id: int):

        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, account_number, account_type, balance, status, created_at
                FROM accounts
                WHERE customer_id = ?
                """,
                (customer_id,)
            )

            return cursor.fetchall()

    def update_balance(self, account_id, new_balance, conn=None):

        if conn is None:
            conn = get_connection()
            close_conn = True
        else:
            close_conn = False

        conn.execute(
            "UPDATE accounts SET balance = ? WHERE id = ?",
            (new_balance, account_id)
        )

        if close_conn:
            conn.commit()
            conn.close()


    def generate_account_number(self):

        with get_connection() as conn:
            row = conn.execute(
                "SELECT MAX(id) as max_id FROM accounts"
            ).fetchone()

        next_id = (row["max_id"] or 0) + 1

        year = datetime.now().year

        return f"GBK-{year}-{next_id:06d}"


    def get_account_by_id(self, account_id: int):

        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM accounts WHERE id = ?",
                (account_id,)
            ).fetchone()