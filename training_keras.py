import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy as np
import random
import json

from keras.models import Sequential
from keras.layers import Dense

# Load intents from JSON
with open('data/intents.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)


# Function to generate n-grams from a string
def ngrams(text, n):
    tokens = text.split(' ')
    ngrams_list = []
    for i in range(len(tokens) - n + 1):
        ngram = ' '.join(tokens[i:i+n])
        ngrams_list.append(ngram)
    return ngrams_list


# Preprocess the data
words = []
classes = []
documents = []
ignore_words = ['à', 'ừ', '!', '?', ',', 'dạ', 'vâng', '"', '(', ')']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique stemmed words", words)
'''
# Create training data
training = []
output = []

output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])
'''
training = []
output = []

output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append(bag + output_row)  # Combine bag and output_row into a single list

random.shuffle(training)
training = np.array(training, dtype=np.float32)  # Set the data type to float32

train_x = training[:, :len(words)]
train_y = training[:, len(words):]
# Convert train_x and train_y to numpy arrays
train_x = np.array(train_x)
train_y = np.array(train_y)

# Define the model
model = Sequential()
model.add(Dense(8, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(train_x, train_y, epochs=1000, batch_size=8, verbose=1)

# Save the model
model.save('models/model.keras')
import pickle
# Save the training data
data = {'words': words, 'classes': classes, 'train_x': train_x, 'train_y': train_y}
with open("models/training_data", "wb") as file:
    pickle.dump(data, file)
