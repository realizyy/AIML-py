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
    @staticmethod
    def getUser(uid):
        # Check if the user exists in the dictionary
        if uid in chatbot.users:
            try:
                # return specific user from uid
                user = chatbot.users[uid]
                if user is not None:
                    return user
            except Exception as e:
                print('Exception type:', type(e).__name__)
                print('Exception message:', str(e))
                return None
        else:
            print(f"No user with uid {uid}")
            return None

    # fungsi untuk mereturn semua user
    @staticmethod
    def getUsers():
        try:
            users = chatbot.users
            if users is not None:
                return users
        except Exception as e:
            print('Exception type:', type(e).__name__)
            print('Exception message:', str(e))
            return None