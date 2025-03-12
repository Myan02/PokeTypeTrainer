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

# give the user information about certain types
def run_type_directory(matchups):
   
   is_running = True

   # press q to quit the game
   while(is_running):
      current_type = input('Which type do you want to learn about?\n').lower()
      
      # make sure to type accurately
      if current_type == 'q':
            break
         
      elif current_type not in list(matchups.keys()):
            print('that type doesn\'t exist, try again...')
            continue
      
      # get type relations about the current type
      super_effective_against_type = [relation['name'] for relation in matchups[current_type]['double_damage_from']]  
      half_effective_against_type = [relation['name'] for relation in matchups[current_type]['half_damage_from']]
      not_effective_against_type = [relation['name'] for relation in matchups[current_type]['no_damage_from']]
      
      super_effective_to_type =  [relation['name'] for relation in matchups[current_type]['double_damage_to']]
      half_effective_to_type = [relation['name'] for relation in matchups[current_type]['half_damage_to']]
      not_effective_to_type = [relation['name'] for relation in matchups[current_type]['no_damage_to']]
      
      
      print(f'\nyou chose: {current_type} \n' +
            f'{current_type} is weak against {super_effective_against_type}\n' + 
            f'{current_type} is strong against {half_effective_against_type}\n' +
            f'{current_type} takes no damage against {not_effective_against_type}\n\n' +
            f'{current_type} deals double damage against {super_effective_to_type}\n' +
            f'{current_type} deals half damage against {half_effective_to_type}\n' + 
            f'{current_type} deals no damage against {not_effective_to_type}\n')
            
   

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
      
   app_running = True
   
   while(app_running):
      
      user_input = input('welcome to the poke type trainer. Please select 1 to run the trainer, 2 to get help, and anything else to quit... ')

      match user_input:
         case '1':
            run_trainer(matchups=matchups)
            
         case '2':
            run_type_directory(matchups=matchups)
            
         case _:
            break
      
   

if __name__ == '__main__':
   main()

