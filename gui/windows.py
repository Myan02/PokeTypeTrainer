# script holds all pyqt5 application windows
# written by Michael Baburyan March 25, 2025

import time
from math import floor
from random import choice as pick_one, shuffle as shuffle_list
from modules import Score, Pokemon

from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt, QCoreApplication, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFontDatabase, QPixmap


# abstract class, handles requests and some game logic related to requests
class Window(QMainWindow):
    
    # get pokemon matchups ONCE, keeps info for the rest of the time the application is up
    matchups = Pokemon.get_type_info_r()
    
    # make a highscore file to keep track of a device's highscore like a save state
    Score.initialize_highscore()

    # load the window's styles
    def load_stylesheet(self, stylesheet: str) -> None:
        try:
            with open(stylesheet, 'r') as file:
                self.setStyleSheet(file.read())
        except Exception as e:
            print(f'unable to load stylesheet \"{stylesheet}\", maybe it was deleted? error: {e}')
    
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

# menu window, first thing to open when the user starts up the app
class Menu(Window):
   
    def __init__(self) -> None:
      
        # initialize menu variables
        super().__init__()
        self.setWindowTitle('PokeTrainer')
        self.layoutWidget = QWidget()
        self.font_id = QFontDatabase.addApplicationFont('./gui/fonts/Minecraftia-Regular.ttf')  # load custom fonts
        self.pokemon_logo = QPixmap('./gui/icons/International_Pokémon_logo.svg.png')
        
        # menu elements
        self.title_label = QLabel()
        self.play_button = QPushButton(text='Play')
        self.help_button = QPushButton(text='Help')
        self.options_button = QPushButton(text='Options')
        self.quit_button = QPushButton(text='Quit')
        self.copyright_label = QLabel(text='Made with love - MB')
        self.menu_elements = (self.title_label, self.play_button, self.help_button, self.options_button, self.quit_button, self.copyright_label)
        
        # button signals and slots
        self.quit_button.clicked.connect(self.quit_application)
        
        # containers and layouts
        self.menu_container = self.init_menu_ui()
        self.layoutWidget.setLayout(self.menu_container)
        self.setCentralWidget(self.layoutWidget)
   
    # prepare the widgets
    def init_menu_ui(self) -> QVBoxLayout:
      
        # create the vertical layout
        vbox = QVBoxLayout()
        
        # sub layouts for the pushbutton options
        hbox_top = QHBoxLayout()
        hbox_bottom = QHBoxLayout()
        
        # all all widgets and layouts
        hbox_top.addWidget(self.play_button)
        hbox_top.addWidget(self.help_button)
        hbox_bottom.addWidget(self.options_button)
        hbox_bottom.addWidget(self.quit_button)
        
        vbox.addWidget(self.title_label)
        vbox.addLayout(hbox_top)
        vbox.addLayout(hbox_bottom)
        vbox.addWidget(self.copyright_label)
            
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
        
        # set size of the buttons
        self.play_button.setMinimumWidth(150)
        self.help_button.setMinimumWidth(150)
        self.options_button.setMinimumWidth(150)
        self.quit_button.setMinimumWidth(150)
        
        # set pokemon logo
        self.title_label.setGeometry(0, 0, 341, 125)
        self.scaled_pokemon_logo = self.pokemon_logo.scaled(self.title_label.size(), aspectRatioMode=1)
        self.title_label.setPixmap(self.scaled_pokemon_logo)
        self.title_label.setScaledContents(True)
        
 
        # get css styling for this batch of widgets
        self.load_stylesheet('./gui/stylesheets/menu.qss')
        
        return vbox
  
    # safely quit the application
    def quit_application(self):
        QCoreApplication.instance().quit()
        

