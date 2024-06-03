import aiml
from services import order_services, payment_services, chat_services
from models.user import User
from models.context import Context
from controller import user_controller

kernel = aiml.Kernel()

# Learn from the startup file
kernel.learn("std-startup.xml")
# Respond to load aiml b
kernel.respond("load aiml b")
# Set the name of the bot and the owner
kernel.setBotPredicate("name", "ALICE")
kernel.setBotPredicate("master", "R.a")

# Initialize the context and users
context = {}
users = {}

# Function to handle the chatbot response with further logic
kernel.setPredicate("check_order_status", order_services.track_order)

def chatbot_response(input, uid):
    if uid not in users: #if the user is not in the users list, then create a new user
        users[uid] = User(uid)
        #set the user's information from the database
        # the structure of the user data is (id, name, email, phone, orders[])
        user_data = user_controller.getUser(uid)
        users[uid].name = user_data[1]
        users[uid].email = user_data[2]
        users[uid].phone = user_data[3]
        users[uid].orders = user_data[4]
        #set the user's name to the bot predicate
        kernel.setPredicate("nama_user", users[uid].name)
        kernel.setPredicate("email_user", users[uid].email)
        kernel.setPredicate("phone_user", users[uid].phone)
        # as soon will be add more...

    if uid not in context: #if the user is not in the context list, then create a new context
        context[uid] = Context(uid)

    # check if the input is to check the order status (problems with the orders)
    if input.upper().startswith("CEK STATUS ORDER"):
        # get the next input from the user
        next_input = input[16:].strip()
        # call the check_order_status function with the next input
        response = order_services.track_order(next_input)
        #print(response)
        return response
    elif input.upper().startswith("ITEM YANG KURANG"):
        # get the next input from the user
        next_input = input[16:].strip()
        # call the missing_food function with the next input
        response = order_services.missing_food(next_input)
        #print(response)
        return response
    elif input.upper().startswith("PESANAN SALAH"):
        # get the next input from the user
        next_input = input[16:].strip()
        # call the handle_wrong_food function with the next input
        response = order_services.wrong_food(next_input)
        #print(response)
        return response
    elif input.upper().startswith("REFUND ORDER"):
        # get the next input from the user
        next_input = input[13:].strip()
        # call the refund function with the next input
        response = payment_services.refund(next_input)
        #print(response)
        return response
    else:
        # if the input is not to check the order status, then respond with the chatbot
        response = kernel.respond(input)
        return response

    response = kernel.respond(input)
    return response