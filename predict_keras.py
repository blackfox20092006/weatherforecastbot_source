import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
from keras.layers import Input, Dense
from keras.models import Model

import random
import pickle
import json

# Load dữ liệu từ file pickle
data = pickle.load(open("models/training_data", "rb"))
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# Load intents từ file json
with open('data/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

# Xây dựng mô hình
input_layer = Input(shape=(len(train_x[0]),))
hidden_layer = Dense(8, activation='relu')(input_layer)
hidden_layer = Dense(8, activation='relu')(hidden_layer)
output_layer = Dense(len(train_y[0]), activation='softmax')(hidden_layer)

model = Model(inputs=input_layer, outputs=output_layer)
model.compile(optimizer='adam', loss='categorical_crossentropy')

# Load trọng số của mô hình từ file tflearn
model.load_weights('models/model.keras')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)
ERROR_THRESHOLD = 0.25
def classify(sentence):
    results = model.predict(np.array([bow(sentence, words)]))[0]
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list
context = {}
def response(sentence, userID='1', show_details=False):
    results = classify(sentence)
    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    if 'context_set' in i:
                        if show_details:
                            print('context:', i['context_set'])
                        context[userID] = i['context_set']
                    if not 'context_filter' in i or (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details:
                            print('tag:', i['tag'])
                        return random.choice(i['responses'])
            results.pop(0)
