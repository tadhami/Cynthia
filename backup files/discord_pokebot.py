import json
import discord.abc
import os 
import string
import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
import pokebot_parser
import output_generator

# Installation: needed to download anaconda, create an environment called tf, and in it
# did nltk.download() in the terminal
# then I downloaded the things that weren't properly downloading, like punkt and omw 1.4
# then it worked
# NOTE: for intents[1]: set up a conditional and have a list of pokemon game names. if any of those words
# or key words (probably faster?) is in that list, then no need to ask a follow up question. if there 
# is no name in the input, then ask a follow-up question ("Which game would you like to check?")

#NOTE: for intents[0]: set up a conditional that asks for the region (if a region isn't specified, or rather it's either national, a region is there, no region is there and not national)

nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")

output = ''
dex_num_output = '7'
strength_output = ''
weakness_output = ''
evolution_output = ''
type_output = ''
move_output = 'ZA WARUDO'
height_output = ''
weight_output = ''
all_output = ''
classification_output = ''
list_output = ''

'''

'''
data = {"intents": [
    {"tag": "hi",
     "patterns": ["hi!", "what's up?", "hello!", "sup", "what's good", "hey there", "howdy"],
     "responses": ["Hi! How's it going? If you aren't sure where to go from here, try asking me a question! And if you don't know what to ask, you can try asking me what information I can give you or what I can do"],
     },
     {"tag": "features",
     "patterns": ["what are things you can do?", "what sorts of features do you have?", "what can you tell me?", "what information can you give me?", "what information can you tell me?", "What are you capable of?", "Describe what you can do", "How capable are you?", "Tell me about what you can do", "What features do you contain?", "Can you tell me how to {0}?"],
     "responses": ["I can list out my features, can tell you a bunch of things related to specific pokemon (pokedex number, game-specific location, evolution criteria, strengths, weaknesses, types, classification, all the information I have on a particular pokemon, height, and weight), and can give you the location of any item in any game!"],
     },
     {"tag": "list_out",
     "patterns": ["list out all your features", "give me a list of all your features", "list"],
     "responses": [list_output],
     },
    {"tag": "dex_number",
     "patterns": ["what's {0} pokedex number?", "{0} pokedex number", "{0} dex number", "{0} national dex number", "{0} pokedex nbr"],
     "responses": [dex_num_output],
     },
    {"tag": "location",
     "patterns": ["Where to catch Rookidee in Shield", "where do you catch {0} in {0}?", "where do you catch {0} in pokemon {0}?", "how to catch {0} in {0}?", "where to find {0} in {0}?", "where to catch {0} in {0}?", "where to catch {0} in pokemon{0}?" , "where to catch {0}?", "where to get {0} in {0}", "where to find {0} in {0}", "how to get {0} in {0}", "{0} location in {0}", "{0} location"],
     "responses": [output]
     },
    {"tag": "level_evolve",
     "patterns": ["{0} what level does {0} evolve?",
                  "{0} when does {0} evolve into {0}?", "{0} what level does {0} evolve into {0}?", "{0} how to evolve {0}", "{0} how to evolve {0} in pokemon {0}"],
     "responses": [evolution_output]
     },
    {"tag": "strengths",
     "patterns": ["what's {0} good against?", "what's {0} super effective on?", "what are {0} strengths?", "{0} strengths"],
     "responses": [strength_output]
     },
    {"tag": "weaknesses",
     "patterns": ["what's {0} weak against?", "what's {0} weak to?", "what are {0}'s weaknesses?", "{0} weaknesses",],
     "responses": [weakness_output]
     },
     {"tag": "type",
     "patterns": ["what's {0} type?", "what type is {0}?", "what is {0}'s type?", "{0} type ",],
     "responses": [type_output]
     },
     {"tag": "height",
     "patterns": ["how tall is {0}?", "what's {0} height?", "{0} height", "how short is {0}?",],
     "responses": [height_output]
     },
     {"tag": "weight",
     "patterns": ["what's {0} weight?", "how heavy is {0}?", "{0} weight", "how light is {0}?",],
     "responses": [weight_output]
     },
     {"tag": "classification",
     "patterns": ["what kind of pokemon is {0}", "classification {0}", "what is {0} classified as?", "{0} classification?", "describe {0} for me", "classify {0} for me"],
     "responses": [classification_output]
     },
     {"tag": "all info",
     "patterns": ["tell me everything about {0}", "tell me everything there is to know about {0}?", "give me all the info about {0}", "can you give me all the information you have about {0}?", "can you tell me all you can about {0}?", "everything about {0}", "everything you have about {0}", "tell me all you know about {0}"],
     "responses": [all_output]
     },
     {"tag": "move learning",
     "patterns": ["when does {0} learn {0}?", "what level does {0} learn {0}?", "level learn {0}", "when does {0} learn the move {0}"],
     "responses": [move_output]
     }, 
     {"tag": "goodbye",
     "patterns": ["goodbye!", "bye!", "bye", "cya", "see you later"],
     "responses": ["Bye!! Hopefully I was able to answer all your questions!"]
     },
     {"tag": "ucl",
     "patterns": ["ratio, catch this ratio"],
     "responses": ["Warra UCL for man city"]
     }
]}
# initializing lemmatizer to get stem of words
lemmatizer = WordNetLemmatizer()
# Each list to create
words = []
classes = []
doc_X = []
doc_y = []
# Loop through all the intents
# tokenize each pattern and append tokens to words, the patterns and
# the associated tag to their associated list
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        doc_X.append(pattern)
        doc_y.append(intent["tag"])

    # add the tag to the classes if it's not there already
    if intent["tag"] not in classes:
        classes.append(intent["tag"])
