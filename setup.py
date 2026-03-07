from database.connection import get_connection

def initialize_database():
    with get_connection() as conn:
        with open("database/schema.sql", "r") as f:
            conn.executescript(f.read())
        conn.commit()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")