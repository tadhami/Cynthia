import difflib
import numpy as np 
import pokebot_parser

def my_item_checker():
    with open('items.txt') as fp:
        all_items = fp.readlines()
    all_items = [x.strip() for x in all_items]
    for i in range(len(all_items)):
        all_items[i] = all_items[i].replace("é", "e")
    all_items_lower = all_items.copy()
    for i in range(len(all_items_lower)):
        all_items_lower[i] = all_items_lower[i].lower()
        all_items_lower[i] = all_items_lower[i].replace(" ", "")
    return all_items, all_items_lower

def item_extractor(message):
    all_items_tup = my_item_checker()
    all_items = all_items_tup[0]
    lower_items = all_items_tup[1]
    n = 1
    while(True):
        message = input("enter a request: ")
        if (message == 'quit'):
            break
        game_tup = pokebot_parser.game_checker(message)
        message = message.replace(game_tup[1], "")
        # print("message with game removed is: ", message)
        # handle if plural -ies
        message = message.split(' ')
        # print("message after splitting into list: ", message)
        for i in range(len(message)):
            if (message[i][-3:] == 'ies'):
                message[i] = message[i].replace("ies", "y")
        message = ' '.join(message)
        # print("message after rejoining: ", message)
        cutoff = 0.95
        message = message.replace(" ", "")
        result = [message[i: j] for i in range(len(message))
            for j in range(i + 1, len(message) + 1)]
        # print(result)
        substring_list = []
        for substring in result: 
            close_matches = difflib.get_close_matches(substring, lower_items, n, cutoff)
            if (len(close_matches) > 0):
                print(close_matches)
                substring_list.append(close_matches[0])
        # print(substring_list)
        unique, counts = np.unique(substring_list, return_counts=True)
        print("unique is: ", unique)
        print("counts are: ", counts)
        try:
            if (max(counts) == min(counts)):
                item_of_interest = max(unique, key=len)
            else:
                item_of_interest = unique[np.argmax(counts)]
            idx = lower_items.index(item_of_interest)
            final_extracted_item = all_items[idx]
            print("final item is: ", final_extracted_item)
        except:
            final_extracted_item = 'Not Found'
            print(final_extracted_item)



