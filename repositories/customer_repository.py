from database.connection import get_connection

class CustomerRepository:

    def create_customer(self, full_name, email, phone):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO customers (full_name, email, phone) VALUES (?, ?, ?)",
                (full_name, email, phone)
            )
            conn.commit()
            return cursor.lastrowid

    def get_by_email(self, email):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM customers WHERE email = ?",
                (email,)
            ).fetchone()
            
    def get_customer_by_id(self, customer_id: int):
        with get_connection() as conn:
            return conn.execute(
                "SELECT id, full_name, email, phone, created_at FROM customers WHERE id=?",
                (customer_id,)
            ).fetchone()