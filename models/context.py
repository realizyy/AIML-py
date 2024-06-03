# File: models/context.py
class Context:
    def __init__(self, uid):
        self.uid = uid
        self.conversation = []

    def add_message(self, sender, message):
        self.conversation.append({sender: message})

    def get_messages(self):
        return self.conversation
