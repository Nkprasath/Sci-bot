# Importing libraries
from flask import Flask, render_template, request, jsonify
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from difflib import get_close_matches
from tensorflow.keras.models import load_model
from silence_tensorflow import silence_tensorflow
silence_tensorflow()

# Define the flask app
app = Flask(__name__)

# define lemmatization which converts words into dictionaries
lemmatizer = WordNetLemmatizer()

# Get the dataset
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# Get the model
model = load_model('chatbot_model.model')

# Tokenizes the input and lemmatize each word
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Create a BOW with the input by counting each occurrence
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predict the probabilities of the sentence using the trained model
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Randomly retrieve a response from the predicted list of intents
def get_response(intents_list, intents_json):
        try:
            tag = intents_list[0]['intent']
            list_of_intents = intents_json['intents']
            for i in list_of_intents:
                if i['tag'] == tag:
                    result = random.choice(i['responses'])
            return result
        except: return None

# Loads new json file and returns as dictionary
def load_new_knowledge(file_path) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# appends the new knowledge to json
def save_new_knowledge(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Finds the closest match in new knowledge database with the question asked
def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


# Get answer from new knowledge database if available, else return none
def get_answer(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]

# Define route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Defines the process of the chatbot
@app.route('/process', methods=['POST'])
def process():
    # Get the user input from the request
    user_message = request.form['user_input']

    # Predict the intent of the user message
    ints = predict_class(user_message)

    # Check if there's a predefined response for the predicted intent
    response = get_response(ints, intents)

    if response is not None:
        return jsonify({'response': response, 'teach': False})  # Add teach flag with False value
    else:
        # Load knowledge base
        knowledge_base = load_new_knowledge('new_knowledge.json')
        best_match = find_best_match(user_message, [q["question"] for q in knowledge_base["question"]])

        # If match found from new knowledge database, return it
        if best_match is not None:
            answer = get_answer(best_match, knowledge_base)
            if answer is not None:
                return jsonify({'response': answer, 'teach': False})
    return jsonify({'response': "I don't know the answer. Can you teach me?", 'teach': True}) # teach flag is true when the bot does not know the answer

@app.route('/teach', methods=['POST'])
def teach():
    user_message = request.form.get('user_input')  # Get the latest question
    answer = request.form.get('answer') # Get the answer for the latest question

    knowledge_base: dict = load_new_knowledge('new_knowledge.json') # Load the knowledge base as a dictionary
    knowledge_base["question"].append({"question": user_message, "answer": answer}) # append to dictionary and save
    save_new_knowledge('new_knowledge.json', knowledge_base)

    return jsonify({'response': 'I learnt something today!'})

# Define route for about page
@app.route('/about_page')
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)