# File: models/context.py
import chatbot


class Context:
    def __init__(self, uid):
        self.uid = uid
        self.conversation = []

    def add_message(self, sender, message):
        self.conversation.append({sender: message})

    def get_messages(uid):
        try:
            if uid == '':
                context = chatbot.context
                # return all of the context
                return context
            else:
                context = chatbot.context[uid]
                if context is not None:
                    return context
        except Exception as e:
            print('Exception type:', type(e).__name__)
            print('Exception message:', str(e))
            return None
