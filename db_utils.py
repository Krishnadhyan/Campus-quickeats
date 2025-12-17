import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "campus_quickeat.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_canteens():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, college, name FROM canteens;")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_menu_for_canteen(canteen_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, price
        FROM menu_items
        WHERE canteen_id = ?;
    """, (canteen_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def ensure_user(pesu_id, name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE pesu_id = ?;", (pesu_id,))
    row = cur.fetchone()

    if row:
        conn.close()
        return row["id"]

    cur.execute("""
        INSERT INTO users (pesu_id, name)
        VALUES (?, ?);
    """, (pesu_id, name))

    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def create_order(user_id, menu_item, canteen, pickup_code, placed_at):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (
            user_id, menu_item, canteen, pickup_code,
            placed_at, status
        )
        VALUES (?, ?, ?, ?, ?, 'pending');
    """, (user_id, menu_item, canteen, pickup_code, placed_at))

    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id


def get_pending_orders():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            o.id AS order_id,
            u.name AS student_name,
            u.pesu_id AS pesu_id,
            o.menu_item,
            o.canteen,
            o.status,
            o.placed_at,
            o.pickup_code
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.status = 'pending'
        ORDER BY o.placed_at ASC;
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def update_order_status(order_id, new_status):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET status = ?
        WHERE id = ?;
    """, (new_status, order_id))

    conn.commit()
    conn.close()


def get_order_status(order_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT status FROM orders WHERE id = ?;", (order_id,))
    row = cur.fetchone()

    conn.close()
    if row:
        return row["status"]
    return None
