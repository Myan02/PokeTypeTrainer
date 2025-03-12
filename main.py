from modules import Pokemon
import run

def main():
   
   matchups = Pokemon.get_type_info_r()
   app_running = True
   
   while(app_running):
      
      user_input = input('welcome to the poke type trainer. Please select 1 to run the trainer, 2 to get help, and anything else to quit... ')
      print()
      
      match user_input:
         case '1':
            run.trainer(matchups=matchups)
            
         case '2':
            run.type_directory(matchups=matchups)
            
         case _:
            break
      

if __name__ == '__main__':
   main()

