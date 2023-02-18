# Final algorithm: extract a move name from a message 
import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import pandas as pd
import random 
import difflib
import pokebot_parser
import numpy as np 


def get_moves_list():
    pokemon_data = pd.read_csv("pokemon_moves.csv")
    move_df = pd.DataFrame(pokemon_data)
    move_names_lst = move_df['Name']
    return move_names_lst

def lower_moves_list(move_names_list):
    for i in range(len(move_names_list)):
        move_names_list[i] = move_names_list[i].lower()
    return move_names_list

def exceptions_move_name_extractor(result, check):
    moves_names_lst = get_moves_list()
    upper_moves_names_lst = get_moves_list()
    moves_names_lst = lower_moves_list(moves_names_lst).tolist()

    exceptions_lst = ['barb barrage', 'bubble beam', 'bug bite', 'charge beam', 'clangorous soulblaze', 'conversion 2', 'conversion', 'discharge', 'head charge', 'heal block', 'high jump kick', 'inferno overdrive', 'misty explosion', 'petal blizzard', 'powder snow', 'power trick',
    'psychic fangs', 'rage powder', 'reflect type', 'sleep powder', 'sludge bomb', 'sludge wave', 'splishy splash', 'steam eruption', 'strength sap', 'struggle bug', 'stun spore', 'thunder cage', 'thunder fang', 'thunder punch', 'thunder wave', 'toxic spikes', 'trick room',
    'volt tackle', 'wild charge', 'zen headbutt', 'gyro ball', 'heal block', 'high jump kick', 'mat block', 'sand tomb', 'stun spore', 'trick room', 'water sport', 'pyro ball', 'block', 'jump kick', 'block', 'sandstorm', 'spore', 'trick']

    substring_list = []
    n = 1
    cutoff = 0.95
    for substring in result:
        close_matches = difflib.get_close_matches(substring, exceptions_lst, n, cutoff)
        if (len(close_matches) > 0):
            substring_list.append(close_matches[0])
    unique, counts = np.unique(substring_list, return_counts=True)
    try:
        if (max(counts) == min(counts)):
            item_of_interest = max(unique, key=len)
            if (check == 1):
                idx = moves_names_lst.index(item_of_interest)
                final_extracted_item = upper_moves_names_lst[idx]
                return final_extracted_item 
        else:
            item_of_interest = unique[np.argmax(counts)]
            if (check == 1):
                idx = moves_names_lst.index(item_of_interest)
                final_extracted_item = upper_moves_names_lst[idx]
                return final_extracted_item 
        idx = exceptions_lst.index(item_of_interest)
        final_extracted_item = exceptions_lst[idx]
        return final_extracted_item
    except:
        final_extracted_item = 'Not Found'
        return final_extracted_item

exc_list = []

def move_name_extractor(name, check):
    moves_names_lst = get_moves_list()
    upper_moves_names_lst = get_moves_list()
    moves_names_lst = lower_moves_list(moves_names_lst).tolist()
    
    n = 1
    message = name
    game_tup = pokebot_parser.game_checker(message)
    # If there's a game in the message, should probably move this into the output file 
    try:
        message = message.replace(game_tup[1], "")
    except:
        pass 

    cutoff = 0.7
    message = message.replace(" ", "")
    result = [message[i: j] for i in range(len(message))
        for j in range(i + 1, len(message) + 1)]
    
    # Handle special cases for names, less able to handle spelling errors but not a huge deal
    final_extracted_item = exceptions_move_name_extractor(result, check)
    if (final_extracted_item != 'Not Found'):
        return final_extracted_item

    substring_list = []
    for substring in result:
        close_matches = difflib.get_close_matches(substring, moves_names_lst, n, cutoff)
        if (len(close_matches) > 0):
            substring_list.append(close_matches[0])
    unique, counts = np.unique(substring_list, return_counts=True)
    try:
        if (max(counts) == min(counts)):
            item_of_interest = max(unique, key=len)
            if (check == 1):
                idx = moves_names_lst.index(item_of_interest)
                final_extracted_item = upper_moves_names_lst[idx]
                return final_extracted_item
            return item_of_interest
        else:
            item_of_interest = unique[np.argmax(counts)]
            if (check == 1):
                idx = moves_names_lst.index(item_of_interest)
                final_extracted_item = upper_moves_names_lst[idx]
                return final_extracted_item
            return item_of_interest
    except:
        final_extracted_item = 'Not Found ' + str(close_matches)
        return final_extracted_item

def format_pokemondb_move_urls(move_name):
    general_url = 'https://pokemondb.net/move/'
    move_lst = move_name.split()
    new_name = ''
    for i in range(len(move_lst)):
        move_lst[i] = move_lst[i].lower()
    new_name = ' '.join(move_lst)
    new_name = new_name.replace(",", "")
    new_name = new_name.replace("'", "")
    new_name = new_name.replace(" ", "-")
    return general_url + new_name 

def get_move_info_csv(query, message):
    move_name = move_name_extractor(message, 1)
    data = pd.read_csv("pokemon_moves.csv")
    df = pd.DataFrame(data)
    df.set_index('Name', inplace=True)
    out = df.loc[move_name, query]
    if (str(out) == 'nan'):
        return 'Not sure'
    return out 


while True: # goes in output generator
    message = input()
    output = get_move_info_csv('Effect', message)
    print(output)


# Checking if a pokemon can learn a move and when it learns a move

