import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "campus_quickeat.db"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # USERS table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pesu_id TEXT UNIQUE,
            name TEXT
        );
    """)

    # ORDERS table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            menu_item TEXT,
            canteen TEXT,
            status TEXT,
            placed_at TEXT,
            pickup_code TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)

    # CANTEENS table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS canteens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            college TEXT,
            name TEXT
        );
    """)

    # MENU ITEMS table — NEW COMPOSITE PRIMARY KEY
    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER,
            canteen_id INTEGER,
            name TEXT,
            price REAL,
            PRIMARY KEY (canteen_id, id),
            FOREIGN KEY(canteen_id) REFERENCES canteens(id)
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Database setup complete!")


if __name__ == "__main__":
    setup_database()
