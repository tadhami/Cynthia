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
    pokemon_data = pd.read_csv("csv_files/pokemon_moves.csv")
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

def get_move_info_csv(query, message):
    move_name = move_name_extractor(message, 1)
    data = pd.read_csv("csv_files/pokemon_moves.csv")
    df = pd.DataFrame(data)
    df.set_index('Name', inplace=True)
    out = df.loc[move_name, query]
    if (str(out) == 'nan'):
        return 'No extra effects'
    return out 

def get_name_from_dex_number(pokemon_id):
    data = pd.read_csv("csv_files/Pokemon_data.csv")
    pokemon_df = pd.DataFrame(data)
    pokemon_df.set_index("pokedex_number", inplace = True)
    pokemon_name = pokemon_df.loc[pokemon_id, 'name']
    name_series = pd.Series(pokemon_name)
    pokemon_name = name_series.iloc[0]
    return pokemon_name

def list_of_links_generator(pokemon_id, new_number, pokemon_page, list_of_links):
    g1 = '/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g1)
    g2 = '-gs/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g2)
    g3 = '-rs/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g3)
    g4 = '-dp/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g4)
    g5 = '-bw/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g5)
    g6 = '-xy/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g6)
    g7 = '-sm/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g7)
    g8_name = get_name_from_dex_number(pokemon_id).lower()
    g8 = '-swsh/' + g8_name
    list_of_links.append(pokemon_page + g8)

    return list_of_links

def gen_extractor(message):
    idx = message.index("gen")
    return int(message[idx + 4])

def get_move_information(soup, move_name, gen):
    move_info = soup.findAll('a', text = move_name)
    ret_lst = []
    ret_str = ''
    
    if (len(move_info) == 0) and (gen == 0):
        ret_str = "It can't learn it\n"
        return ret_str
    if (len(move_info) == 0) and (gen != 0):
        ret_str = "It can't learn it in gen " + str(gen) + '\n'
        return ret_str 
    
    # gen 8 gives extra unnecessary info
    if (len(move_info) > 3):
        move_info = move_info[0:3]
    for i in range(len(move_info)):
        item = move_info[i]
        table_header = item.findPrevious(attrs = {'class':'dextable'}).find('td').text.strip()
        if ("(Details)" in table_header):
            table_header = table_header.replace(" (Details)", "")
        final_item = item.findPrevious('tr').find('td').text.strip()
        # to avoid inclusion of extra gen 8 move entries
        check = item.findPrevious('tr').find('td').find('br')
        if (check == None):
            if ("BDSP Only" in final_item):
                str_idx = final_item.index("BDSP Only")
                final_item = final_item[:str_idx] + " " + final_item[str_idx:]
            try:
                final_item = int(final_item)
                final_item = str(final_item)
                final_item = table_header + ": " + final_item
                ret_lst.append(final_item)
            except:
                if (i != (len(move_info) - 1)):
                    final_item = table_header + ": " + final_item
                    ret_lst.append(final_item)
                else:
                    final_item = table_header + ": " + final_item
                    ret_lst.append(final_item)
    for i in range(len(ret_lst)):
        ret_lst[i] = ret_lst[i] + "\n"
            
    # handle repeats, like when you see Level # twice
    ret_lst = [*set(ret_lst)]
    move_filter = move_name + "\n"

    if move_filter in ret_lst:
        ret_lst.remove(move_filter)
    if (gen != 0):
        ret_lst.insert(0, "Gen: " + str(gen) + "\n")
    for i in range(len(ret_lst)):
        ret_str += ret_lst[i]
    return ret_str 

