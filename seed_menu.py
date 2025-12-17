import sqlite3
from pathlib import Path

# Use the DB in the same folder as this script
DB_PATH = Path(__file__).resolve().parent / "campus_quickeat.db"

def seed():
    print(f"Using database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1) Ensure tables exist (with corrected menu_items schema)
    print("Ensuring tables 'canteens' and 'menu_items' exist...")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS canteens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            college TEXT,
            name TEXT
        );
    """)

    # IMPORTANT: menu_items now uses manual IDs (restart per canteen)
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

    # 2) Clear old data (clean reseed)
    print("Clearing old data from 'menu_items' and 'canteens'...")

    cur.execute("DELETE FROM menu_items;")
    cur.execute("DELETE FROM canteens;")
    conn.commit()

    # Reset AUTOINCREMENT for canteens
    cur.execute("DELETE FROM sqlite_sequence WHERE name='canteens';")
    conn.commit()

    # 3) Insert canteens
    print("Inserting canteens...")

    canteens = [
        ("PESU RR", "RR Food Court"),
        ("PESU RR", "Hornbill"),
        ("PESU RR", "Momomia"),
    ]

    for college, name in canteens:
        cur.execute(
            "INSERT INTO canteens (college, name) VALUES (?, ?);",
            (college, name)
        )

    conn.commit()

    # Build name -> id mapping
    cur.execute("SELECT id, name FROM canteens;")
    rows = cur.fetchall()
    name_to_id = {name: cid for cid, name in rows}

    # 4) Insert menu items with IDs restarting from 1 for each canteen
    print("Inserting menu items...")

    menu_data = {
        "RR Food Court": [
            ("Masala Dosa", 40.0),
            ("Idli Vada", 25.0),
            ("Fried Rice", 70.0),
            ("Parotha Curry", 70.0),
            ("South Meals", 80.0),
            ("North Meals", 90.0),
        ],
        "Hornbill": [
            ("Coffee", 30.0),
            ("Cold Coffee", 60.0),
        ],
        "Momomia": [
            ("Veg Momos", 60.0),
        ],
    }

    for canteen_name, items in menu_data.items():
        canteen_id = name_to_id[canteen_name]
        item_id = 1  # restart numbering for each canteen

        for name, price in items:
            cur.execute(
                "INSERT INTO menu_items (id, canteen_id, name, price) VALUES (?, ?, ?, ?)",
                (item_id, canteen_id, name, price)
            )
            item_id += 1

    conn.commit()
    conn.close()

    print("✅ Seeding complete! Canteens & menu items added.")

if __name__ == "__main__":
    seed()
