from db_utils import *
import random
from datetime import datetime
import time


def generate_pickup_code():
    return random.randint(100000, 999999)


def student_app():

    print("\n===== STUDENT ORDERING SYSTEM =====")

    while True:
        print("\nChoose an option:")
        print("1. Place new order")
        print("2. Check order status")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            place_order()

        elif choice == "2":
            order_id = input("Enter your Order ID: ").strip()
            if not order_id.isdigit():
                print("Invalid Order ID!")
                continue

            status = get_order_status(int(order_id))
            if status is None:
                print("❌ Order not found!")
            else:
                print(f"📢 Current status: {status.upper()}")

        elif choice == "3":
            print("Goodbye!")
            break
        elif status =="READY":
            print(f"Order {order_id} ready to pick up")

        else:
            print("Invalid choice. Try again.")


def place_order():
    canteens = get_canteens()

    print("\nAvailable Canteens:")
    for idx, c in enumerate(canteens, start=1):
        print(f"{idx}. {c['name']} ({c['college']})")

    canteen_choice = int(input("Enter Canteen Number: "))
    canteen_id = canteens[canteen_choice - 1]["id"]
    canteen_name = canteens[canteen_choice - 1]["name"]

    menu = get_menu_for_canteen(canteen_id)
    print("\nMenu:")
    for item in menu:
        print(f"{item['id']}. {item['name']} - ₹{item['price']}")

    menu_id = int(input("Select Menu Item ID: "))
    selected_item = None

    for m in menu:
        if m["id"] == menu_id:
            selected_item = m
            break

    pesu_id = input("Enter your PESU ID: ")
    name = input("Enter your Name: ")

    user_id = ensure_user(pesu_id, name)

    pickup_code = generate_pickup_code()
    placed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_id = create_order(
        user_id=user_id,
        menu_item=selected_item["name"],
        canteen=canteen_name,
        pickup_code=pickup_code,
        placed_at=placed_at
    )

    print("\n🎉 Order Placed Successfully!")
    print("Your Order ID:", order_id)
    print("Pickup Code:", pickup_code)


if __name__ == "__main__":
    student_app()
