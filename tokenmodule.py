# token_module.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "campus_quickeat.db"

def generate_token(order_id: int) -> str:
    """
    Generate token in the format T-001 based on order_id.
    """
    return f"T-{order_id:03d}"


def attach_token(order_id: int):
    """
    Updates the order record to ADD the token (pickup_code field)
    after the student places the order.
    """
    token = generate_token(order_id)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders
        SET pickup_code = ?
        WHERE id = ?
    """, (token, order_id))

    conn.commit()
    conn.close()

    return token


if __name__ == "__main__":
    print("Token generator test:")
    print(generate_token(1))
