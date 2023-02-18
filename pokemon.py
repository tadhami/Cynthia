import pandas as pd 
import csv 
import pokebot_parser
from pprint import pprint

class Pokemon:
    def __init__(self):
        pass
def populate_pokemon(self, name):
    self.name = name
    
    dex_num = pokebot_parser.dex_num_extractor(name)
    self.dex_num = dex_num 

    pokemon_file = pd.read_csv("csv_files/Pokemon_data.csv")
    pokemon_df = pd.DataFrame(pokemon_file)
    pokemon_df.set_index("name", inplace = True)

    self.generation = pokemon_df.loc[self.name, 'generation']
    self.classification = pokemon_df.loc[self.name, 'classification']
    self.abilities = pokemon_df.loc[self.name, 'abilities']
    self.height_m = pokemon_df.loc[self.name, 'height_m']
    self.weight_kg = pokemon_df.loc[self.name, 'weight_kg']
    self.types = pokebot_parser.type_extractor(self.name, 1)[0:1]
    self.weaknesses = pokebot_parser.weaknesses(pokebot_parser.type_extractor(self.name, 0))
    self.strengths = pokebot_parser.strengths(pokebot_parser.type_extractor(self.name, 0))
    self.base_total = pokemon_df.loc[self.name, 'base_total'] 
    self.hp = pokemon_df.loc[self.name, 'hp'] 
    self.attack = pokemon_df.loc[self.name, 'attack'] 
    self.defense = pokemon_df.loc[self.name, 'defense'] 
    self.sp_attack = pokemon_df.loc[self.name, 'sp_attack']
    self.sp_defense = pokemon_df.loc[self.name, 'sp_defense'] 
    self.speed = pokemon_df.loc[self.name, 'speed']
    self.capture_rate = pokemon_df.loc[self.name, 'capture_rate']
    self.base_egg_steps = pokemon_df.loc[self.name, 'base_egg_steps']
    self.base_happiness = pokemon_df.loc[self.name, 'base_happiness']
    self.is_legendary = pokemon_df.loc[self.name, 'is_legendary']
    self.is_mythical = pokemon_df.loc[self.name, 'is_mythical']
    self.cur_moves = 'None for now' 
    self.all_moves = 'None for now'
    try:
        self.evolution_criteria = pokebot_parser.obtain_evolution_output(self.name)
    except:
        self.evolution_criteria = "Doesn't evolve"

def all_string_builder(self):
    out = ''
    out += "National Dex number: " + str(self.dex_num) + '\n'
    out += "Name: " + str(self.name) + '\n'
    out += "Generation: " + str(self.generation) + '\n'
    out += "Classification: " + str(self.classification) + '\n'
    out += "Abilities: " + str(self.abilities) + '\n'
    out += "Height: " + str(self.height_m) + '\n'
    out += "Weight: " + str(self.weight_kg) + '\n'
    out += "Type: " + str(self.types) + '\n'
    out += "Weaknesses:\n " + str(self.weaknesses) + '\n'
    out += "Strengths:\n " + str(self.strengths) + '\n'
    out += "Base total: " + str(self.base_total) + '\n'
    out += "HP: " + str(self.hp) + '\n'
    out += "Attack: " + str(self.attack) + '\n'
    out += "Defense: " + str(self.defense) + '\n'
    out += "Special Attack: " + str(self.sp_attack) + '\n'
    out += "Special Defense: " + str(self.sp_defense) + '\n'
    out += "Speed: " + str(self.speed) + '\n'
    out += "Capture Rate: " + str(self.capture_rate) + '\n'
    out += "Base egg steps: " + str(self.base_egg_steps) + '\n'
    out += "Base Happiness: " + str(self.base_happiness) + '\n'
    out += "Legendary: " + str(self.is_legendary) + '\n'
    out += "Mythical: " + str(self.is_mythical) + '\n'
    out += "Current moves: " + self.cur_moves + '\n'
    out += "All moves it can learn: " + self.all_moves + '\n'
    out += "Evolution Criteria: " + self.evolution_criteria 
    return out 
