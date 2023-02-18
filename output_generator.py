import pokebot_parser
import pokemon
import pokemon_name_checker
import pogo_parser
import move_parser
'''
Script containing function calls to generate an output string/response string based on certain conditionals
(relating to which tag)
'''
out = ''
# 4
exclusion_tags = ['goodbye', 'hi', 'features', 'ucl']
limitations_disclaimer = "These are just the pokemon that will spawn for this specific season or event, other pokemon are probably spawning too but I can't determine every single pokemon spawning right now in Pokemon Go. If you want a more comprehensive look at what's spawning by you, check out pokemap.net"

def list_features():
    out = "- Tell you a pokemon's pokedex number\n- Tell you a pokemon's specific in-game location\n- Tell you a pokemon's evolution criteria\n- Tell you a pokemon's strengths\n- Tell you a pokemon's weaknesses\n- Tell you a pokemon's type\n- Tell you a pokemon's height\n- Tell you a pokemon's weight\n- Tell you a pokemon's classification\n- Tell you all I know about a pokemon\n- Tell you the location of any item in any game\n- For Pokemon Go I can tell you the next and current: 5-star raids, mega raids, community days, research breakthroughs, events, current spawns, spotlight hours, and raid hours"
    return out 
def chatbot_output_string_generator(tag, message):
    if (tag == 'dex_number'):
        # 905
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        output = str(pokebot_parser.dex_num_extractor(pokemon_name))
        return output  
    elif (tag == 'location'):
        # 29,865 for pokemon locations + 39,963 = 69,828
        try:
            pokemon_name = pokemon_name_checker.my_name_extractor(message)
        except:
            pokemon_name = None
        try:
            game_tuple = pokebot_parser.game_checker(message)
        except:
            game_tuple = False, 'No game found: Output Generator'
        if (game_tuple[0] == True):
            pokemon_game = pokebot_parser.game_processor(game_tuple)
            item_tup = pokebot_parser.get_item_output(message, game_tuple)
            if (item_tup[1] == True):
                final_item_output = pokebot_parser.item_final_output(item_tup[0], pokemon_game)
                return final_item_output
            elif (pokemon_name != None):
                location_output = pokebot_parser.obtain_pokemon_output(pokemon_name, pokemon_game)
                return location_output 
        else:
            output = "You either can't get it in this game, you misspelled the name, or I'm not advanced enough to handle this request"
            return output 
    elif (tag == 'level_evolve'):
        # 905
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        output = pokebot_parser.obtain_evolution_output(pokemon_name)
        return output 
    elif (tag == 'strengths'):
        # 905
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        type_lst = pokebot_parser.type_extractor(pokemon_name, 1)
        output = pokebot_parser.strengths(type_lst)
        return output 
    elif (tag == 'weaknesses'):
        # 905
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        type_lst = pokebot_parser.type_extractor(pokemon_name, 1)
        output = pokebot_parser.weaknesses(type_lst)
        return output 
    elif (tag == 'type'):
        # 905
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        type_lst = pokebot_parser.type_extractor(pokemon_name, 1)
        output = type_lst[2].replace("\n", "")
        return output
    elif (tag == 'height'):
        # 905
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        my_pokemon = pokemon.Pokemon()
        pokemon.populate_pokemon(my_pokemon, pokemon_name)
        return str(my_pokemon.height_m) + ' m tall'
    elif (tag == 'weight'):
        # 905
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        my_pokemon = pokemon.Pokemon()
        pokemon.populate_pokemon(my_pokemon, pokemon_name)
        return str(my_pokemon.weight_kg) + 'kg'
    elif (tag == 'classification'):
        # 905
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        my_pokemon = pokemon.Pokemon()
        pokemon.populate_pokemon(my_pokemon, pokemon_name)
        return str(my_pokemon.classification)
    elif (tag == 'all info'):
        # 905 
        pokemon_name = pokemon_name_checker.my_name_extractor(message)
        my_pokemon = pokemon.Pokemon()
        pokemon.populate_pokemon(my_pokemon, pokemon_name)
        out = pokemon.all_string_builder(my_pokemon)
        return out 
    elif (tag == 'list_out'):
        # 1
        print("entered list out")
        output = list_features()
        print("output is: ", output)
        return output 
    elif (tag == 'pogo_all_spawns'):
        # 1
        output = pogo_parser.get_pogo_general_string()
        return output + limitations_disclaimer
    elif (tag == 'pogo_season_spawns'):
        # 1
        output = pogo_parser.get_pogo_season_string() 
        return output + limitations_disclaimer
    elif (tag == 'pogo_event_spawns'):
        # 1
        output = pogo_parser.get_pogo_event_string()
        return output + limitations_disclaimer
    # NOTE: EDITS START HERE    
    elif (tag == 'raids'):
        # 6
        try:
            output = pogo_parser.get_current_raid_info(message)
            return output 
        except:
            output = "Sorry, I couldn't figure out the info on raids you asked about"
            return output 
    elif (tag == 'pogo_next_research_breakthrough'):
        # 1
        try:
            output = pogo_parser.get_most_recent_research_breakthroughs()
            return output 
        except:
            output = "Sorry, I couldn't find the info you asked for about research breakthroughs"
    elif (tag == 'pogo_current_research_breakthrough'):
        # 1
        try:
            output = pogo_parser.get_most_recent_research_breakthroughs()
            return output 
        except:
            output = "Sorry, I couldn't find the info you asked for about research breakthroughs"
    elif (tag == 'pogo_next_spotlight_hour'):
        # 1
        try:
            output = pogo_parser.get_spotlight_hour_info(True) 
            return output 
        except:
            output = "Sorry, I couldn't find the spotlight hour info you were looking for"
            return output 
    elif (tag == 'pogo_current_spotlight_hour'):
        # 1
        try:
            output = pogo_parser.get_spotlight_hour_info(False) 
            return output 
        except:
            output = "Sorry, I couldn't find the spotlight hour info you were looking for"
            return output  
    elif (tag == 'pogo_next_month_comm_day'):
        # 1
        print("Comm day has been reached")
        try: 
            output = pogo_parser.get_comm_day_info(True)
            return output 
        except: 
            output = "Sorry, I couldn't figure out the comm day info you were asking for"
            return output 
    elif (tag == 'pogo_current_month_comm_day'):
        # 1
        try: 
            output = pogo_parser.get_comm_day_info(False)
            return output 
        except: 
            output = "Sorry, I couldn't figure out the comm day info you were asking for"
            return output
    #NOTE: EVENTS END HERE    
    elif (tag == 'moves_effect'):
        # 866 questions
        try:
            game_tup = pokebot_parser.game_checker(message)
            message = message.replace(game_tup[1], "")
        except:
            pass
        try:
            pokemon_name = pokemon_name_checker.my_name_extractor(message)
            message = message.replace(pokemon_name, "")
        except:
            pass
        try:
            output = move_parser.get_move_info_csv('Effect', message)
        except:
            output = "Sorry I'm not sure." 
        return output
    elif (tag == 'can_learn_move'):
        # 783,730 unique questions
        try:
            name = pokebot_parser.pokemon_name_extractor(message)
            num = pokebot_parser.dex_num_extractor(name)
            pokemon_page = 'https://www.serebii.net/pokedex'
            links = move_parser.list_of_links_generator(num, str(num).zfill(3), pokemon_page, []) 
            move_name = move_parser.move_name_extractor(message, 1)
            dct = move_parser.can_learn_move(links, move_name)
            output = move_parser.move_dct_string(dct)
            return output
        except:
            return "I have no idea" 
    elif (tag == 'when_learn_move_gen'):
        # 6,269,840 unique questions
        try:
            output = move_parser.when_learn_move(message)
            return output
        except:
            return 'Not sure'  
    elif (tag == 'when_learn_move_game'):
        # 25,863,090 unique questions: 866 moves x 905 pokemon x 33 games + 783,730 if no game
        try:
            output = move_parser.when_learn_move_game(message)
            return output
        except:
            return 'Not sure'
    elif (tag == 'send_shiny_pic'):
        return "Here you go!"
    elif (tag == 'send_normal_pic'):
        return "Here you go!"
    
def json_modifier(json_data, tag, message):
    print("tag in json_modifier is: ", tag)
    json_dict = {'hi':0, 'features':1, 'list_out':2, 'dex_number':3, 'location':4, 'level_evolve':5, 'strengths':6, 
    'weaknesses':7, 'type':8, 'height':9, 'weight':10, 'classification':11, 'all info':12, 'goodbye':13, 'ucl':14, 'pogo_all_spawns':15,
    'pogo_season_spawns':16, 'pogo_event_spawns':17, 'raids':18, 'pogo_next_research_breakthrough':19, 'pogo_current_research_breakthrough':20,
    'pogo_next_spotlight_hour':21, 'pogo_current_spotlight_hour':22, 'pogo_next_month_comm_day':23, 'pogo_current_month_comm_day':24, 
    'moves_effect':25, 'can_learn_move':26, 'when_learn_move_gen':27,
    'when_learn_move_game':28, 'send_shiny_pic':29, 'send_normal_pic':30}
    if (tag not in exclusion_tags):
        output = chatbot_output_string_generator(tag, message)
        print("AFTER ENTER: OUTPUT IS: ", output) 
        json_data['intents'][json_dict[tag]]['responses'][0] = output
    return json_data 



