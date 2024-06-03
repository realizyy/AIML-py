from database import db_connection

db = db_connection.create_connection()

def getUser(user_id):
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result
    except Exception as e:
        return None
