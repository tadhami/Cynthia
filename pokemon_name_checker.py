import difflib
import numpy as np 
import pokebot_parser
import pandas as pd 

pokemon_file = pd.read_csv("Pokemon_data.csv")
pokemon_df = pd.DataFrame(pokemon_file)
names = pokemon_df["name"]

def my_pokemon_name_checker():
    my_names = [x.strip() for x in names]
    my_names_lower = my_names.copy()
    for i in range(len(my_names_lower)):
        my_names_lower[i] = my_names_lower[i].lower()
        my_names_lower[i] = my_names_lower[i].replace(" ", "")
    return my_names, my_names_lower

def capitalize_each_word(lst):
    for i in range(len(lst)):
        lst[i] = lst[i].capitalize()
    return lst 

def find_nearest_matches(name, result, lower_names, all_names, message):
    name = name.lower()
    substring_list = []
    n = 1
    cutoff = 0.8
    for substring in result:
        close_matches = difflib.get_close_matches(substring, lower_names, n, cutoff)
        if (len(close_matches) > 0):
            substring_list.append(close_matches[0])
    unique, counts = np.unique(substring_list, return_counts=True)
    if (len(unique) > 0):
        print("Did you mean: ", unique)

def validate_spelling(name, result, lower_names, all_names, message):
    '''
    Function to check the final output for the next function with the initial message
    '''
    name = name.lower()
    substring_list = []
    n = 1
    cutoff = 0.9
    for substring in result:
        close_matches = difflib.get_close_matches(substring, lower_names, n, cutoff)
        if (len(close_matches) > 0):
            substring_list.append(close_matches[0])
    unique, counts = np.unique(substring_list, return_counts=True)
    try:
        if (max(counts) == min(counts)):
            item_of_interest = max(unique, key=len)
        else:
            item_of_interest = unique[np.argmax(counts)]
        idx = lower_names.index(item_of_interest)
        final_extracted_item = all_names[idx]
        return final_extracted_item
    except:
        final_extracted_item = 'Not Found'
        return final_extracted_item

def special_case_names(result):
    '''
    Function to handle special-case names of pokemon that weren't being correctly detected in other functions. 
    Less able to handle spelling errors, but at least by writing this function the spell-check capabilities
    of the other functions are retained. 

    '''
    special_case_names_lower = ['nidorina', 'nidorino' ,'woobat','porygon','azumarill', 'nosepass', 'porygon-z', 'porygon2', 'fan rotom', 'mow rotom', 'cinccino','minccino','klinklang', 'lairon', 'swoobat', 'pidgeotto']
    special_case_names_upper = ['Nidorina', 'Nidorino','Woobat','Porygon','Azumarill', 'Nosepass', 'Porygon-Z', 'Porygon2', 'Fan Rotom', 'Mow Rotom', 'Cinccino', 'Minccino', 'Klinklang', 'Lairon', 'Swoobat', 'Pidgeotto']

    substring_list = []
    n = 1
    cutoff = 0.93
    for substring in result:
        close_matches = difflib.get_close_matches(substring, special_case_names_lower, n, cutoff)
        if (len(close_matches) > 0):
            substring_list.append(close_matches[0])
    unique, counts = np.unique(substring_list, return_counts=True)
    try:
        if (max(counts) == min(counts)):
            item_of_interest = max(unique, key=len)
        else:
            item_of_interest = unique[np.argmax(counts)]
        idx = special_case_names_lower.index(item_of_interest)
        final_extracted_item = special_case_names_upper[idx]
        return final_extracted_item
    except:
        final_extracted_item = 'Not Found'
        return final_extracted_item

def my_name_extractor(message):
    all_names_tup = my_pokemon_name_checker()
    all_names = all_names_tup[0]
    lower_names = all_names_tup[1]
    n = 1
    try:
        game_tup = pokebot_parser.game_checker(message)
        message = message.replace(game_tup[1], "")
    except:
        pass 
    item_tup = pokebot_parser.get_item_output(message, game_tup)
    item = ''
    if (item_tup[1] == True):
        item = item_tup[0].lower()
    item_idx = message.find(item)
    if (item_idx > 0):
        if (message[item_idx - 1].isalpha() == False): # handle Lairon or Nosepass (item is iron or pass)
            message = message.replace(item, "")
    elif (item_idx == 0):
        message = message.replace(item, "")
   
    message = message.replace(" ", "").lower()
    message = message.replace("'s", "")
    result = []
    if ("mega" in message):
        idx = message.find("mega")
        poke_name = message[idx:]
        result.append(poke_name)
    elif ("alolan" in message):
        idx = message.find("alolan")
        poke_name = message[idx:]
        result.append(poke_name)
    elif ("galarian" in message):
        idx = message.find("galarian")
        poke_name = message[idx:]
        result.append(poke_name)
    else: 
        result = [message[i: j] for i in range(len(message))
            for j in range(i + 1, len(message) + 1)]
    
    # Handle special cases for names, less able to handle spelling errors but not a huge deal
    final_extracted_item = special_case_names(result)
    if (final_extracted_item != 'Not Found'):
        return final_extracted_item
    # Handle rest of names here
    cutoff = 0.75
    substring_list = []
    for substring in result: 
        close_matches = difflib.get_close_matches(substring, lower_names, n, cutoff)
        if (len(close_matches) > 0):
            substring_list.append(close_matches[0])
    unique, counts = np.unique(substring_list, return_counts=True)
    try:
        if (max(counts) == min(counts)):
            item_of_interest = max(unique, key=len)
        else:
            item_of_interest = unique[np.argmax(counts)]
        idx = lower_names.index(item_of_interest)
        final_extracted_item = all_names[idx]
        validator = validate_spelling(final_extracted_item, result, lower_names, all_names, message)
        if (validator == final_extracted_item):
            return final_extracted_item
        if (validator == 'Not Found'):
            find_nearest_matches(final_extracted_item, result, lower_names, all_names, message)
            final_extracted_item = 'Not Found'
            return final_extracted_item
        return final_extracted_item
    except:
        final_extracted_item = 'Not Found'
        validator = validate_spelling(final_extracted_item, result, lower_names, all_names, message)
        return final_extracted_item
