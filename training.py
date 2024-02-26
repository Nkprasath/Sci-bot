# Define libraries
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import regularizers

# define lemmatization which converts words into dictionaries
lemmatizer = WordNetLemmatizer()

# Get the dataset
intents = json.loads(open('intents.json').read())

# Defining empty lists for future use
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# tokenise each word and append to lists
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmatize each word and ignore punctuations
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words)) # sort the words

# dump the processed words and classes to pkl files
classes = sorted(set(classes))
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

# prepare training data with BOW and assign labels using One hot encoding
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)

train_x = np.array([x[0] for x in training]) # contains the bag of words
train_y = np.array([x[1] for x in training]) # contains labels

# Pad sequences to make them of equal length
train_x = pad_sequences(train_x, padding='post')

# Define the model
model = Sequential()
model.add(Dense(256, input_shape=(train_x.shape[1],)))
model.add(BatchNormalization())  # Add Batch Normalization layer
model.add(LeakyReLU(alpha=0.1))  # Use LeakyReLU activation function
model.add(Dropout(0.5))
model.add(Dense(128))
model.add(BatchNormalization())
model.add(LeakyReLU(alpha=0.1))
model.add(Dropout(0.5))
model.add(Dense(len(classes), activation='softmax', kernel_regularizer=regularizers.l2(0.001)))  # Using L2 Regularization to prevent overfitting

sgd = SGD(lr=0.0001, decay=1e-6, momentum=.9)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# saving the model
# 82% accuracy
history = model.fit(train_x, train_y, epochs=700, batch_size=5, verbose=True)
model.save('chatbot_model.model', history)
# print("Done")
