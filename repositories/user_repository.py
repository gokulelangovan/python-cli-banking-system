from database.connection import get_connection

class UserRepository:
    
    def create_user(self, email, hashed_password):
        with get_connection() as conn:
        
            cursor = conn.execute(
                """
                INSERT INTO users (email, hashed_password)
                VALUES (?, ?)
                """,
                (email, hashed_password)
            )
            
            return cursor.lastrowid
        
    def get_user_by_email(self, email):
        with get_connection() as conn:
        
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            ).fetchone()
            
            return user