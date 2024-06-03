from database import db_connection
from database import firebase_connection

db = db_connection.create_connection()
dbfirebase = db_connection.create_connection()

def track_order(order_id):
    try:
        # logic to track order
        cursor = db.cursor()
        trimmed_order_id = order_id[4:14].upper()

        #print('order id:', order_id)
        #print ('trimmed order id:', trimmed_order_id)
        cursor.execute(f"SELECT * FROM histories WHERE order_id LIKE '%{trimmed_order_id}%'")
        result = cursor.fetchone()

        if result is None:
            return "Order tidak ditemukan"
        else:
            #print(result)
            #The structure of the result is (id(history), user_id, cour_id, umkm_id, item, harga, ongkir, jarak, status, bukti, bukti_akhir, alasan, order_id, created_at, updated_at)
            if result[8] == 'completed':
                return f"Order dengan ID {order_id} sudah selesai"
            elif result[8] == 'canceled':
                return f"Order dengan ID {order_id} sudah dibatalkan"
            else:
                return f"Order dengan ID {order_id} sedang dalam proses, mohon tunggu 30-45 menit ya!"
    except Exception as e:
        if order_id == '':
            return "Silahkan inputkan order ID Anda, dengan format 'CEK STATUS ORDER (Order ID Kamu)'"
        else:
            return "Error : " + str(e)

def missing_food(order_id):
    try:
        cursor = db.cursor()
        trimmed_order_id = order_id[4:14].upper()
        cursor.execute(f"SELECT * FROM histories WHERE order_id LIKE '%{trimmed_order_id}%'")
        result = cursor.fetchone()
        if result is None:
            return "Order tidak ditemukan"
        else:
            #print(result)
            #The structure of the result is (id(history), user_id, cour_id, umkm_id, item, harga, ongkir, jarak, status, bukti, bukti_akhir, alasan, order_id, created_at, updated_at)
            return f"Berikut merupakan item yang Anda pesan: {result[4]}"
    except Exception as e:
        if order_id == '':
            return "Silahkan inputkan order ID Anda, dengan format 'ITEM YANG KURANG (Order ID Kamu)'"
        else:
            return "Error : " + str(e)

def wrong_food(order_id):
    # logic to handle wrong food
    try:
        cursor = db.cursor()
        trimmed_order_id = order_id[4:14].upper()
        cursor.execute(f"SELECT * FROM histories WHERE order_id LIKE '%{trimmed_order_id}%'")
        result = cursor.fetchone()
        if result is None:
            return "Order tidak ditemukan"
        else:
            #print(result)
            #The structure of the result is (id(history), user_id, cour_id, umkm_id, item, harga, ongkir, jarak, status, bukti, bukti_akhir, alasan, order_id, created_at, updated_at)
            return f"Berikut merupakan item yang Anda pesan: {result[4]}"
    except Exception as e:
        if order_id == '':
            return "Silahkan inputkan order ID Anda, dengan format 'PESANAN SALAH (Order ID Kamu)'"
        else:
            return "Error : " + str(e)

def contact_customer_service():
    # logic to contact customer service
    return "Silahkan hubungi customer service kami di nomor +62 851-6319-3031, WhatsApp : wa.me/6285163193031, Instagram : @dkampus_, atau email : dkampus.ind@gmail.com"