from database import db_connection

db = db_connection.create_connection()

def handler_refund(order_id):
    # logic to refund
    cursor = db.cursor()
    trimmed_order_id = order_id[4:14].upper()

    cursor.execute(f"SELECT * FROM histories WHERE order_id LIKE '%{trimmed_order_id}%'")
    result = cursor.fetchone()
    if result is None:
        return "Order tidak ditemukan"
    else:
        if result[8] == 'completed':
            return f"Order dengan ID {order_id} sudah selesai"
        elif result[8] == 'canceled':
            return f"Order dengan ID {order_id} sudah dibatalkan"
        else:
            cursor.execute(f"UPDATE histories SET status = 'refunded' WHERE order_id LIKE '%{trimmed_order_id}%'")
            db.commit()
            return f"Order dengan ID {order_id} telah direfund"