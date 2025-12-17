from db_utils import get_pending_orders, update_order_status

def show_pending_orders():
    orders = get_pending_orders()

    if not orders:
        print("\nNo pending orders.\n")
        return

    print("\n=== PENDING ORDERS ===")
    print("Order ID | Token | Item | Canteen | Time")
    print("-------------------------------------------")

    for o in orders:
        print(
            f"{o['order_id']} | "
            f"{o['pickup_code']} | "
            f"{o['menu_item']} | "
            f"{o['canteen']} | "
            f"{o['placed_at']}"
        )

    print("-------------------------------------------")


def main():
    print("🍳 CAMPUS QUICK-EAT — KITCHEN APP")
    print("Commands:")
    print("  ready <order_id>  → mark order as READY")
    print("  refresh           → refresh orders")
    print("  quit              → exit")

    while True:
        show_pending_orders()

        command = input("\nEnter command: ").strip().lower()

        if command == "quit":
            print("Exiting kitchen app.")
            break

        elif command == "refresh":
            continue

        elif command.startswith("ready"):
            parts = command.split()

            if len(parts) != 2 or not parts[1].isdigit():
                print("❌ Usage: ready <order_id>")
                continue

            order_id = int(parts[1])
            update_order_status(order_id, "ready")
            print("\n✅ ORDER READY FOR PICKUP\n")

        else:
            print("❌ Invalid command")


if __name__ == "__main__":
    main()
