from flask import Flask, request
from flask_restful import Resource, Api
from chatbot import chatbot_response
from chatbot import context
from database import db_connection
from database import firebase_connection
from models.user import User as ModelUser
from models.context import Context
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
        #print('Log context:\n', context[uid].get_messages())
        return {'message': bot_response}

    def get(self):
        return {'message': 'Hello, World!'}

class Ping(Resource):
    def get(self):
        start_time = time.time()
        return {'message': 'Pong! ' + 'Response time: ' + str(round(time.time() - start_time, 2)) + 's'}

class testDBConnection(Resource):
    def get(self):
        try:
            db = db_connection.create_connection()
            if db is None:
                return {'message': 'MySQL Database Connection Failed'}
            else:
                try:
                    cursor = db.cursor()
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    total_tables = len(tables)
                except Exception as e:
                    return {'message': 'MySQL Database Connection Failed with error: ' + str(e)}
                return {'message': 'MySQL Database Connection OK!',
                        'host': db.server_host,
                        'port': db.server_port,
                        'user': db.user,
                        'database': db.database,
                        'total_tables': total_tables}
        except Exception as e:
            return {'message': 'MySQL Database Connection Failed with error: ' + str(e)}

class testFBConnection(Resource):
    def get(self):
        try:
            dbfirebase, env_url, env_cred = firebase_connection.create_connection()
            if dbfirebase is None:
                return {'message': 'Firebase Database Connection Failed'}
            else:
                try:
                    ref = dbfirebase.reference('/')
                    data = ref.get()
                    total_data = len(data)
                    print('Total data:', total_data)
                    for key, value in data.items():
                        print(key, value)
                    return {'message': 'Firebase Database Connection OK!',
                            'url': env_url,
                            'credentials': str(env_cred),
                            'total_data': total_data}
                except Exception as e:
                    return {'message': 'Firebase Database Connection Failed with error: ' + str(e)}
        except Exception as e:
            return {'message': 'Firebase Database Connection Failed with error: ' + str(e)}

from flask import request

class testModel(Resource):
    def get(self, uid):
        # Get the uid from the request (query number)/empty for all users
        if 'uid' in request.args:
            uid = request.args['uid']
        else:
            uid = ''
        # Get the user data from the model
        user_data = ModelUser.getUser(uid)
        return {'message': 'Todo to get user data with uid/all users', 'data': str(user_data)}


class testContext(Resource):
    def get(self, uid):
        # Get the uid from the request (query number)/empty for all users
        if 'uid' in request.args:
            uid = request.args['uid']
        else:
            uid = ''
        # Get the context data from the model
        context_data = Context.get_messages(uid)
        return {'message': 'Todo to get context data with uid/all users', 'data': str(context_data)}


# Routes for the API
api.add_resource(ChatBot, '/chat')
api.add_resource(Ping, '/ping')
api.add_resource(testDBConnection, '/testDB')
api.add_resource(testFBConnection, '/testFB')
api.add_resource(testModel, '/testModelUser/<string:uid>')
api.add_resource(testContext, '/testContextUser/<string:uid>')