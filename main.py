from random import choice
from requests import get

# retrieve information about type matchups as a table
def get_type_info_r() -> dict:
   
   # returns a list containing information about each type as a dict
   types_request = get('https://pokeapi.co/api/v2/type').json()['results']
   
   matchups = {}
   for entry in types_request:
      # name of the current type (ie. normal, fighting, rock, etc)
      type_name = entry['name']
      
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
   

# main game
def run_trainer(matchups):
   
   is_running = True

   # press q to quit the game
   while(is_running):
   
      # pick a type at random and assign all weaknesses of that type to a list
      current_type = choice(list(matchups.keys()))
      current_answers = [relation['name'] for relation in matchups[current_type]['double_damage_from']]  
      
      # get the user's answer
      user_choice = input(f'{current_type} is weak against... \n\n')
      
      if user_choice.lower() == 'q':
         break
      
      # as long as the user inputs one weakness correctly, they move on
      if user_choice in current_answers:
         print('\n\nthat\'s correct! Next up:')
      else:
         print(f'\n\nsorry, that\'s incorrect. {current_type} is actually weak against {current_answers}')


def main():
   
   matchups = get_type_info_r()

   run_trainer(matchups=matchups)
      

if __name__ == '__main__':
   main()


'''
def run_type_directory(matchups):
   
   is_running = True

   while(is_running):
      user_input = input('Which type do you want to learn about?\n').lower()
      
      if user_input not in matchups.keys():
            print('that type doesn\'t exist, try again...')
            continue
         
      elif user_input == 'q':
            break
      
      current_type = matchups[user_input]
      current_answers = [relation['name'] for relation in matchups[current_type]['double_damage_from']]  
      
      print(f'\nyou chose: {current_type} \n' +
            f'{current_type} is weak against {current_answers}\n')
'''