import stanza
import spacy_stanza
import xml.etree.ElementTree as ET
import aiml
import os

kernel = aiml.Kernel()

# Learn from the startup file
kernel.learn("std-startup.xml")
# Respond to load aiml b
kernel.respond("load aiml b")
# Set the name of the bot and the owner
kernel.setBotPredicate("name", "ALICE")
kernel.setBotPredicate("master", "R.a")

# Load Stanza's Indonesian model
stanza_nlp = stanza.Pipeline('id', download_method=None) # Load the model using stanza.Pipeline

# Load Spacy's Indonesian model
nlp = spacy_stanza.load_pipeline('id', download_method=None)  # Load the model using spacy_stanza.load_pipeline

# Load AIML patterns dari semua file dalam direktori
aiml_patterns = []
def load_aiml_patterns():
    path = './databot/std-dkampus/'
    for filename in os.listdir(path):
        if filename.endswith('.aiml'):
            tree = ET.parse(path + filename)
            root = tree.getroot()
            for pattern in root.iter('pattern'):
                aiml_patterns.append(pattern.text)
        print('Loaded AIML patterns from:', filename)

def preprocess_input(input, response=None):
    # 1. Tokenisasi dengan Stanza
    print('Doing pre-processing... for:', input)
    doc = stanza_nlp(input)
    tokens = [token.text.lower() for sentence in doc.sentences for token in sentence.words]  # Ambil semua token dan jadikan lowercase

    # 2. Pencarian Pola AIML yang Cocok
    try:
        for pattern in aiml_patterns:
            # Tokenisasi pola AIML
            pattern_tokens = [token.text.lower() for sentence in stanza_nlp(pattern).sentences for token in sentence.words]

            # Cek apakah pola hanya terdiri dari satu kata
            if len(pattern.strip().split()) == 1:
                if pattern.strip().lower() == input.strip().lower():  # Perbandingan langsung (case-insensitive)
                    response = kernel.respond(pattern)
                    return response

            # Cek apakah semua token pola ada dalam input
            if all(token in tokens for token in pattern_tokens):
                # Jika ada kecocokan, kembalikan respons dari AIML
                response = kernel.respond(pattern)
                return response
        print('Stanza tokens:', tokens)
    except Exception as e:
        print('Error while pre-processing aiml:', str(e))

    # 3. Pencocokan dengan SpaCy (opsional)
    if not response:  # Jika belum ditemukan respons, gunakan SpaCy
        spacy_doc = nlp(input)
        for pattern in aiml_patterns:
            spacy_pattern_doc = nlp(pattern)
            similarity = spacy_doc.similarity(spacy_pattern_doc)
            if similarity > 0.8:  # Atur threshold similarity sesuai kebutuhan
                response = kernel.respond(pattern)
                return response
    #log the process
    print('Spacy:', spacy_doc)
    # 4. Jika tidak ada kecocokan, kembalikan None
    return None

# Main function untuk menginputkan pesan dan mendapatkan respons dari chatbot
def main():
    uid = '25'
    load_aiml_patterns()
    while True:
        input_message = input("You: ")
        try:
            response = kernel.respond(input_message)
            if response == 'Maaf, saya tidak mengerti maksud Anda.' or response == 'Maaf, saya tidak mengerti maksud Anda. Silahkan ulangi pertanyaan Anda.' or response == 'Maaf, saya tidak mengerti maksud Anda. Silahkan ulangi pertanyaan Anda dengan kata-kata yang lebih jelas.':
                print("[Pattern not found! Using pre-processing...]")
                response = preprocess_input(input_message)
                if response:
                    print("Bot:", response)
                else:
                    print("[No response found!]")
            else:
                print("Bot:", response)
        except Exception as e:
            print("Error:", str(e))


if __name__ == '__main__':
    main()