from bs4 import BeautifulSoup
import requests 
import datetime
import pandas as pd 
from dateutil import parser
from dateutil.relativedelta import relativedelta
import pokebot_parser
import difflib
# added a comment

seasons_url = 'https://www.serebii.net/pokemongo/seasons.shtml'
event_url = 'https://www.serebii.net/pokemongo/events.shtml'
general_url = 'https://www.serebii.net/pokemongo/'
current_event_url = ''
pogo_news_url = 'https://pokemongolive.com/en/news/'

today = datetime.datetime.now()
all_seasons_page = requests.get(seasons_url)
all_seasons_soup = BeautifulSoup(all_seasons_page.content, "html.parser")
all_seasons_table = all_seasons_soup.find(text = 'Duration').findPrevious(attrs={'class':'dextab'})
seasons = all_seasons_table.find_all('tr')[1:]

all_events_page = requests.get(event_url)
all_events_soup = BeautifulSoup(all_events_page.content, "html.parser")
all_events_table = all_events_soup.find(text = 'Duration').findPrevious(attrs={'class':'dextab'})
events = all_events_table.find_all('tr')[1:]

def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end

def get_season_soup():
    for item in seasons:
        event_info = item.findAll(attrs={'class':'fooinfo'})

        dates = event_info[1].text.strip()
        event_url = event_info[0].find('a')['href']
        
        dates_lst = dates.split(' - ')
        start = dates_lst[0]
        end = dates_lst[1]

        start = start.split(" ")
        end = end.split(" ")

        start[1] = ''.join(filter(str.isdigit, start[1]))
        end[1] = ''.join(filter(str.isdigit, end[1]))

        start = " ".join(start)
        end = " ".join(end)

        start_object = datetime.datetime.strptime(start,'%B %d %Y')
        end_object = datetime.datetime.strptime(end,'%B %d %Y')
        
        if (time_in_range(start_object, end_object, today)) == True:
            current_event_url = general_url + event_url
            current_event_page = requests.get(current_event_url)
            current_event_soup = BeautifulSoup(current_event_page.content, "html.parser")
            return current_event_soup
    return 

def get_season_table(soup, selection_text):
    table = soup.find(text = selection_text).findNext(attrs={'class':'dextab'})
    table_rows = table.findAll('tr')[1:]
    res = []
    for tr in table_rows:
        row = []
        td_num_img_type = tr.findAll('td', attrs={'class':'cen'})
        td_name = tr.findAll('td', attrs = {'class':'fooinfo'})
        if (len(td_num_img_type) > 0):
            num = td_num_img_type[0].text.strip()
            row.append(num)
            name = td_name[0].text.strip()
            row.append(name)
            pokemon_type_links = td_num_img_type[2].select('img')
            if (len(pokemon_type_links) == 1):
                type_1_link = pokemon_type_links[0]['src'].replace(".gif", "")
                type_1_last_slash = type_1_link.rfind("/") + 1
                type_1 = type_1_link[type_1_last_slash:].capitalize()
                row.append(type_1)
            elif (len(pokemon_type_links) == 2):
                type_1_link = pokemon_type_links[0]['src'].replace(".gif", "")
                type_2_link = pokemon_type_links[1]['src'].replace(".gif", "")

                type_1_last_slash = type_1_link.rfind("/") + 1
                type_2_last_slash = type_2_link.rfind("/") + 1

                type_1 = type_1_link[type_1_last_slash:].capitalize()
                type_2 = type_2_link[type_2_last_slash:].capitalize()
                type_str = type_1 + "/" + type_2
                row.append(type_str)
            res.append(row)
    df = pd.DataFrame(res, columns=["No.", "Name", "Type"])
    df_prime = df.to_string(index = False)
    return df_prime

def get_name(soup):
    try:
        first_table = soup.find('table', attrs={'class':'tab'})
    except:
        return 
    name = first_table.find('td', attrs = {'class':'fooleft'}).text.strip()
    return name

def contains_time(date_list):
    time_str = ':'
    for i in range(len(date_list)):
        if time_str in date_list[i]:
            return True, i 
    return False, 0

def contains_day(date_list):
    days_lst = ['00', '01', '02', '03', '04', '05', '06', '07', 
    '08', '09', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', 
    '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', 
    '30', '31']
    for i in range(len(date_list)):
        if date_list[i] in days_lst:
            return True, date_list[i] 
    return False, 'No Day Found' 

