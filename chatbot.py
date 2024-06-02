import aiml
from services import order_services, payment_services, chat_services
from models.user import User
from models.context import Context

kernel = aiml.Kernel()

# Learn from the startup file
kernel.learn("std-startup.xml")
# Respond to load aiml b
kernel.respond("load aiml b")
# Set the name of the bot
kernel.setBotPredicate("nameBOT", "ALICE")

# Initialize the context and users
context = {}
users = {}

def process_input(input, uid):
    # If the user is expected to input an order_id, handle it
    if isinstance(context[uid], Context) and context[uid].awaiting_order_id:
        function = getattr(order_services, 'track_order')
        context[uid].awaiting_order_id = False
        return function(input)

    # If the input is a number and it's in the context, call the corresponding function
    if input.isdigit() and isinstance(context[uid], Context) and input in context[uid].options:
        function_name = context[uid].options[input]
        function = getattr(order_services if function_name == 'track_order' else chat_services, function_name)
        if function_name == 'track_order':
            context[uid].awaiting_order_id = True
            return "Silakan masukkan ID pesanan yang ingin Anda lacak."
        else:
            return function(uid)
    return None

def chatbot_response(input, uid):
    global users, context
    # Check if the user exists, if not create a new user and context
    if uid not in users:
        users[uid] = User(uid)
        context[uid] = Context(uid)

    # Check if the user has chosen to not use the bot anymore
    if users[uid].usebot == '0':
        return "Chatbot berhenti, kamu akan dialihkan untuk berbicara dengan customer service/admin kami."

    # Process the input
    processed_input = process_input(input, uid)

    # Otherwise, process the input as usual
    response = kernel.respond(input)
    if "|" in response:
        options = response.split("|")
        # map each option to a function
        option_functions = {
            "MAKANAN BELUM SAMPAI": {
                "1": "track_order",
                "2": "request_refund",
                "3": "contact_customer_service"
            },
            "MAKANAN ADA YANG KURANG": {
                "1": "handle_missing_food",
                "2": "request_refund",
                "3": "contact_customer_service"
            },
            "MAKANAN ADA YANG SALAH": {
                "1": "handle_wrong_food",
                "2": "request_refund",
                "3": "contact_customer_service"
            },
            "EXIT": "handler_exit_chatbot"
        }
        context[uid].options = option_functions[input.upper()]
        return options
    elif response == "":
        return "Maaf, saya tidak mengerti"
    else:
        return response