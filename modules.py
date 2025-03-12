from requests import get

# keeps track of game states for player
class App:
   states = {
      'closed' : 0,
      'menu'   : 1,
      'runner' : 2
   }
   current_state = states['closed']
   
   curr_score = 0
   max_score = 0
   
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
   
   
   # update the state when the player interacts with the menu
   @classmethod
   def change_state(cls, state):
      cls.current_state = cls.states[state]
      
   # increase or decrease the score based on the current combo
   @classmethod
   def update_score(cls, score):
      cls.curr_score += score * cls.current_combo

   # increase the combo multiplier once player has enough combo
   @classmethod
   def increase_combo(cls):
      cls.current_combo = cls.combos[cls.current_combo_index]
   
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
   
   # return the player's max score
   @classmethod
   def get_highscore(cls):
      return cls.max_score

# Retrieve information about pokemon
class Pokemon:
   
   # returns a list containing information about each type as a dict
   types_r = get('https://pokeapi.co/api/v2/type').json()['results']
   
   @classmethod
   def get_type_info_r(cls) -> dict:
      
      matchups = {}
      for entry in cls.types_r:
         # name of the current type (ie. normal, fighting, rock, etc)
         type_name = entry['name']
         
         # skip over stellar and unknown types
         if type_name == 'stellar' or type_name == 'unknown':
            continue
      
         # get information about the current type
         type_info_request = get(f'https://pokeapi.co/api/v2/type/{type_name}').json()
         
         # populate a table with all damage relations to the current type, ie:
         '''
            rock : 
               double_damage_from (this type is super effective against rock): fighting, ground, water, etc
               double_damage_to (rock types deal super effective damage aginst this type): flying, bug, etc
               etc
         '''
         matchups[type_name] = type_info_request['damage_relations']
         
      return matchups

   