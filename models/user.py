# File: models/user.py
class User:
    def __init__(self, uid):
        self.uid = uid
        self.usebot = '1'  # '1' for 'yes' and '0' for 'no
        self.name = ''
        self.email = ''
        self.np = ''
        self.alamat = ''
        self.orders = []