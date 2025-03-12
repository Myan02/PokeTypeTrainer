from random import choice as pick_one, shuffle as shuffle_list
from modules import App

# give the user information about certain types
def type_directory(matchups):
   
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
            f'{current_type} deals double damage to {super_effective_to_type}\n' +
            f'{current_type} deals half damage to {half_effective_to_type}\n' + 
            f'{current_type} deals no damage to {not_effective_to_type}\n')
            
# main game
def trainer(matchups):
   
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
            # update the player's score and combo
            App.update_score(10)
            App.update_combo_index()
            
            match App.get_combo_index():
               case 3:
                  App.increase_combo()
               case 5:
                  App.increase_combo()
               case 7:
                  App.increase_combo()
               case 10:
                  App.increase_combo()
               case 15:
                  App.increase_combo()
               case _:
                  pass
            
            print('\nthat\'s correct! Next up:\n')
      
         else:
            App.update_score(-10)
            App.reset_combo()
            
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
            # update the player's score and combo
            App.update_score(10)
            App.update_combo_index()
            
            match App.get_combo_index():
               case 3:
                  App.increase_combo()
               case 5:
                  App.increase_combo()
               case 7:
                  App.increase_combo()
               case 10:
                  App.increase_combo()
               case 15:
                  App.increase_combo()
               case _:
                  pass
            
            print('\nthat\'s correct! Next up:\n')
         else:
            App.update_score(-10)
            App.reset_combo()
            
            print(f'\nsorry, that\'s incorrect. {current_type} is actually weak against {current_answers}\n')

   App.set_highscore()
   print(f'good job! \nYour score was: {App.get_score()}\n' + 
                   f'Your Highscore is: {App.get_highscore()}\n')
   App.reset_score()
   App.reset_combo()

