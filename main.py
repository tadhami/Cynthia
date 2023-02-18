from io import BytesIO
import json

from click import pass_context
import discord.abc
from discord.ext import commands 
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

# import aiohttp 
# import io

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

output = ''
dex_num_output = '7'
strength_output = ''
weakness_output = ''
evolution_output = ''
type_output = ''
move_output = ''
height_output = ''
weight_output = ''
all_output = ''
classification_output = ''
list_output = ''
pogo_all_output = ''
pogo_season_output = ''
pogo_event_output = ''
raids_output = ''
pogo_next_research_breakthrough_output = ''
pogo_current_research_breakthrough_output = ''
pogo_next_spotlight_hour_output = ''
pogo_current_spotlight_hour_output = ''
pogo_next_month_comm_day_output = ''
pogo_current_month_comm_day_output = ''
moves_effect_output = ''
can_learn_move_output = ''
when_learn_move_gen_output = ''
when_learn_move_game_output = ''
when_learn_move_all_output = ''
shiny_img_output = ''
normal_img_output = ''


'''

'''
data = {"intents": [
    {"tag": "hi",
     "patterns": ["hi!", "what's up?", "hello!", "sup", "what's good", "hey there", "howdy"],
     "responses": ["Hi! How's it going? If you aren't sure where to go from here, try asking me a question! And if you don't know what to ask, you can try asking me what information I can give you or what I can do"],
     },
     {"tag": "features",
     "patterns": ["what are things you can do?", "what sorts of features do you have?", "what can you tell me?", "what information can you give me?", "what information can you tell me?", "What are you capable of?", "Describe what you can do", "How capable are you?", "Tell me about what you can do", "What features do you contain?", "Can you tell me how to {0}?"],
     "responses": ["I can list out my features, can tell you a bunch of things related to specific pokemon (pokedex number, game-specific location, evolution criteria, strengths, weaknesses, types, classification, all the information I have on a particular pokemon, height, and weight), can give you the location of any item in any game, and can tell you a bunch of Pokemon Go info like next and current: mega raids, 5-star raids, research breakthroughs, spotlight hours, community days, raid hours, and events"],
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
     {"tag": "goodbye",
     "patterns": ["goodbye!", "bye!", "bye", "cya", "see you later"],
     "responses": ["Bye!! Hopefully I was able to answer all your questions!"]
     },
     {"tag": "ucl",
     "patterns": ["ratio, catch this ratio"],
     "responses": ["Warra UCL for man city"]
     },
     {"tag": "pogo_all_spawns",
     "patterns": ["what pokemon are out in pokemon go right now?", "which pokemon are in pogo right now?", "which pokemon are active in pokemon go right now?", "pokemon Go current pokemon", "pokemon currently available in Pokemon Go", "Which pokemon are spawning in Pokemon Go right now?", "pokemon spawning in pokemon Go"],
     "responses": [pogo_all_output]
     },
     {"tag": "pogo_season_spawns",
     "patterns": ["which pokemon are spawning this season in pogo?", "which pokemon are out this season in pokemon Go?", "what is the season right now in pokemon Go?", "what pokemon are available this season in pogo?", "what pokemon are available this season in pokemon Go?", "pokemon Go current season", "pogo current season"],
     "responses": [pogo_season_output]
     },
     {"tag": "pogo_event_spawns",
     "patterns": ["which pokemon are spawning this event in pogo?", "which pokemon are out this event in pokemon Go?", "what is the event right now in pokemon Go?", "what pokemon are available this event in pogo?", "what pokemon are available this event in pokemon Go?", "pokemon Go current event pokemon", "pokemon Go current event", "current pogo event"],
     "responses": [pogo_event_output]
     }, 
     {"tag": "raids",
     "patterns": ["what's appearing in {0} star raids right now?", "What's appearing in mega raids right now?", "What's in raids next?", "What's in mega raids next?", "What's in five-star raids next?"],
     "responses": [raids_output]
     }, 
     {"tag": "pogo_next_research_breakthrough",
     "patterns": ["next research breakthrough pokemon Go", "what research breakthrough is in pokemon Go next?", "What is the next research breakthrough in pogo?", "what is the research breakthrough next month in pokemon Go?", "next research breakthrough pokemon Go"],
     "responses": [pogo_next_research_breakthrough_output]
     },
     {"tag": "pogo_current_research_breakthrough",
     "patterns": ["current research breakthrough pokemon Go", "what research breakthrough is in pokemon Go right now?", "What research breakthrough is in pogo?", "what is the research breakthrough this month in pokemon Go?", "current research breakthrough pokemon Go"],
     "responses": [pogo_current_research_breakthrough_output]
     },
     {"tag": "pogo_next_spotlight_hour",
     "patterns": ["next spotlight hour pokemon Go", "what spotlight hour is in pokemon Go next?", "What is the next spotlight hour in pogo?", "what is the spotlight hour next month in pokemon Go?", "next spotlight hour pokemon Go"],
     "responses": [pogo_next_spotlight_hour_output]
     },
     {"tag": "pogo_current_spotlight_hour",
     "patterns": ["current spotlight hour pokemon Go", "what spotlight hour is in pokemon Go right now?", "What spotlight hour is in pogo?", "what is the spotlight hour this month in pokemon Go?", "current spotlight hour pokemon Go"],
     "responses": [pogo_current_spotlight_hour_output]
     },
     {"tag": "pogo_next_month_comm_day",
     "patterns": ["next community day pokemon Go", "next comm day pokemon Go", "what community day is in pokemon Go next?", "What is the next community day in pogo?", "what is the comm day next month in pokemon Go?", "next community day pokemon Go"],
     "responses": [pogo_next_month_comm_day_output]
     },
     {"tag": "pogo_current_month_comm_day",
     "patterns": ["current community day pokemon Go", "what community day is in pokemon Go right now?", "What is this month's community day in pogo?", "what is the spotlight hour this month in pokemon Go?", "current community day pokemon Go"],
     "responses": [pogo_current_month_comm_day_output]
     },
     {"tag": "moves_effect",
     "patterns": ["what does {0} do?", "What is the effect of {0}?", "what does the move {0} do?"],
     "responses": [moves_effect_output]
     }, 
     {"tag": "can_learn_move",
     "patterns": ["Can {0} learn {0}?", "Can {0} learn {0} in gen {0}?"],
     "responses": [can_learn_move_output]
     }, 
     {"tag": "when_learn_move_gen",
     "patterns": ["when does {0} learn {0} in gen {0}?"],
     "responses": [when_learn_move_gen_output]
     }, 
     {"tag": "when_learn_move_game",
     "patterns": ["when does {0} learn {0} in pokemon {0}?", "when does {0} learn {0} in red?", "when does {0} learn {0} in blue?", "when does {0} learn {0} in yellow?", "when does {0} learn {0} in gold?", "when does {0} learn {0} in silver?", "when does {0} learn {0} in crystal?", "when does {0} learn {0} in ruby?", "when does {0} learn {0} in sapphire?", "when does {0} learn {0} in emerald?", "when does {0} learn {0} in firered?", "when does {0} learn {0} in leafgreen?", "when does {0} learn {0} in diamond?", "when does {0} learn {0} in pearl?", "when does {0} learn {0} in platinum?", "when does {0} learn {0} in black?", "when does {0} learn {0} in white?", "when does {0} learn {0} in black 2?", "when does {0} learn {0} in white 2?", "when does {0} learn {0} in pokemon X?", "when does {0} learn {0} in pokemon Y?", "when does {0} learn {0} in omega ruby?", "when does {0} learn {0} in alpha sapphire?", "when does {0} learn {0} in sun?", "when does {0} learn {0} in moon?", "when does {0} learn {0} in ultra sun?", "when does {0} learn {0} in ultra moon?", "when does {0} learn {0} in sword?", "when does {0} learn {0} in shield?", "when does {0} learn {0} in brilliant diamond?", "when does {0} learn {0} in shining pearl?", "when does {0} learn {0} in legends arceus?"],
     "responses": [when_learn_move_game_output]
     },
     {"tag": "send_shiny_pic",
     "patterns": ["What does shiny {0} look like?", "{0} shiny appearance"],
     "responses": [shiny_img_output]
     }, 
     {"tag": "send_normal_pic",
     "patterns": ["What does {0} look like?", "{0} appearance"],
     "responses": [normal_img_output]
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
    global tag_global 
    tag_global = tag 
    print("tag is: ", tag)
    try:
        intents_json = output_generator.json_modifier(intents_json, tag, message)
    except:
        pass
    list_of_intents = intents_json["intents"]
    result = 0
    for i in list_of_intents:
        if i["tag"] == tag:
            print("get_response : ", i) 
            result = random.choice(i["responses"])
            print("result is: ", result)
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
bot = commands.Bot(command_prefix="$", self_bot=False)

@bot.event
async def on_ready():
    print("Online")
    
@bot.event
async def on_message(message):
    # don't want bot to reply to itself
    if message.author.id == bot.user.id:
        return
    else:
        inp = message.content
        bot_response = chat_resp(inp)
        if bot.user.mention in message.content:
            if (tag_global == 'send_shiny_pic'):
                pokemon_name = pokebot_parser.pokemon_name_extractor(inp).lower()
                image = pokebot_parser.get_pokemon_image(pokemon_name, True)
                bytes = BytesIO()
                image.save(bytes, format = "PNG")
                bytes.seek(0)
                await message.reply(bot_response.format(message), file = discord.File(fp = bytes, filename = 'image.png'))
            elif (tag_global == 'send_normal_pic'):
                pokemon_name = pokebot_parser.pokemon_name_extractor(inp).lower()
                image = pokebot_parser.get_pokemon_image(pokemon_name, False)
                bytes = BytesIO()
                image.save(bytes, format = "PNG")
                bytes.seek(0)
                await message.reply(bot_response.format(message), file = discord.File(fp = bytes, filename = 'image.png'))
            else:
                await message.reply(bot_response.format(message))
    await bot.process_commands(message)

@bot.command()
async def status(ctx):
    await ctx.reply(f'{"Currently online"}, {ctx.author.name}')

@bot.command()
async def list(ctx):
    features = "- Tell you a pokemon's pokedex number\n- Tell you a pokemon's specific in-game location\n- Tell you a pokemon's evolution criteria\n- Tell you a pokemon's strengths\n- Tell you a pokemon's weaknesses\n- Tell you a pokemon's type\n- Tell you a pokemon's height\n- Tell you a pokemon's weight\n- Tell you a pokemon's classification\n- Tell you all I know about a pokemon\n- Tell you the location of any item in any game\n- For Pokemon Go I can tell you the next and current: 5-star raids, mega raids, community days, research breakthroughs, events, current spawns, spotlight hours, and raid hours"
    await ctx.reply(f'{features}')

bot.run(token)