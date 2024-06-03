from database import db_connection

db = db_connection.create_connection()

def track_order(order_id):
    # logic to track order
    cursor = db.cursor()
    # the order id is 8808ced4021356bd60f89af5c2e5311e46e6866947648f7f960fdecacafc0ea6
    #then the format what cust see is #TRX+uppercase(10 first char of order id)
    #so the user will input #TRX8808CED40
    # find the order id in the database with the format 8808CED40 from the input
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
            return f"Order dengan ID {order_id} sedang dalam proses"

def missing_food(order_id):
    # logic to handle missing food
    # this function will be called when the user send the topic "MAKANAN ADA YANG KURANG" to the chatbot
    # the chatbot will ask the order id and the item that is missing this the return of response of bot to the user
    # <template>Maaf, makanan ada yang kurang? Silahkan berikan order ID Anda.</template>
    cursor = db.cursor()
    trimmed_order_id = order_id[4:14].upper()
    cursor.execute(f"SELECT * FROM histories WHERE order_id LIKE '%{trimmed_order_id}%'")
    result = cursor.fetchone()
    if result is None:
        return "Order tidak ditemukan"
    else:
        #print(result)
        #The structure of the result is (id(history), user_id, cour_id, umkm_id, item, harga, ongkir, jarak, status, bukti, bukti_akhir, alasan, order_id, created_at, updated_at)
        return (f"Berikut merupakan item yang Anda pesan: \n{result[4]}.\nBisa tolong sebutkan item yang kurang?")

def handle_wrong_food():
    # logic to handle wrong food
    return "Handling wrong food..."

def contact_customer_service():
    # logic to contact customer service
    return "Contacting customer service..."