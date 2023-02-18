import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
import random
import difflib
import item_checker
import numpy as np 
from PIL import Image 
from io import BytesIO


data = pd.read_csv("csv_files/Pokemon_data.csv")
type_data = pd.read_csv("csv_files/types_chart.csv")
type_df = pd.DataFrame(type_data)
type_df.set_index('Attacker/Defender', inplace = True)
types = type_df.columns

def get_pokemon_image(pokemon_name, is_shiny):
    if (is_shiny == True):
        url = 'https://img.pokemondb.net/sprites/home/shiny/2x/' + pokemon_name + '.jpg'
    else:
        url = 'https://img.pokemondb.net/sprites/home/normal/2x/' + pokemon_name + '.jpg'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    # https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    basewidth = 150
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    return img 

def get_item_output(message, game_tuple):
    all_items_tup = item_checker.my_item_checker()
    all_items = all_items_tup[0]
    all_items_lower = all_items_tup[1]
    try:
        message = message.replace(game_tuple[1], "")
        message = message.split(' ')
    except:
        pass
    for i in range(len(message)):
        if (message[i][-3:] == 'ies'):
            message[i] = message[i].replace("ies", "y")
    message = ' '.join(message)
    message = message.replace(" ", "")

    result = [message[i: j] for i in range(len(message))
        for j in range(i + 1, len(message) + 1)]
    substring_list = []
    n = 1
    cutoff = 0.95
    for substring in result: 
        close_matches = difflib.get_close_matches(substring, all_items_lower, n, cutoff)
        if (len(close_matches) > 0):
            substring_list.append(close_matches[0])
    unique, counts = np.unique(substring_list, return_counts=True)
    try:
        if (max(counts) == min(counts)):
            item_of_interest = max(unique, key=len)
        else:
            item_of_interest = unique[np.argmax(counts)]
        idx = all_items_lower.index(item_of_interest)
        final_extracted_item = all_items[idx]
        return final_extracted_item, True
    except:
        final_extracted_item = 'Not Found'
        return final_extracted_item, False

def item_final_output(item, game):
    item_data = pd.read_csv("csv_files/item_locations.csv")
    item_df = pd.DataFrame(item_data)
    item_df.set_index('item_name', inplace=True)
    my_item = item_df.loc[item, game]
    my_item = my_item.replace("{a WEIRD string}", "\n")
    return my_item[:-1]
    # print(my_item)

def pokemon_name_extractor(message):
    message_list = message.split(" ")

    pokemon_name = 'No pokemon name found in input'
    for i in range(len(message_list)):
        word = message_list[i]
        word = word.capitalize()
        word = word.replace("'s", "")
        # print("name is: ", word)
        # word_quotes = '"{}"'.format(word)
        # print("word quotes is: ", word)
        if ((word) in data['name'].unique()):
            pokemon_name = word
            # print("POKEMON NAME: ", pokemon_name)
            return pokemon_name

def game_checker(message):
    games_list = ['alpha sapphire', 'omega ruby', 'omegaruby', 'alphasapphire', 'fire red', 'red', 'blue', 'yellow', 'firered', 'leafgreen', 'leaf green', 'ruby', 'sapphire', 
    'emerald', 'brilliant diamond', 'shining pearl', 'pearl', 'diamond', 'platinum','heartgold', 'soulsilver', 'heart gold', 'soul silver', 
    'gold', 'silver', 'crystal', 'black 2', 'white 2', 'black', 'white', 'pokemon x', 'pokemon y', 'ultra sun', 'ultra moon', 'pokemon ultra sun', 'pokemon ultra moon',
    'sun', 'pokemon sun', 'moon', 'pokemon moon',
    'sword', 'shield', 'legends arceus']
    for i in range(len(games_list)):
        message = message.lower()
        game = games_list[i]
        # print("game is: ", game)
        game_idx = message.find("in " + game)
        # print("game idx is: ", game_idx)
        # print("message is: ", message)
        if (game_idx != -1):
            game_idx += 3
            message_game = message[game_idx:game_idx + len(game)]
            return (True, message_game) 
    # break up message into tokens 
    # make them all lowercase
    return (False, None)

