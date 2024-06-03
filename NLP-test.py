import stanza
import spacy_stanza

# Load Stanza's Indonesian model
stanza_nlp = stanza.Pipeline('id')  # Load the model using stanza.Pipeline

# Load Spacy's Indonesian model
nlp = spacy_stanza.load_pipeline('id')  # Load the model using spacy_stanza.load_pipeline

# Process Indonesian text
doc = nlp("Saya pesan makanan, tapi makanan tersebut belum sampai")
for sent in doc.sents:
    for word in sent:
        print(f"{word.text:{12}}{word.pos_:{10}}{word.dep_:{10}}{word.head.text}")
