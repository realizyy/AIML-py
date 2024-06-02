# File: models/context.py
class Context:
    def __init__(self, uid):
        self.uid = uid
        self.awaiting_order_id = False
        self.options = {}