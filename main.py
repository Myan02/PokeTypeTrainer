from random import choice as pick_one, shuffle as shuffle_list
from requests import get

# retrieve information about type matchups as a table
def get_type_info_r() -> dict:
   
   # returns a list containing information about each type as a dict
   types_request = get('https://pokeapi.co/api/v2/type').json()['results']
   
   matchups = {}
   for entry in types_request:
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
   multiple_choice = True
   
   '''
   go back and add error handling to all user input decisions
   '''
   # give the user the choice between multiple choice questions and responses
   user_input = input('would you like multiple choice or to type your answers? type m for multiple choice and t for typing... ').lower()
   
   if user_input == 'm':
      multiple_choice = True
   elif user_input == 't':
      multiple_choice = False

   # press q to quit the game
   while(is_running):
   
      # pick a type at random and assign all weaknesses of that type to a list
      current_type = pick_one(list(matchups.keys()))
      current_answers = [relation['name'] for relation in matchups[current_type]['double_damage_from']]  
      
      # run this if there are multiple choice responses
      if multiple_choice:
         number_of_choices = 4
         
         # populate a list with all choices
         choices_available = []
         for choice_index in range(number_of_choices):
            
            # place the answer at index 0
            if choice_index == 0:
               choices_available.append(pick_one(current_answers))
               
            # place wrong answers at index 1-3
            else:
               choices_available.append(pick_one([rand_type for rand_type in list(matchups.keys()) if rand_type not in current_answers and rand_type not in choices_available]))
            
         # shuffle the list so the right answer isn't always at index 0
         shuffle_list(choices_available)
         
         print(f'{current_type} is weak against...\n')
      
         # print options
         for choice_index in range(number_of_choices):
            print(f'{choice_index + 1}. {choices_available[choice_index]}')
         print()
      
         # get the user's answer
         user_choice = input(f'your answer... ')
         
         if user_choice.lower() == 'q':
            break
         
         # convert the user input into the type they chose
         user_choice = choices_available[int(user_choice) - 1]
         
         # check if their answer is correct or not
         if user_choice in current_answers:
            print('\nthat\'s correct! Next up:\n')
         else:
            print(f'\nsorry, that\'s incorrect. {current_type} is actually weak against {current_answers}\n')
         
         # clear the available choices for the next question
         choices_available.clear()
      
      elif multiple_choice == False:
         # get the user's answer
         user_choice = input(f'{current_type} is weak against... ').lower()
         
         if user_choice == 'q':
            break
         
         # as long as the user inputs one weakness correctly, they move on
         if user_choice in current_answers:
            print('\nthat\'s correct! Next up:\n')
         else:
            print(f'\nsorry, that\'s incorrect. {current_type} is actually weak against {current_answers}\n')


def main():
   
   matchups = get_type_info_r()
      
   app_running = True
   
   while(app_running):
      
      user_input = input('welcome to the poke type trainer. Please select 1 to run the trainer, 2 to get help, and anything else to quit... ')
      print()
      
      match user_input:
         case '1':
            run_trainer(matchups=matchups)
            
         case '2':
            run_type_directory(matchups=matchups)
            
         case _:
            break
      
   

if __name__ == '__main__':
   main()

