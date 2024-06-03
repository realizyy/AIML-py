from flask import Flask, request
from flask_restful import Resource, Api
from chatbot import chatbot_response
from chatbot import context
import time

app = Flask(__name__)
api = Api(app)

# Temporary data from users

class ChatBot(Resource):
    def post(self):
        uid = request.get_json().get('uid', '')
        user_input = request.get_json().get('message', '')
        bot_response = chatbot_response(user_input, uid)
        #log the user input and bot response
        print(f"User[{uid}] Say: {user_input} \nBot Say: {bot_response}")
        # print the return all the messages in the context
        print('Log context:\n', context[uid].get_messages())
        return {'message': bot_response}

    def get(self):
        return {'message': 'Hello, World!'}

class Ping(Resource):
    def get(self):
        start_time = time.time()
        return {'message': 'Pong! ' + 'Response time: ' + str(round(time.time() - start_time, 2)) + 's'}


# Routes for the API
api.add_resource(ChatBot, '/chat')
api.add_resource(Ping, '/ping')