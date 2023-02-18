import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import pandas as pd
import random 
import pokebot_parser

data = pd.read_csv("csv_files/Pokemon_data.csv")
def get_name_from_dex_number(pokemon_id):
    pokemon_df = pd.DataFrame(data)
    pokemon_df.set_index("pokedex_number", inplace = True)
    pokemon_name = pokemon_df.loc[pokemon_id, 'name']
    name_series = pd.Series(pokemon_name)
    pokemon_name = name_series.iloc[0]
    return pokemon_name

# item = get_name_from_dex_number(2)
# print(item)
# id = pokebot_parser.dex_num_extractor(item)
# print("Your id is: ", id)

def parse_location(webpage, location_class_list, num_games, gen1, bdsp, gen8):
    selector = 'body > div > div > main > div'
    locations_dict = {}
    try:
        my_page = requests.get(webpage)
        my_soup = BeautifulSoup(my_page.content, "html.parser")
        for br in my_soup('br'):
            br.replace_with(',')
    except:
        for i in range(num_games):
                locations_dict['game' + str(i)] = 'Not found in this generation'
        print(locations_dict)
        return locations_dict
  
    if (gen8 == True):
        try:
            gen8_element = my_soup.select('body > div > div > main > div:nth-child(2)')[0]
        except:
            locations_dict['game0'] = 'Not found in Legends Arceus'
            locations_dict['game1'] = 'Not found in Sword'
            locations_dict['game2'] = 'Not found in Shield'
            locations_dict['game3'] = 'Not found in Brilliant Diamond'
            locations_dict['game4'] = 'Not found in Shining Pearl'
            print(locations_dict)
            return locations_dict
        try:
            pla_locations = gen8_element.find_all('td', attrs={'class':location_class_list[0]})[0]
            pla_idx = pla_locations.parent.findPrevious('tr')
            pla_updated_locations = pla_idx.findAllNext('tr', limit = 1)

            pla_and_location = pla_updated_locations[0].find_all('td')
            locations_dict['game0'] = pla_and_location[1].get_text(separator = " ", strip = True)
        except:
            locations_dict['game0'] = 'Not found in Legends Arceus'
        try:
            gen8_locations = gen8_element.find_all('td', attrs={'class':location_class_list[1]})[0]
            gen8_idx = gen8_locations.parent.findPrevious('tr')
            gen8_updated_locations = gen8_idx.findAllNext('tr', limit = 2)

            sword_and_location = gen8_updated_locations[0].find_all('td')
            locations_dict['game1'] = sword_and_location[1].get_text(separator = " ", strip = True)

            shield_and_location = gen8_updated_locations[1].find_all('td')
            locations_dict['game2'] = shield_and_location[1].get_text(separator = " ", strip = True)
        except:
            locations_dict['game1'] = 'Not found in Sword'
            locations_dict['game2'] = 'Not found in Shield'
        try: 
            bdsp_locations = gen8_element.find_all('td', attrs={'class':location_class_list[2]})[0]
            bdsp_idx = bdsp_locations.parent.findPrevious('tr')
            bdsp_updated_locations = bdsp_idx.findAllNext('tr', limit = 2)

            brilliant_diamond_and_location = bdsp_updated_locations[0].find_all('td')
            locations_dict['game3'] = brilliant_diamond_and_location[1].get_text(separator = " ", strip = True)

            shining_pearl_and_location = bdsp_updated_locations[1].find_all('td')
            locations_dict['game4'] = shining_pearl_and_location[1].get_text(separator = " ", strip = True)
        except:
            locations_dict['game3'] = 'Not found in Brilliant Diamond'
            locations_dict['game4'] = 'Not found in Shining Pearl'
    else:
        try:
            location_element = my_soup.select(selector)[0]
            # print("location_element is: ", location_element)
            games_locations = location_element.find_all('td', attrs={'class':location_class_list[0]})[bdsp]
            # print("games_locations are: ", games_locations)
            games_idx = games_locations.parent.findPrevious('tr')
            updated_locations = games_idx.findAllNext('tr', limit = num_games)
            for i in range(num_games):
                if (i == 1 and gen1 == True):
                    location = updated_locations[i].find_all('td')
                    final_location = location[2].get_text(separator = " ", strip = True)
                    final_location = final_location.replace("PokÃ©mon", "Pokemon")
                    locations_dict['game' + str(i)] = final_location
                elif (i == 2 and gen1 == True):
                    location = updated_locations[3].find_all('td')
                    final_location = location[1].get_text(separator = " ", strip = True)
                    final_location = final_location.replace("PokÃ©mon", "Pokemon")
                    locations_dict['game' + str(i)] = final_location
                elif (i == 3 and gen1 == True):
                    continue 
                else:
                    location = updated_locations[i].find_all('td')
                    final_location = location[1].get_text(separator = " ", strip  = True)
                    final_location = final_location.replace("PokÃ©mon", "Pokemon")
                    locations_dict['game' + str(i)] = final_location
        except:
            for i in range(num_games):
                locations_dict['game' + str(i)] = 'Not found in this generation'
            print(locations_dict)
            return locations_dict
    print(locations_dict)
    return locations_dict

def list_of_links_generator(pokemon_id, new_number, pokemon_page, list_of_links):
    g1 = '/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g1)
    # elif (i <= 251):
    g2 = '-gs/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g2)
    # elif (i <= 386):
    g3 = '-rs/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g3)
    # elif (i <= 493):
    g4 = '-dp/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g4)
    # elif (i <= 649):
    g5 = '-bw/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g5)
    # elif (i <= 721):
    g6 = '-xy/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g6)
    # elif (i <= 809):
    g7 = '-sm/' + new_number + '.shtml'
    list_of_links.append(pokemon_page + g7)
    g8_name = get_name_from_dex_number(pokemon_id).lower()
    g8 = '-swsh/' + g8_name
    list_of_links.append(pokemon_page + g8)

    return list_of_links

