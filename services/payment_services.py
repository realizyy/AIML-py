from database import db_connection

db = db_connection.create_connection()

def refund(order_id):
    # logic to refund
    try:
        cursor = db.cursor()
        trimmed_order_id = order_id[4:14].upper()

        cursor.execute(f"SELECT * FROM histories WHERE order_id LIKE '%{trimmed_order_id}%'")
        result = cursor.fetchone()
        # print(result)
        if result is None:
            return "Order tidak ditemukan"
        else:
            # The structure of the result is (id(history), user_id, cour_id, umkm_id, item, harga, ongkir, jarak, status, bukti, bukti_akhir, alasan, order_id, created_at, updated_at)
            if result[9] == 'canceled':
                return f"Permintaan refund untuk order dengan ID {order_id} berhasil dilakukan, silahkan masukan nomor handphone yang terdaftar untuk proses refund."

    except Exception as e:
        if order_id == '':
            return "Silahkan inputkan order ID Anda, dengan format 'REFUND ORDER (Order ID Kamu)'"
        else:
            return "Error : " + str(e)