def game_processor(game_tuple):
    website_game_list = ['Red', 'Blue', 'Yellow', 'Gold', 'Silver', 'Crystal', 'Ruby', 'Sapphire', 'Emerald', 
    'FireRed', 'LeafGreen', 'Diamond', 'Pearl', 'Platinum', 'HeartGold', 'SoulSilver', 'Black', 'White', 
    'Black 2', 'White 2', 'X', 'Y', 'Omega Ruby', 'Alpha Sapphire', 'Sun', 'Moon', 'Ultra Sun', 'Ultra Moon', 
    'Sword', 'Shield', 'Brilliant Diamond', 'Shining Pearl', 'Legends: Arceus']
    unprocessed_game = game_tuple[1]
    unprocessed_game = unprocessed_game.replace("pokemon ", "")
    unprocessed_game = unprocessed_game.title()
    game = ''
    if ('firered' in unprocessed_game.lower()):
        game = 'FireRed'
    elif ('leafgreen' in unprocessed_game.lower()):
        game = 'LeafGreen'
    elif ('leaf green' in unprocessed_game.lower()):
        game = 'LeafGreen'
    elif ('fire red' in unprocessed_game.lower()):
        game = 'FireRed'
    elif ('alphasapphire' in unprocessed_game.lower()):
        game = 'Alpha Sapphire'
    elif ('omegaruby' in unprocessed_game.lower()):
        game = 'Omega Ruby'
    elif ('heartgold' in unprocessed_game.lower()):
        game = 'HeartGold'
    elif ('heart gold' in unprocessed_game.lower()):
        game = 'HeartGold'
    elif ('soul silver' in unprocessed_game.lower()):
        game = 'SoulSilver'
    elif ('soulsilver' in unprocessed_game.lower()):
        game = 'SoulSilver'
    elif ('legends arceus' in unprocessed_game.lower()):
        game = 'Legends: Arceus'
    elif (len(unprocessed_game.split()) == 1):
        game = unprocessed_game.title()
    else:
        for i in range(len(website_game_list)):
            if (unprocessed_game in website_game_list[i]):
                game = website_game_list[i]
    return game

def get_gen_from_game(game):
    gen_dct = {'Red':'Gen 1', 'Blue':'Gen 1', 'Yellow':'Gen 1', 'Gold':'Gen 2', 'Silver':'Gen 2', 'Crystal':'Gen 2',
    'Ruby':'Gen 3', 'Sapphire':'Gen 3', 'Emerald':'Gen 3', 'FireRed':'Gen 3', 'LeafGreen':'Gen 3',
    'Diamond':'Gen 4', 'Pearl':'Gen 4', 'Platinum':'Gen 4', 'HeartGold':'Gen 4', 'SoulSilver':'Gen 4',
    'Black':'Gen 5', 'White':'Gen 5', 'Black 2':'Gen 5', 'White 2':'Gen 5', 'X':'Gen 6', 'Y':'Gen 6', 'Omega Ruby':'Gen 6', 'Alpha Sapphire':'Gen 5',
    'Sun':'Gen 7', 'Moon':'Gen 7', 'Ultra Sun':'Gen 7', 'Ultra Moon':'Gen 7',
    'Sword':'Gen 8', 'Shield':'Gen 8', 'Brilliant Diamond':'Gen 8', 'Shining Pearl':'Gen 8', 'Legends: Arceus':'Gen 8'}
    return gen_dct[game]


def type_extractor(pokemon_name, get_type):
    pokemon_data = pd.read_csv("csv_files/Pokemon_data.csv")
    pokemon_df = pd.DataFrame(pokemon_data)
    pokemon_df = pokemon_df.drop(["pokedex_number"], axis = 1)
    pokemon_df.set_index("name", inplace = True)
    pokemon_name = pokemon_name.title()
    first_type = pokemon_df.loc[pokemon_name, "type1"] # string
    second_type = pokemon_df.loc[pokemon_name, "type2"]
    output_string = ''
    if (get_type == 1):
        if (second_type == "None"):
            output_string = pokemon_name + "'s type(s): " + first_type + "\n"
        else:
            output_string = pokemon_name + "'s type(s): " + first_type + "," + second_type + "\n"
    return [first_type, second_type, output_string]

def dex_num_string_extractor(pokemon_name):
    try:
        pokemon_name = pokemon_name.capitalize()
        pokemon_df = pd.DataFrame(data)
        pokemon_df.set_index("name", inplace = True)
        dex_number = pokemon_df.loc[pokemon_name, 'pokedex_number']
        out = pokemon_name + "'s National Dex number is: " + str(dex_number)
    except:
        out = 'No entry found'
    return out 

def dex_num_extractor(pokemon_name):
    try:
        pokemon_name = pokemon_name.capitalize()
        pokemon_df = pd.DataFrame(data)
        pokemon_df.set_index("name", inplace = True)
        dex_number = pokemon_df.loc[pokemon_name, 'pokedex_number']
    except:
        dex_number = 'No num found'
    return dex_number 

def weaknesses(type_tuple):
    weaknesses_lst = []
    type_1 = type_tuple[0]
    type_2 = type_tuple[1]
    output_string = type_tuple[2]
    if (type_2 == 'None'):
        for i in range(len(types)):
            val = type_df.T.loc[type_1, types[i]]
            if (val == 1):
                weaknesses_lst.append(types[i])
        # print("weaknesses list is: ", weaknesses_lst)
        # output_string += "Its weaknesses are: \n"
        for i in range(len(weaknesses_lst)):
            if (i < (len(weaknesses_lst) - 1)):
                output_string += "- " + weaknesses_lst[i] + "\n"
            else:
                output_string += "- " + weaknesses_lst[i]
        return output_string
    else:
        for i in range(len(types)):
            val1 = type_df.T.loc[type_1, types[i]]
            val2 = type_df.T.loc[type_2, types[i]]
            sum = val1 + val2
            if (sum > 0):
                weaknesses_lst.append(types[i])
        # output_string += "Its weaknesses are: \n"
        for i in range(len(weaknesses_lst)):
            if (i < (len(weaknesses_lst) - 1)):
                output_string += "- " + weaknesses_lst[i] + "\n"
            else:
                output_string += "- " + weaknesses_lst[i]
        return output_string