def generate_locations_csv():
    rows = [['pokemon_id','red_location', 'blue_location', 'yellow_location', 
    'gold_location', 'silver_location', 'crystal_location', 
    'ruby_location', 'sapphire_location', 'emerald_location', 'fr_location', 'lg_location', 
    'diamond_location', 'pearl_location', 'platinum_location', 'hg_location', 'ss_location',
    'black_location', 'white_location', 'black2_location', 'white2_location', 
    'x_location', 'y_location', 'or_location', 'as_location',
    'sun_location', 'moon_location', 'ultra_sun_location', 'ultra_moon_location',
    'sword_location', 'shield_location', 'brilliant_diamond_location', 'shining_pearl_location', 'pla_location']]
    for i in range(900, 906, 1):
        new_number = str(i).zfill(3)
        pokemon_id = str(i)
        pokemon_page = 'https://www.serebii.net/pokedex'
        my_links = list_of_links_generator(i, new_number, pokemon_page, [])
        
        gen1_dict = parse_location(my_links[0], ['firered'], 4, True, 0, False)
        red_location = gen1_dict['game0']
        blue_location = gen1_dict['game1']
        yellow_location = gen1_dict['game2']
        sleep(random.randint(0,3))
        gen2_dict = parse_location(my_links[1], ['heartgold'], 3, False, 0, False)
        gold_location = gen2_dict['game0']
        silver_location = gen2_dict['game1']
        crystal_location = gen2_dict['game2']        
        sleep(random.randint(0,3))
        gen3_dict = parse_location(my_links[2], ['ruby'], 5, False, 1, False)
        ruby_location = gen3_dict['game0']
        sapphire_location = gen3_dict['game1']
        emerald_location = gen3_dict['game2']
        fr_location = gen3_dict['game3']
        lg_location = gen3_dict['game4']         
        sleep(random.randint(0,3))
        gen4_dict = parse_location(my_links[3], ['diamond'], 5, False, 1, False)
        diamond_location = gen4_dict['game0']
        pearl_location = gen4_dict['game1']
        platinum_location = gen4_dict['game2']
        hg_location = gen4_dict['game3']
        ss_location = gen4_dict['game4']         
        sleep(random.randint(0,3))
        gen5_dict = parse_location(my_links[4], ['fooblack'], 4, False, 0, False)
        black_location = gen5_dict['game0']
        white_location = gen5_dict['game1']
        black2_location = gen5_dict['game2']
        white2_location = gen5_dict['game3']
        sleep(random.randint(0,3))
        gen6_dict = parse_location(my_links[5], ['foox'], 4, False, 0, False)
        x_location = gen6_dict['game0']
        y_location = gen6_dict['game1']
        or_location = gen6_dict['game2']
        as_location = gen6_dict['game3']
        sleep(random.randint(0,3))
        gen7_dict = parse_location(my_links[6], ['foosun'], 4, False, 0, False)
        sun_location = gen7_dict['game0']
        moon_location = gen7_dict['game1']
        ultra_sun_location = gen7_dict['game2']
        ultra_moon_location = gen7_dict['game3']
        sleep(random.randint(0,3))
        gen8_dict = parse_location(my_links[7], ['fooeevee', 'foox', 'diamond'], 5, False, 0, True)
        pla_location = gen8_dict['game0']
        sword_location = gen8_dict['game1']
        shield_location = gen8_dict['game2']
        brilliant_diamond_location = gen8_dict['game3']
        shining_pearl_location = gen8_dict['game4']
        sleep(random.randint(0,3))

        rows.append([pokemon_id,red_location, blue_location, yellow_location, 
        gold_location, silver_location, crystal_location, 
        ruby_location, sapphire_location, emerald_location, fr_location, lg_location, 
        diamond_location, pearl_location, platinum_location, hg_location, ss_location,
        black_location, white_location, black2_location, white2_location, 
        x_location, y_location, or_location, as_location,
        sun_location, moon_location, ultra_sun_location, ultra_moon_location,
        sword_location, shield_location, brilliant_diamond_location, shining_pearl_location, pla_location])

        with open('csv_files/locations_temp.csv', 'w', encoding="utf-8", newline='') as f_output:
            csv_output = csv.writer(f_output)
            csv_output.writerows(rows)
generate_locations_csv()


# parse_location('https://www.serebii.net/pokedex-dp/' + str(14).zfill(3) + '.shtml', ['diamond'], 5, False, 1, False)
# parse_location('https://www.serebii.net/pokedex/' + str(151).zfill(3) + '.shtml', ['firered'], 4, True, 0, False)
# parse_location('https://www.serebii.net/pokedex-gs/' + str(152).zfill(3) + '.shtml', ['heartgold'], 3, False, 0, False)
# parse_location('https://www.serebii.net/pokedex-rs/' + str(386).zfill(3) + '.shtml', ['ruby'], 5, False, 1, False)
# parse_location('https://www.serebii.net/pokedex-bw/' + str(510).zfill(3) + '.shtml', ['fooblack'], 4, False, 0, False)
# parse_location('https://www.serebii.net/pokedex-xy/' + str(705).zfill(3) + '.shtml', ['foox'], 4, False, 0, False)
# parse_location('https://www.serebii.net/pokedex-sm/' + str(736).zfill(3) + '.shtml', ['foosun'], 4, False, 0, False)
# gen8_name = get_name_from_dex_number(895).lower()
# print(gen8_name)
# parse_location('https://www.serebii.net/pokedex-swsh/' + gen8_name + '/', ['fooeevee', 'foox', 'diamond'], 5, False, 0, True)