def contains_month(date_list):
    months_lst = ['January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December']
    for i in range(len(date_list)):
        if date_list[i] in months_lst:
            return True, date_list[i]
    return False, 'No Month Found' 

def contains_year(date_list):
    for i in range(len(date_list)):
        if date_list[i].startswith("2") and (len(date_list[i]) == 4):
            return True, date_list[i] 
    return False, 'No Year Found' 

def get_event_soup():
    for item in events:
        event_info = item.findAll(attrs={'class':'fooinfo'})
        dates = event_info[1].text.strip()
        event_url = event_info[0].find('a')['href']
        dates_lst = dates.split(' - ')
        try:
            if len(dates_lst) > 1:
                # print("more than one day: ", dates_lst)
                start = dates_lst[0]
                end = dates_lst[1]
            else:
                # print("Single DAY ONLY: ", dates_lst)
                continue 
        except:
            print("not found: ", item)
            continue 
        # print("initially end: ", end)
        # print("initially start: ", start)
        try:
            year = parser.parse(end).year
        except:
            continue 
        start = start.split(" ")
        if (len(start) < 3):
            start.append(str(year))
        end = end.split(" ")

        start_time_tup = contains_time(start)
        end_time_tup = contains_time(end)
        if (start_time_tup[0] == True):
            start.pop(start_time_tup[1])
            if len(start) == 0:
                continue 
        if (end_time_tup[0] == True):
            end.pop(end_time_tup[1])
            if len(end) == 0:
                continue 
        
        # Fill in missing months or years, or remove times
        start[1] = ''.join(filter(str.isdigit, start[1]))
        end[1] = ''.join(filter(str.isdigit, end[1]))

        start_day_tup = contains_day(start)
        start_month_tup = contains_month(start)
        start_year_tup = contains_year(start)

        end_day_tup = contains_day(end)
        end_month_tup = contains_month(end)
        end_year_tup = contains_year(end)

        # you want there to be a day in there, skip if no date
        if start_day_tup[0] == False:
            continue  
        if end_day_tup[0] == False:
            continue   
        if start_month_tup[0] == False:
            start.insert(0, end_month_tup[1])
        if end_month_tup[0] == False:
            end.insert(0, start_month_tup[1])
        if start_year_tup[0] == False:
            start.insert(2, end_year_tup[1])
        if end_year_tup[0] == False:
            end.insert(2, start_year_tup[1])

        start = " ".join(start)
        end = " ".join(end)
        
        # by this point, need a string that's been formatted correctly
        start_object = datetime.datetime.strptime(start,'%B %d %Y')
        end_object = datetime.datetime.strptime(end,'%B %d %Y')
        if (time_in_range(start_object, end_object, today)) == True:
            print("time_in_range conditional entered ", start_object, end_object)
            current_event_url = general_url + event_url
            current_event_page = requests.get(current_event_url)
            current_event_soup = BeautifulSoup(current_event_page.content, "html.parser")
            return current_event_soup

def get_event_table(soup, selection_text):
    try:
        table = soup.find(text = selection_text).findNext(attrs={'class':'dextab'})
    except:
        return "No Current Event"
    table_rows = table.findAll('tr')[1:]
    res = []
    for tr in table_rows:
        row = []
        td_num_img_type = tr.findAll('td', attrs={'class':'cen'})
        td_name = tr.findAll('td', attrs = {'class':'fooinfo'})
        if (len(td_num_img_type) > 0):
            num = td_num_img_type[0].text.strip()
            row.append(num)
            name = td_name[0].text.strip()
            row.append(name)
            pokemon_type_links = td_num_img_type[2].select('img')
            if (len(pokemon_type_links) == 1):
                type_1_link = pokemon_type_links[0]['src'].replace(".gif", "")
                type_1_last_slash = type_1_link.rfind("/") + 1
                type_1 = type_1_link[type_1_last_slash:].capitalize()
                row.append(type_1)
            elif (len(pokemon_type_links) == 2):
                type_1_link = pokemon_type_links[0]['src'].replace(".gif", "")
                type_2_link = pokemon_type_links[1]['src'].replace(".gif", "")

                type_1_last_slash = type_1_link.rfind("/") + 1
                type_2_last_slash = type_2_link.rfind("/") + 1

                type_1 = type_1_link[type_1_last_slash:].capitalize()
                type_2 = type_2_link[type_2_last_slash:].capitalize()
                type_str = type_1 + "/" + type_2
                row.append(type_str)
            res.append(row)
    df = pd.DataFrame(res, columns=["No.", "Name", "Type"])
    df_prime = df.to_string(index = False)
    return df_prime

