# qr_generator.py
import qrcode

def generate_qr(order_id: int, token: str):
    """
    Creates QR code PNG file storing order_id + token.
    """
    data = {
        "order_id": order_id,
        "token": token
    }

    file_name = f"qr_order_{order_id}.png"

    qr = qrcode.make(data)
    qr.save(file_name)

    print(f"QR Generated: {file_name}")
    return file_name


if __name__ == "__main__":
    print("Testing QR Generator:")
    generate_qr(10, "T-010")
