from database import db_connection

db = db_connection.create_connection()

def handler_chat(user_id, message):
    #For firebase, we can use the user_id to get the user's name
    return "Handler chat ..."

def handler_exit_chatbot(user_id):
    #For firebase, we can use the user_id to get the user's name
    return "Chatbot berhenti, kamu akan dialihkan untuk berbicara dengan customer service/admin kami."