def get_pogo_season_string():
    current_season_soup = get_season_soup()
    current_season_name = get_name(current_season_soup)
    current_season_table = get_season_table(current_season_soup, "Northern Hemisphere Spawns")
    return current_season_name + "\n" + current_season_table + "\n"

def get_pogo_event_string():
    event_soup = get_event_soup()
    event_name = get_name(event_soup)
    current_event_table = get_event_table(event_soup, "Specific Pokémon")
    return event_name + "\n" + current_event_table  + "\n"

def get_pogo_general_string():
    season_info = get_pogo_season_string()
    event_info = get_pogo_event_string()
    return season_info + "\n" + event_info + "\n"

def get_next_raids():
    news_page = requests.get(pogo_news_url)
    news_soup = BeautifulSoup(news_page.content, "html.parser")
    current_month = today.month()

#NOTE:Updated Code, 9/14/22
#  features to add:
    # What does ___'s shiny look like? https://pokemondb.net/pokedex/shiny
    # Use serebii for all the pogo info you need 
# What's the next pokemon Go event? 

def dct_to_string(dct):
    ''' 
    convert a dictionary to some output string
    '''
    my_str = ''
    i = 0
    for key in dct:
        if (i < len(dct)): 
            my_str += str(dct[key]) + '\n'
        else:
            my_str += str(dct[key])
    return my_str 

def pogo_events_output():
    url = 'https://www.serebii.net/pokemongo/events.shtml'
    serebii_url = 'https://www.serebii.net/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    latest_events = soup.find(attrs = {'class':'dextab'}).findAll('tr')[1:3]
    test_dict = {}
    final_str = 'Here are the two most recent events: \n'
    latest_events

    i = 0
    for item in latest_events:
        event_details = item.findAll('td')
        # event_details should have 3 entries, event image,name, and dates
        try:
            image_details = event_details[0].find('img')
            image = serebii_url + image_details['src']
        except:
            image = 'No image found'
        try:    
            name = event_details[1].text.strip()
        except:
            name = "No event name found"
        try:
            dates = event_details[2].text.strip()
        except:
            dates = "No dates range found"
        test_dict['image' + str(i)] = image 
        test_dict['name' + str(i)] = name
        test_dict['dates' + str(i)] = dates
        i += 1
        # final_str += dct_to_string(test_dict)
    return test_dict

# Searches page for most recent research breakthrough
def get_most_recent_research_breakthroughs():
    url = 'https://www.serebii.net/pokemongo/fieldresearch.shtml'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        research_breakthrough = soup.find(text = "Field Research List").findPrevious('p').findNext('div').find('li')
        date = research_breakthrough.get("title")
        pokemon = research_breakthrough.find('td', attrs = {'class':'pkmn'}).findNext('td').text.strip()
        ret_str = "Here's the most recent one I could find: \n" + date + " | " + pokemon
        return ret_str 
    except:
        ret_str = "I'm not sure!"
        return ret_str

def has_passed(date):
    # need to remove ending of day
    date = date.split(" ")
    date[1] = ''.join(filter(str.isdigit, date[1]))

    date = " ".join(date)
    date_obj = datetime.datetime.strptime(date,'%B %d %Y')

    return not (today <= date_obj) 

def get_spotlight_hour_info(check_next):
    url = 'https://www.serebii.net/pokemongo/events/spotlighthour.shtml'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find('table', attrs = {'class':'dextab'})
    dates = table.findAll('tr')[1:9]
    dates_lst = []
    dates_obj_lst = []
    pokemon_lst = []
    effects_lst = []

    for date in dates:
        final_date = date.findAll('td')[0].text.strip()
        pokemon = date.findAll('td')[1].text.strip()
        effect = date.findAll('td')[2].text.strip()

        dates_lst.append(final_date)
        pokemon_lst.append(pokemon)
        effects_lst.append(effect)
    
    if (check_next == False):
        ret_str = 'Here are some of the most recent ones I could find: \n'
        for i in range(len(dates_lst)):
            date = dates_lst[i]
            name = pokemon_lst[i]
            effect = effects_lst[i]
            if (i < len(dates_lst) - 1):
                ret_str += date + " | " + name + " | " + effect + '\n' 
            else:
                ret_str += date + " | " + name + " | " + effect
        return ret_str 

    for date in dates_lst:

        date = date.split(" ")
        date[1] = ''.join(filter(str.isdigit, date[1]))
        date = " ".join(date)
        date_obj = datetime.datetime.strptime(date,'%B %d %Y')
        dates_obj_lst.append(date_obj)
    
    # https://www.geeksforgeeks.org/python-find-the-closest-date-from-a-list/
    res = min(dates_obj_lst, key=lambda sub: abs(sub - today))
    idx = dates_obj_lst.index(res)
    
    res = res.strftime("%B %d %Y")
    final_str = "The next spotlight hour is: \n" + res + ' | ' + pokemon_lst[idx] + ' | ' + effects_lst[idx]
    return final_str 