# lemmatize all the words in the vocab and convert them to lowercase
# if the words don't appear in punctuation
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
# sorting the vocab and classes in alphabetical order and taking the # set to ensure no duplicates occur
words = sorted(set(words))
classes = sorted(set(classes))

# list for training data
training = []
out_empty = [0] * len(classes)
# creating the bag of words model
for idx, doc in enumerate(doc_X):
    bow = []
    text = lemmatizer.lemmatize(doc.lower())
    for word in words:
        bow.append(1) if word in text else bow.append(0)
    # mark the index of class that the current pattern is associated
    # to
    output_row = list(out_empty)
    output_row[classes.index(doc_y[idx])] = 1
    # add the one hot encoded BoW and associated classes to training
    training.append([bow, output_row])
# shuffle the data and convert it to an array
random.shuffle(training)
training = np.array(training, dtype=object)
# split the features and target labels
train_X = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

# defining some parameters
input_shape = (len(train_X[0]),)
output_shape = len(train_y[0])
epochs = 200
# the deep learning model
model = Sequential()
model.add(Dense(128, input_shape=input_shape, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(output_shape, activation="softmax"))
adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)
model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=["accuracy"])
print(model.summary())
model.fit(x=train_X, y=train_y, epochs=200, verbose=1)


def clean_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens


def bag_of_words(text, vocab):
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens:
        for idx, word in enumerate(vocab):
            if word == w:
                bow[idx] = 1
    return np.array(bow)


def pred_class(text, vocab, labels):
    bow = bag_of_words(text, vocab)
    result = model.predict(np.array([bow]))[0]
    thresh = 0.2
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list


def get_response(intents_list, intents_json, message):
    tag = intents_list[0]
    print("tag is: ", tag)
    try:
        intents_json = output_generator.json_modifier(intents_json, tag, message)
    except:
        pass 
    list_of_intents = intents_json["intents"]
    result = 0
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result

# running the chatbot
def chat_resp(message):
    intents = pred_class(message, words, classes)
    result = get_response(intents, data, message)
    return result 

# https://towardsdatascience.com/how-to-build-your-own-ai-chatbot-on-discord-c6b3468189f4

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        else:
           inp = message.content
           bot_response = chat_resp(inp)
           if client.user.mention in message.content:
            await message.channel.send(bot_response.format(message))

client = MyClient()
client.run(token)