# File: models/user.py
import chatbot
class User:
    def __init__(self, uid):
        self.uid = uid
        self.usebot = '1'  # '1' for 'yes' and '0' for 'no
        self.name = ''
        self.email = ''
        self.np = ''
        self.alamat = ''
        self.orders = []

    # fungsi untuk mereturn user berdasarkan uid
    def getUser(uid):
        try:
            if uid == '':
                users = chatbot.users
                # return all of the users
                return users
            else:
                user = chatbot.users[uid]
                if user is not None:
                    return user
        except Exception as e:
            print('Exception type:', type(e).__name__)
            print('Exception message:', str(e))
            return None

    # fungsi untuk mereturn semua user
    def getUsers(self):
        try:
            users = chatbot.users
            if users is not None:
                return users
        except Exception as e:
            print('Exception type:', type(e).__name__)
            print('Exception message:', str(e))
            return None