def when_learn_move(message):
    pokemon = pokebot_parser.pokemon_name_extractor(message)
    message = message.replace(pokemon.lower(), "")
    number_str = str(pokebot_parser.dex_num_extractor(pokemon)).zfill(3)
    number = pokebot_parser.dex_num_extractor(pokemon)
    move_name = move_name_extractor(message, 1)
    
    pokemon_page = 'https://www.serebii.net/pokedex'
    my_links = list_of_links_generator(number, number_str, pokemon_page, [])
    try:
        idx = gen_extractor(message)
    except:
        return "Didn't include gen in message"
    
    link = my_links[idx - 1]
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser", from_encoding = "iso-8859-1")

    try:
        move_info = get_move_information(soup, move_name, 0)
    except:
        move_info = "Error: when_learn_move"
    sleep(random.randint(0,3))

    move_info = move_info[:-1]
    return move_info

def when_learn_move_all_gens(message):
    pokemon = pokebot_parser.pokemon_name_extractor(message)
    message = message.replace(pokemon.lower(), "")
    number_str = str(pokebot_parser.dex_num_extractor(pokemon)).zfill(3)
    number = pokebot_parser.dex_num_extractor(pokemon)
    move_name = move_name_extractor(message, 1)
    move_info = ''
    final_str = ''

    pokemon_page = 'https://www.serebii.net/pokedex'
    my_links = list_of_links_generator(number, number_str, pokemon_page, [])
    gen = 1
    for link in my_links:
        try:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, "html.parser", from_encoding = "iso-8859-1")
        except:
            move_info = "Not found in this gen. "
        try:
            move_info = get_move_information(soup, move_name, gen)
        except:
            move_info += "Error: when_learn_move"
        sleep(random.randint(0,3))
        final_str += move_info
        gen += 1
    
    final_str = final_str[:-1]
    return final_str

def when_learn_move_game(message):
    initial_message = message
    pokemon = pokebot_parser.pokemon_name_extractor(message)
    message = message.replace(pokemon.lower(), "")
    number_str = str(pokebot_parser.dex_num_extractor(pokemon)).zfill(3)
    number = pokebot_parser.dex_num_extractor(pokemon)
    move_name = move_name_extractor(message, 1)

    pokemon_page = 'https://www.serebii.net/pokedex'
    my_links = list_of_links_generator(number, number_str, pokemon_page, [])
    try:
        tup = pokebot_parser.game_checker(initial_message)
        if tup[0] == True:
            game = pokebot_parser.game_processor(tup)
        else:
            game = ''
            final_str = when_learn_move_all_gens(initial_message)
            return final_str 
        idx = int(pokebot_parser.get_gen_from_game(game)[4:])
    except:
        return "Error: when_learn_move_game, or didn't include a game"

    link = my_links[idx - 1]
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser", from_encoding = "iso-8859-1")

    try:
        move_info = get_move_information(soup, move_name, 0)
    except:
        move_info = "Error: when_learn_move"
    sleep(random.randint(0,3))

    move_info = move_info[:-1]
    return move_info



# Can or can't learn a move:
# contains links for gens 1-8 for each pokemon
# be sure to include a try/except statement for if a link doesn't even work 
def move_dct_string(move_dictionary):
    ret_str = ''
    for key in move_dictionary:
        ret_str += (key + ': ' + move_dictionary[key] + '\n')
    ret_str = ret_str[:-1]
    return ret_str 

# goes in output generator:
number = str(254).zfill(3)
pokemon_page = 'https://www.serebii.net/pokedex'
my_links = list_of_links_generator(254, number, pokemon_page, [])

def can_learn_move(links, move_name):
    gen_dict = {}
    gen_num = 1
    for i in range(len(links)):
        gen_link = links[i]
        sleep(random.randint(0,3))
        try:
            page = requests.get(gen_link)
            soup = BeautifulSoup(page.content, "html.parser")
            move_found = soup.find(text = move_name)
            if len(move_found) > 0:
                move_found = "Yes it learns it in this gen"
            else:
                move_found = "Nope"
        except:
            move_found = "Nope"
        gen_dict['Gen ' + str(gen_num)] = move_found
        gen_num += 1
    return gen_dict
    