def strengths(type_tuple):
    strengths_lst = []
    type_1 = type_tuple[0]
    type_2 = type_tuple[1]
    output_string = type_tuple[2]
    try:
        if (type_2 == 'None'):
            for i in range(len(types)):
                val = type_df.loc[type_1, types[i]]
                if (val == 1):
                    strengths_lst.append(types[i])
            # output_string += "It's strong and super effective against: \n"
            if (len(strengths_lst) > 0):
                for i in range(len(strengths_lst)):
                    if (i < (len(strengths_lst) - 1)):
                        output_string += "- " + strengths_lst[i] + "\n"
                    else:
                        output_string += "- " + strengths_lst[i]
                return output_string
            else:
                print("None")
        else:
            for i in range(len(types)):
                val1 = type_df.loc[type_1, types[i]]
                val2 = type_df.loc[type_2, types[i]]
                sum = val1 + val2
                if (sum == 2):
                    strengths_lst.append(types[i]) 
                elif (val1 == 1):
                    strengths_lst.append(types[i])
                elif (val2 == 1):
                    strengths_lst.append(types[i])
            # output_string += "It's strong and super effective against: \n"
            if (len(strengths_lst) > 0):
                for i in range(len(strengths_lst)):
                    if (i < (len(strengths_lst) - 1)):
                        output_string += "- " + strengths_lst[i] + "\n"
                    else:
                        output_string += "- " + strengths_lst[i]
                return output_string
            else:
                print("None")
    except:
        print("Error: strengths")
 
def region_extractor(message):
    try: 
        message.lower()
    except:
        print("ERROR: region_extractor message lower")
    regions_list = ['kanto', 'johto', 'hoenn', 'sinnoh', 'unova', 'kalos', 'alola', 'galar', 'hisui']
    for i in range(len(regions_list)):
        region = regions_list[i]
        message_region = message.find(region)
        if (message_region != -1):
            return (True, message_region)
    return (False, None)

def obtain_pokemon_output(pokemon_name, game):
    dex_num = dex_num_extractor(pokemon_name)
    location_data = pd.read_csv('csv_files/Pokemon_locations.csv')
    location_df = pd.DataFrame(location_data)
    location_df.set_index('pokemon_id', inplace = True)
    pokemon_location = location_df.loc[dex_num, game]
    # location_series = pd.Series(pokemon_location)
    # final_location = location_series.iloc[0]
    return pokemon_location

def obtain_evolution_output(pokemon_name):
    evolution_data = pd.read_csv("csv_files/evolution_criteria.csv")
    evolution_df = pd.DataFrame(evolution_data)
    evolution_df.set_index('pokemon_name', inplace = True)
    evolution_criteria = evolution_df.loc[pokemon_name, 'evolution_criteria']
    return evolution_criteria 

def get_move_effect(move):
    move_data = pd.read_csv("csv_files/pokemon_moves.csv")
    move_df = pd.DataFrame(move_data)
    move_df.set_index('Name', inplace = True)
    move_effect = move_df.loc[move, 'Effect']
    return move_effect 

    # each intent gets its own parse function
    # use a bunch of boolean functions to determine which parse function is used

    # so let's say intent is pokemon_location: 
        # 2 inputs to check, if pokemon (assign an int) and game (also assign an int?)
        # if both inputs pass, then pass into pokemon_location_parser
        # build response string in this function and return as output
    # if intent is level_evolve: 
        # 1 input to check, it pokemon (assign an int)
        # if input passes, pass into level_parser function
        # this parser needs to determine if it evolves by level or not
        # this parser then needs to build an output string, either the level or 
        # "doesn't evolve by level-up, I suggest asking "how to get ______ in ______ ""
    # dex number should be easy
    # if intent is item locations:
        # 2 inputs to check, if item (if your pokemon_int converter doesn't make it a number), if game
        # you can reuse your game boolean checker for game, and pokemon boolean checker
        # then pass into item_parser: you have an item and can directly build a link
        # then parse item dex on serebii:
            # NOTE: you'll have to pick out the right game using the second argument and access
            # its next html entry
    # pokemon_go_items:
        # directly parse them through this link on serebii: https://www.serebii.net/pokemongo/items.shtml
        # if your input isn't a pokemon (boolean checker), then it's an item
        # have a boolean checker specifically to see if the game is pokemon_go
        # inputs for pogo_item_parser: item
    # pokemon_go_pokemon_obtaining: 
        # just evolvables 
        # try this link: https://pokemon.gameinfo.io/
    # else case: look it up on google and print out that text at the beginning