def get_star_search_string(message):
    raids_star_lst = ['5 star', '5-star', 'five star', 'mega raids', '4-star', '4 star', 'four star', 
    '3-star', '3 star', 'three star', '2-star', '2 star', 'two star', '1-star', '1 star', 'one star']
    # output closest match

    raids_dct = {'5 star':'☆☆☆☆☆ List', '5-star':'☆☆☆☆☆ List', 'five star':'☆☆☆☆☆ List', 'mega raids':'Mega Raid List', '4-star':'☆☆☆☆ List', '4 star':'☆☆☆☆ List', 'four star':'☆☆☆☆ List', 
    '3-star':'☆☆☆ List', '3 star':'☆☆☆ List', 'three star':'☆☆☆ List', '2-star':'☆☆ List', '2 star':'☆☆ List', 'two star':'☆☆ List', '1-star':'☆ List', '1 star':'☆ List', 'one star':'☆ List'}
    # use closest match to get search string from raids_dct

    n = 1
    cutoff = 0.9
    message = message.replace(" ", "")
    result = [message[i: j] for i in range(len(message))
        for j in range(i + 1, len(message) + 1)]

    substring_list = []
    for substring in result:
        close_matches = difflib.get_close_matches(substring, raids_star_lst, n, cutoff)
        if (len(close_matches) > 0):
            substring_list.append(close_matches[0])
    key = substring_list[0]

    search_string = raids_dct[key]
    return search_string
    # use search string to get pokemon for each raid type

def get_current_raid_info(message):
    search_string = get_star_search_string(message)
    raid_url = 'https://www.serebii.net/pokemongo/raidbattles.shtml'
    page = requests.get(raid_url)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        table = soup.find(text = search_string).findNext('table', attrs = {'class':'dextab'}).find_all('tr')[1:]
    except:
        return "I'm not sure"
    ret_str = ''
    for element in table: 
        lst_num = element.findAll('td', attrs = {'class':'cen'})
        lst_name = element.findAll('td', attrs = {'class':'fooinfo'})
        if (len(lst_num) > 0):
            num = lst_num[0].text.strip()
            ret_str += num + ' | '
        if (len(lst_name) > 0):
            try:
                extra_info = lst_name[0].find('i').text.strip()
                name = lst_name[0].find('a').text.strip()
                ret_str += name + ' | '
                ret_str += extra_info + '\n'
            except:
                name = lst_name[0].find('a').text.strip()
                ret_str += name + '\n' 
    return ret_str 

def get_comm_day_info(check_next):
    url = 'https://www.serebii.net/pokemongo/communityday.shtml'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    current_month_year = today.strftime("%B %Y")
    
    next_month_year = (today + relativedelta(months=1)).strftime('%B %Y')

    current_month_comm_day = soup.find(text = current_month_year).findNext('td').text.strip()
    name = soup.find(text = current_month_year).findNext('td').findNext('td').text.strip()

    if (check_next):
        if (has_passed(current_month_comm_day)):
            try:
                # it's passed and has been announced
                next_comm_day = soup.find(text = next_month_year).findNext('td').text.strip()
                name = soup.find(text = next_month_year).findNext('td').findNext('td').text.strip()
                ret_str = name + '\n' + next_comm_day
                return ret_str 
            except:
                # it's passed but haven't announced it yet
                ret_str = "I'm not sure, I can just find the one this month: \n" + name + '\n' + current_month_comm_day
                return ret_str 
        else:
            # hasn't passed yet
            next_comm_day = current_month_comm_day
            ret_str = name + '\n' + next_comm_day
            return ret_str 
    else:
        ret_str = name + '\n' + current_month_comm_day
        return ret_str  