# quiz window, extends QObject to get access to custom signals
class Trainer(Window, QObject):
   
    # create a signal to be emitting when the player has ran out of time
    quit_signal = pyqtSignal()
   
    # initialize quiz window
    def __init__(self):
        
        # initialize trainer variables
        super().__init__()
        self.setWindowTitle('PokeTrainer')
        self.layoutWidget = QWidget()
        self.font_id = QFontDatabase.addApplicationFont('./gui/fonts/Minecraftia-Regular.ttf')  # load custom fonts
        self.start_time = 0     # used for each question start time to calculate score
        self.end_time = 0       # used for each question start time to calculate score
        self.total_time = 60    # maximum time player has for all questions
        self.first_type_icon = QPixmap()
        self.second_type_icon = QPixmap()
        
        
        # trainer elements
        self.score_label = QLabel(text='Score: ')
        self.time_label = QLabel(text='0:0')
        self.first_type = QLabel()
        self.comparison_label = QLabel(text='is super effective against')
        self.second_type = QLabel()
        self.choices = [QPushButton() for _ in range(4)]
        self.trainer_elements = (self.score_label, self.first_type, self.comparison_label, self.second_type, self.choices)
        
        # containers and layouts
        self.trainer_container = self.init_trainer_ui()
        self.layoutWidget.setLayout(self.trainer_container)
        self.setCentralWidget(self.layoutWidget)
        
    # prepare widgets
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

        # add grid choices
        gridbox.addWidget(self.choices[0], 0, 0)
        gridbox.addWidget(self.choices[1], 0, 1)
        gridbox.addWidget(self.choices[2], 1, 0)
        gridbox.addWidget(self.choices[3], 1, 1)
        
        # add all widgets to main vertical layout
        vbox.addWidget(self.score_label)
        vbox.addWidget(self.time_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.second_type, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
        vbox.addLayout(gridbox)
        
        # set label sizing
        self.score_label.setFixedHeight(40)
        self.time_label.setFixedHeight(40)
        self.second_type.setMinimumSize(75, 75)
        self.second_type.setMaximumSize(75, 75)
            
        # align widgets
        self.score_label.setAlignment(Qt.AlignRight)
        self.time_label.setAlignment(Qt.AlignRight)
        hbox.setAlignment(Qt.AlignCenter)
        self.second_type.setAlignment(Qt.AlignCenter)
        
        
        # object names
        self.score_label.setObjectName('score_label')
        self.time_label.setObjectName('time_label')
        self.first_type.setObjectName('first_type')
        self.comparison_label.setObjectName('comparison_label')
        self.second_type.setObjectName('second_type')
        self.choices[0].setObjectName('choice_1')
        self.choices[1].setObjectName('choice_2')
        self.choices[2].setObjectName('choice_3')
        self.choices[3].setObjectName('choice_4')
        
        # load stylesheet
        self.load_stylesheet('./gui/stylesheets/trainer.qss')
        
        return vbox

    # simply changes the text of the score
    def update_score_label(self) -> None:
        text = f'Score: {int(Score.get_score())}'
        self.score_label.setText(text)

    # prepare the question and answer choices for EACH question
    def set_question(self) -> None:
        
        # calculate how long it takes for the user to choose an answer
        self.start_time = time.time()
        
        # set text and icons for question labels
        self.update_score_label()
        self.first_type.setText('?')
        self.second_type.setGeometry(0, 0, 50, 50)
        icon = QPixmap(f'./gui/icons/{self.current_type}.svg')
        scaled_icon = icon.scaled(self.second_type.size(), aspectRatioMode=1)
        self.second_type.setPixmap(scaled_icon)
        self.second_type.setScaledContents(True)
        
        # debugging purposes (i suck at remembering types lmao)
        print(f'{self.current_answers}\n')
                
        # write our the answer choices and make a connection for the right and wrong answers
        for index, choice in enumerate(self.choices):
            choice.setText(self.choices_available[index])
            
            if choice.text() in self.current_answers:
                choice.clicked.connect(self.correct_answer_picked)
            else:
                choice.clicked.connect(self.wrong_answer_picked)
    

    # invoke when the user gets a correct answer
    def correct_answer_picked(self) -> None:
        
        # the user gets points based on how quickly they answer, every second you take is a second off
        self.end_time = time.time()
        
        # score is held in the module modules.py under the Score class
        Score.update_score(max((10 - (floor(self.end_time - self.start_time))), 0))
        Score.increase_combo()
        
        # prepare next question
        self.reset_question()
        self.get_next_type_choice()
        self.set_question()
    
    # invoke when the user gets a wrong answer
    def wrong_answer_picked(self) -> None:
        
        # I get the end time just to complete the time loop, its not needed for a wrong answer
        self.end_time = time.time()
        
        # if you get a question wrong, your combo is killed AND you lose 10 points... so take your time i guess
        Score.reset_combo()
        Score.update_score(-10)
        
        # prepare next question
        self.reset_question()
        self.get_next_type_choice()
        self.set_question()
    
    # clears variables 
    def reset_question(self) -> None:
        
        # clear and reset all variables
        self.current_answers.clear()
        self.choices_available.clear()
        
        # we need to disconnect the connections because they don't overwrite, they stack
        for choice in self.choices:
            choice.disconnect()
    
    # quiz total time, user can choose how long they want to be quizzed
    def start_countdown(self):
        
        # instantiate a new timer for every new quiz game
        self.timer = QTimer()
        self.timer.timeout.connect(self.countdown_timeout)
        
        # goes off every 1 sec (1000 is in ms)
        self.timer.start(1000)
        
        # set time label so it doesn't show weird values when the user starts the quiz
        self.time_label.setText(f'0:{self.total_time:02d}')

    
    # runs every second when the quiz is started
    def countdown_timeout(self):
        
        # during quiz time
        if self.total_time > 0:
            self.total_time -= 1
            mins, secs = divmod(self.total_time, 60)    # sets the minutes and seconds
            self.time_label.setText(f'{mins:02d}:{secs:02d}')
        
        # once the timer runs out
        else:
            self.timer.stop()
            self.timer.deleteLater()    # deletes the instantiated timer when available
            self.total_time = 60        # resets the time
            self.quit_signal.emit()     # emit to change the window 
            
                
# end quiz window
class GameOver(Window):
    
    # initialize ending window
    def __init__(self):
        
        # prepare variables
        super().__init__()
        self.setWindowTitle('PokeTrainer')
        self.layoutWidget = QWidget()

        # initialize widgets
        self.finished_label = QLabel('All Done!')
        self.score_label = QLabel('You Got: 0 pts')
        self.highscore_label = QLabel('Highscore: 0 pts')
        self.play_again_button = QPushButton('Try Again')
        self.menu_button = QPushButton('Menu')
        self.game_over_elements = [self.finished_label, self.score_label, self.highscore_label, self.play_again_button, self.menu_button]
    
        # layouts and containers
        self.game_over_container = self.init_game_over_ui()
        self.layoutWidget.setLayout(self.game_over_container)
        self.setCentralWidget(self.layoutWidget)
    
    # prepare widgets
    def init_game_over_ui(self) -> None:
        
        # two layout containers, main layout is the vbox
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        
        # add horizontal child layout widgets
        hbox.addWidget(self.play_again_button)
        hbox.addWidget(self.menu_button)
        
        # add main widgets to the vbox
        vbox.addWidget(self.finished_label)
        vbox.addWidget(self.score_label)
        vbox.addWidget(self.highscore_label)
        vbox.addLayout(hbox)
        
        # set widget alignments
        self.finished_label.setAlignment(Qt.AlignCenter)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.highscore_label.setAlignment(Qt.AlignCenter)
        
        # set widget names
        self.finished_label.setObjectName('finished_label')
        self.score_label.setObjectName('score_label')
        self.highscore_label.setObjectName('highscore_label')
        self.play_again_button.setObjectName('play_again_button')
        self.menu_button.setObjectName('menu_button')
        
        # set widget sizes
        self.play_again_button.setFixedWidth(150)
        self.menu_button.setFixedWidth(150)
         
        # load stylesheet
        self.load_stylesheet('./gui/stylesheets/game_over.qss') 
         
        return vbox

    # sets up and resets variables after the quiz ended
    def finalize_run(self):
        
        # if you beat your highscore, this sets your highscore to what you just got in the Scores class (temporary)
        Score.set_highscore()
        
        # set the labels for the scores and display them
        self.score_label.setText(f'You Got: {int(Score.get_score())} pts')
        self.highscore_label.setText(f'Highscore: {int(Score.get_highscore())} pts')
        
        # update the highscore.txt file as a user save state
        Score.update_highscore_file()
        
        # all other variables are cleared to default
        Score.reset_combo()
        Score.reset_score()
            