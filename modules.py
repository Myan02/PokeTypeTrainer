from requests import get
import os

# keeps track of game states for player
class Score:
   
   # local score and highscore to store for that user
   curr_score = 0
   max_score = 0
   
   # combo multipliers, higher combo equals higher point multiplier
   # key = number of questions right in a row
   # value = combo multiplier
   combos = {
      0: 1.0,
      3: 1.1,
      5: 1.5,
      7: 1.7, 
      10: 2.0,
      15: 2.2
   }
   current_combo_index = 0
   current_combo = combos[current_combo_index]
   
   # if the highscore file doesnt exist, create it
   @classmethod
   def initialize_highscore(cls):
      if os.path.exists('./gui/highscore.txt'):
         cls.max_score = cls.retrieve_highscore_file()
      else:
         cls.update_highscore_file()
   
   # increase or decrease the score based on the current combo
   @classmethod
   def update_score(cls, score):
      cls.curr_score += score * cls.current_combo

   # increase the combo multiplier once player has enough combo
   @classmethod
   def increase_combo(cls):
      cls.current_combo_index += 1
      
      match cls.current_combo_index:
               case 3:
                  cls.current_combo = cls.combos[cls.current_combo_index]
               case 5:
                  cls.current_combo = cls.combos[cls.current_combo_index]
               case 7:
                  cls.current_combo = cls.combos[cls.current_combo_index]
               case 10:
                  cls.current_combo = cls.combos[cls.current_combo_index]
               case 15:
                  cls.current_combo = cls.combos[cls.current_combo_index]
               case _:
                  pass
   
   # increment for every continous right answer
   @classmethod
   def update_combo_index(cls):
      cls.current_combo_index += 1

   # return the player's current combo value
   @classmethod
   def get_combo_index(cls):
      return cls.current_combo_index
      
   # reset the combo multiplier
   @classmethod
   def reset_combo(cls):
      cls.current_combo_index = 0
      cls.current_combo = cls.combos[cls.current_combo_index]

   # return the players current score
   @classmethod
   def get_score(cls):
      return cls.curr_score
   
   # reset the player's score
   @classmethod
   def reset_score(cls):
      cls.curr_score = 0
   
   # set the players max score if they achieved a personal best
   @classmethod
   def set_highscore(cls):
      if cls.curr_score > cls.max_score:
         cls.max_score = cls.curr_score
         
   # create and initialize a file to keep highscores
   @classmethod
   def update_highscore_file(cls):
      try:
         with open('./gui/highscore.txt', 'w') as file:
            file.write(str(int(cls.get_highscore())))
      except Exception as e:
         print(f'unable to write to file, error {e}')
   
   # return the player's max score
   @classmethod
   def get_highscore(cls):
      return cls.max_score
   
   # retrieve highscore from file
   @classmethod
   def retrieve_highscore_file(cls):
      try:
         with open('./gui/highscore.txt', 'r') as file:
            return int(file.read())
      except Exception as e:
         print(f'unable to read from file, error {e}')

   

# retrieve information about pokemon
class Pokemon:
   
   # retrieve a pokemon as a Pokemon object
   def __init__(self):
      pass
   
   @classmethod
   def get_type_info_r(cls) -> dict:
      
      # returns a list containing information about each type as a dict
      response = get('https://pokeapi.co/api/v2/type')
      
      # check to make sure HTTP request went through properly
      if response.status_code == 200:
         types_r = response.json()['results']
      else:
         raise Exception(f'pokemon types not retrieved properly, status code {response.status_code}')
         
      matchups = {}
      for entry in types_r:
         # name of the current type (ie. normal, fighting, rock, etc)
         type_name = entry['name']
         
         # skip over stellar and unknown types
         if type_name == 'stellar' or type_name == 'unknown':
            continue
      
         # get information about the current type
         request = get(f'https://pokeapi.co/api/v2/type/{type_name}')
         
         if request.status_code == 200:
            type_info_request = request.json()
         else:
            raise Exception(f'unable to retrieve type information for pokemon type {type_name}, status code {response.status_code}')
         
         
         # populate a table with all damage relations to the current type, ie:
         '''
            rock : 
               double_damage_from (this type is super effective against rock): fighting, ground, water, etc
               double_damage_to (rock types deal super effective damage aginst this type): flying, bug, etc
               etc
         '''
         matchups[type_name] = type_info_request['damage_relations']
         
      return matchups

   