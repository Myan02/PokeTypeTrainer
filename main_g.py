# 11:33:45
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QPixmap
from modules import Pokemon
from modules import Pokemon
from random import choice as pick_one, shuffle as shuffle_list

class Window(QMainWindow):
    
    # get pokemon matchups when app is ran once
    matchups = Pokemon.get_type_info_r()

    def load_stylesheet(self, stylesheet: str) -> None:
        with open(stylesheet, 'r') as file:
            self.setStyleSheet(file.read())
    
    '''
        get current question, correct answer, and wrong answers 
        cls.current_type = the type to pick an answer against
        cls.current_answers = all answers for that one type
        cls.choices_available = a list of available choices for the player to choose from
    '''
    def get_next_type_choice(cls) -> None:
        
        # current question type and answer (only one answer per question)
        cls.current_type = pick_one(list(cls.matchups.keys()))
        cls.current_answers = [relation['name'] for relation in cls.matchups[cls.current_type]['double_damage_from']]  
        
        # populate a list with all choices
        cls.choices_available = []
        for choice_index in range(4):
        
            # place the answer at index 0
            if choice_index == 0:
                cls.choices_available.append(pick_one(cls.current_answers))
                
            # place wrong answers at index 1-3
            else:
                cls.choices_available.append(pick_one([rand_type for rand_type in list(cls.matchups.keys()) if rand_type not in cls.current_answers and rand_type not in cls.choices_available]))
        
        # shuffle the list so the right answer isn't always at index 0
        shuffle_list(cls.choices_available)

class Menu(Window):
    def __init__(self):
        
        # initialize menu
        super().__init__()
        self.setWindowTitle('PokeTrainer')
        self.layoutWidget = QWidget()
        self.font_id = QFontDatabase.addApplicationFont('./fonts/Pokemon_Solid.ttf')
                
        # menu elements
        self.title_label = QLabel(text='PokeTrainer')
        self.play_button = QPushButton(text='Play')
        self.help_button = QPushButton(text='Help')
        self.options_button = QPushButton(text='Options')
        self.quit_button = QPushButton(text='Quit')
        self.copyright_label = QLabel(text='Made with love - MB')
        self.menu_elements = (self.title_label, self.play_button, self.help_button, self.options_button, self.quit_button, self.copyright_label)
        
        self.menu_container = self.init_menu_ui()
        self.layoutWidget.setLayout(self.menu_container)
        self.setCentralWidget(self.layoutWidget)
    
    def init_menu_ui(self) -> QVBoxLayout:
        
        # create the vertical layout
        vbox = QVBoxLayout()
        
        # all widgets lie under the vbox layout
        for widget in self.menu_elements:
            vbox.addWidget(widget)
            
        # align widgets
        self.title_label.setAlignment(Qt.AlignCenter)
        self.copyright_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        
        # each objects unique name maps to a css ID
        self.title_label.setObjectName('title_label')
        self.play_button.setObjectName('play_button')
        self.help_button.setObjectName('help_button')
        self.options_button.setObjectName('options_button')
        self.quit_button.setObjectName('quit_button')
        self.copyright_label.setObjectName('copyright_label')
        
        self.load_stylesheet('./stylesheets/menu.qss')
        
        return vbox


class Trainer(Window):
    
    def __init__(self):
        
        # initialize trainer
        super().__init__()
        self.setWindowTitle('PokeTrainer')
        self.layoutWidget = QWidget()
        
        # trainer elements
        self.score_label = QLabel(text='Score: ')
        self.first_type = QLabel()
        self.comparison_label = QLabel(text='>')
        self.second_type = QLabel()
        self.choices = [QPushButton() for _ in range(4)]
        self.trainer_elements = (self.score_label, self.first_type, self.comparison_label, self.second_type, self.choices)
        
        self.trainer_container = self.init_trainer_ui()
        self.layoutWidget.setLayout(self.trainer_container)
        self.setCentralWidget(self.layoutWidget)
        
        self.get_next_type_choice()
        self.set_question()
    
    
    def init_trainer_ui(self) -> QVBoxLayout:
        
        # create the vertical layout
        vbox = QVBoxLayout()
        
        # create child horizontal layout for question types
        hbox = QHBoxLayout()
        
        # create grid layout for multiple choice locations
        gridbox = QGridLayout()
        
        # add horizontal widgets
        hbox.addWidget(self.first_type)
        hbox.addWidget(self.comparison_label)
        hbox.addWidget(self.second_type)

        # add grid choices
        gridbox.addWidget(self.choices[0], 0, 0)
        gridbox.addWidget(self.choices[1], 0, 1)
        gridbox.addWidget(self.choices[2], 1, 0)
        gridbox.addWidget(self.choices[3], 1, 1)
        
        # add all widgets to main vertical layout
        vbox.addWidget(self.score_label)
        vbox.addLayout(hbox)
        vbox.addLayout(gridbox)
            
        # align widgets
        self.score_label.setAlignment(Qt.AlignRight)
        hbox.setAlignment(Qt.AlignCenter)
        
        # object names
        self.score_label.setObjectName('score_label')
        self.first_type.setObjectName('first_type')
        self.comparison_label.setObjectName('comparison_label')
        self.second_type.setObjectName('second_type')
        self.choices[0].setObjectName('choice_1')
        self.choices[1].setObjectName('choice_2')
        self.choices[2].setObjectName('choice_3')
        self.choices[3].setObjectName('choice_4')
        
        # load stylesheet
        self.load_stylesheet('./stylesheets/trainer.qss')
        
        return vbox


    def set_question(self) -> None:
        
        self.first_type.setText('?')
        self.second_type.setText(self.current_type)
        
        print(self.current_answers)
                
        for index, choice in enumerate(self.choices):
            print(index)
            choice.setText(self.choices_available[index])
            if choice.text() in self.current_answers:
                choice.clicked.connect(self.correct_answer_picked)
            else:
                choice.clicked.connect(self.wrong_answer_picked)
        
    def correct_answer_picked(self) -> None:
        print('yay')
        self.reset_question()
        self.get_next_type_choice()
        self.set_question()
    
    def wrong_answer_picked(self) -> None:
        print('nay')
        self.reset_question()
        self.get_next_type_choice()
        self.set_question()
    
    def reset_question(self) -> None:
        self.current_answers.clear()
        self.choices_available.clear()
        
        for choice in self.choices:
            choice.disconnect()
        
                
        
    
    
    
    

        
        
    



        

def main():
    app = QApplication([])
    
    menu_window = Menu()
    trainer_window = Trainer()
    
    window_manager = QStackedWidget()
    window_manager.addWidget(menu_window)
    window_manager.addWidget(trainer_window)
    menu_window.play_button.clicked.connect(lambda: window_manager.setCurrentIndex(1))
    
    window_manager.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
    
    
    
'''
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
'''
    