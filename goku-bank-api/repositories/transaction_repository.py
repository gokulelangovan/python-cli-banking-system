from database.connection import get_connection

class TransactionRepository:

    def create_transaction(self, account_id, transaction_type, amount, reference=None):
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO transactions 
                   (account_id, transaction_type, amount, reference)
                   VALUES (?, ?, ?, ?)""",
                (account_id, transaction_type, amount, reference)
            )
            conn.commit()
            return cursor.lastrowid

    def get_account_transactions(self, account_id):
        with get_connection() as conn:
            return conn.execute(
                """SELECT * FROM transactions 
                   WHERE account_id = ?
                   ORDER BY created_at DESC""",
                (account_id,)
            ).fetchall()