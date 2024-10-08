from functools import lru_cache
import stanza
import spacy_stanza
import xml.etree.ElementTree as ET
import aiml
from fuzzywuzzy import fuzz
import os
import random
from services import order_services, payment_services, chat_services
from models.user import User
from models.context import Context
from controller import user_controller

# Load Stanza's Indonesian model
stanza_nlp = stanza.Pipeline('id', download_method=None) # Load the model using stanza.Pipeline
# Load Spacy's Indonesian model
nlp = spacy_stanza.load_pipeline('id', download_method=None)  # Load the model using spacy_stanza.load_pipeline

kernel = aiml.Kernel()

# Learn from the startup file
kernel.learn("std-startup.xml")
# Respond to load aiml b
kernel.respond("load aiml b")
# Set the name of the bot and the owner
kernel.setBotPredicate("name", "ALICE")
kernel.setBotPredicate("master", "R.a")

# Load AIML patterns dari semua file dalam direktori
aiml_patterns = []
try:
    path = './databot/std-dkampus/'
    for filename in os.listdir(path):
        if filename.endswith('.aiml'):
            tree = ET.parse(path + filename)
            root = tree.getroot()
            for pattern in root.iter('pattern'):
                aiml_patterns.append(pattern.text)

    print('Loaded AIML patterns there are:', len(aiml_patterns), 'patterns')
except Exception as e:
    print('Error while loading aiml patterns:', str(e))

# Initialize the context and users
context = {}
users = {}

# Function to handle the chatbot response with further logic
kernel.setPredicate("check_order_status", order_services.track_order)

#function preprocess input if the input is not match with the aiml pattern
@lru_cache(maxsize=None)
def preprocess_input(input):
    # Tokenisasi dengan Stanza
    print('Doing pre-processing... for:', input)
    doc = stanza_nlp(input)
    tokens = [token.text.lower() for sentence in doc.sentences for token in sentence.words]  # Ambil semua token dan jadikan lowercase
    print('Stanza tokens:', tokens)

    # Pencarian Pola AIML yang Cocok
    try:
        for pattern in aiml_patterns:
            # Tokenisasi pola AIML
            pattern_tokens = [token.text.lower() for sentence in stanza_nlp(pattern).sentences for token in sentence.words]

            # Cek apakah pola hanya terdiri dari satu kata
            # if len(pattern.strip().split()) == 1:
            #     print('Kondisi jika pola hanya terdiri dari satu kata, pattern:', pattern)
            #     if pattern.strip().lower() == input.strip().lower():  # Perbandingan langsung (case-insensitive)
            #         response = kernel.respond(pattern)
            #         return response

            # Cek apakah semua token pola ada dalam input

            # if all(token in tokens for token in pattern_tokens):
            #     # Jika ada kecocokan, kembalikan respons dari AIML
            #     print('Kondisi jika semua token pola ada dalam input, pattern:', pattern)
            #     response = kernel.respond(pattern)
            #     return response

            # Cek dengan fuzzy matching
            if fuzz.ratio(' '.join(tokens), ' '.join(pattern_tokens)) >= 60:  # Ubah threshold sesuai kebutuhan
                print('Kondisi jika ada kecocokan fuzzy, pattern:', pattern, ' Fuzzy ratio:', fuzz.ratio(' '.join(tokens), ' '.join(pattern_tokens)))
                response = kernel.respond(pattern)
                return response
            else:
                print('Fuzzy ratio:', fuzz.ratio(' '.join(tokens), ' '.join(pattern_tokens)))
    except Exception as e:
        print('Error while pre-processing aiml:', str(e))

def chatbot_response(input, uid):
    # if the user is not in the users list, then create a new user
    if uid not in users:
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

    # if the user is not in the context list, then create a new context
    if uid not in context:
        context[uid] = Context(uid)

    # add the input to the user's context
    #context[uid].add_message("user", input)

    # Check the input, if it is a command, then execute the command. Otherwise, process the input with AIML patterns
    try:
        # Kondisi jika user menggunakan chatbot dengan variable user.chatbot == 1 true, jika tidak maka 0
        if users[uid].usebot == '1':
            if input.upper().startswith('CEK STATUS ORDER'):
                order_id = input[17:]
                return order_services.track_order(order_id)
            elif input.upper().startswith('ITEM YANG KURANG'):
                order_id = input[17:]
                return order_services.missing_item(order_id)
            elif input.upper().startswith('PESANAN SALAH'):
                order_id = input[14:]
                return order_services.wrong_order(order_id)
            elif input.upper().startswith('REFUND ORDER'):
                order_id = input[13:]
                return payment_services.refund(order_id)
            elif input.upper().startswith('EXIT' or 'KELUAR' or 'BOT' or 'STOP' or 'ADMIN'):
                users[uid].usebot = '0'
                return "Kamu terhubung dengan admin, bot akan berhenti."
            else:
                # Check the input with AIML patterns
                response = kernel.respond(input)
                if response == 'Maaf, saya tidak mengerti maksud Anda.' or response == 'Maaf, saya tidak mengerti maksud Anda. Silahkan ulangi pertanyaan Anda.' or response == 'Maaf, saya tidak mengerti maksud Anda. Silahkan ulangi pertanyaan Anda dengan kata-kata yang lebih jelas.':
                    print("[Pattern not found! Using pre-processing...]")
                    response = preprocess_input(input)
                    if response:
                        return response
                    else:
                        print("[No response found!]")
                        randomResponse = ['Maaf, saya tidak mengerti maksud Anda.', 'Maaf, saya tidak mengerti maksud Anda. Silahkan ulangi pertanyaan Anda.', 'Maaf, saya tidak mengerti maksud Anda. Silahkan ulangi pertanyaan Anda dengan kata-kata yang lebih jelas.']
                        return randomResponse[random.randint(0, 2)]
                else:
                    return response
    except Exception as e:
        print("Error:", str(e))
        return "Maaf, terjadi kesalahan dalam sistem. Silahkan coba beberapa saat lagi."
