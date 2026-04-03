from database.connection import get_connection

def get_customer_id_by_user(user_id: int):

    with get_connection() as conn:

        cursor = conn.execute(
            "SELECT customer_id FROM users WHERE id=?",
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            raise Exception("User not found")

        return row["customer_id"]