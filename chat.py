import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pickle
import numpy as np
import random
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

class Chatbot:
    def __init__(self):
        self.model = None
        self.data = None
        self.stemmer = LancasterStemmer()
        self.words = []
        self.labels = []

    def load_data(self):
        nltk.download('punkt')
        intents_file = 'intents.json'  # Assuming intents.json is in the same directory
        with open(intents_file) as file:
            self.data = json.load(file)

        pickle_file = 'models/data.pickle'
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as f:
                self.words, self.labels, training, output = pickle.load(f)
        else:
            training, output = self.prepare_training_data()
            os.makedirs('models', exist_ok=True)  # Create models directory if it doesn't exist
            with open(pickle_file, 'wb') as f:
                pickle.dump((self.words, self.labels, training, output), f)

        return training, output

    def prepare_training_data(self):
        docs_x = []
        docs_y = []

        for intent in self.data['intents']:
            for pattern in intent['patterns']:
                wrds = nltk.word_tokenize(pattern)
                self.words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent['tag'])

                if intent['tag'] not in self.labels:
                    self.labels.append(intent['tag'])

        self.words = [self.stemmer.stem(w.lower()) for w in self.words if w != '?']
        self.words = sorted(list(set(self.words)))
        self.labels = sorted(self.labels)

        training = []
        output = []
        out_empty = [0 for _ in range(len(self.labels))]

        for x, doc in enumerate(docs_x):
            bag = []
            wrds = [self.stemmer.stem(w) for w in doc]

            for w in self.words:
                bag.append(1) if w in wrds else bag.append(0)

            output_row = out_empty[:]
            output_row[self.labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        return np.array(training), np.array(output)

    def build_model(self, training, output):
        self.model = Sequential([
            Dense(8, input_shape=(len(training[0]),), activation='relu'),
            Dense(8, activation='relu'),
            Dense(len(output[0]), activation='softmax')
        ])

        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        try:
            self.model.load_weights("models/model_weights.h5")
        except:
            self.model.fit(training, output, epochs=3, batch_size=8)
            self.model.save_weights("models/model_weights.weights.h5")

    def bag_of_words(self, s):
        bag = [0 for _ in range(len(self.words))]

        s_words = nltk.word_tokenize(s)
        s_words = [self.stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, W in enumerate(self.words):
                if W == se:
                    bag[i] = 1

        return np.array(bag)

    def classify(self, inp):
        results = self.model.predict(np.array([self.bag_of_words(inp)]))[0]
        results_index = np.argmax(results)
        tag = self.labels[results_index]
        return tag

    def respond(self, tag):
        for intent in self.data['intents']:
            if intent['tag'] == tag:
                responses = intent['responses']
                return random.choice(responses)
        return "I'm sorry, I don't understand that."

    def chat(self):
        training, output = self.load_data()
        self.build_model(training, output)
        print("Start chatting with the bot...(Type 'stop' to quit)")
        while True:
            inp = input("You: ")
            if inp.lower() == 'stop':
                break
            tag = self.classify(inp)
            response = self.respond(tag)
            print(response)

def main():
    chatbot = Chatbot()
    chatbot.chat()

if __name__ == '__main__':
    main()
