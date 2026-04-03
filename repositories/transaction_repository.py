from datetime import datetime
from database.connection import get_connection


class TransactionRepository:

    def create_transaction(self, account_id, transaction_type, amount, reference=None, conn=None):

        local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if conn is None:
            conn = get_connection()
            close_conn = True
        else:
            close_conn = False

        cursor = conn.execute(
            """
            INSERT INTO transactions
            (account_id, transaction_type, amount, reference, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (account_id, transaction_type, amount, reference, local_time)
        )

        if close_conn:
            conn.commit()
            conn.close()

        return cursor.lastrowid


    def get_transactions_by_account(self, account_id: int):

        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT transaction_type, amount, reference, created_at
                FROM transactions
                WHERE account_id = ?
                ORDER BY created_at DESC
                """,
                (account_id,)
            )

            return cursor.fetchall()