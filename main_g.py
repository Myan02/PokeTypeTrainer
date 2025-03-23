# 11:33:45
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase, QPixmap
from modules import Pokemon
import run

class Window(QMainWindow):

    def load_stylesheet(self, stylesheet: str) -> None:
        with open(stylesheet, 'r') as file:
            self.setStyleSheet(file.read())
        

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
        self.first_type.setPixmap(QPixmap('./icons/bug.svg').scaled(100, 100))
        self.comparison_label = QLabel(text='>')
        self.second_type = QLabel()
        self.choice_1 = QPushButton()
        self.choice_2 = QPushButton()
        self.choice_3 = QPushButton()
        self.choice_4 = QPushButton()
        self.trainer_elements = (self.score_label, self.first_type, self.comparison_label, self.second_type, self.choice_1, self.choice_2, self.choice_3, self.choice_4)
        
        self.trainer_container = self.init_trainer_ui()
        self.layoutWidget.setLayout(self.trainer_container)
        self.setCentralWidget(self.layoutWidget)
    
    
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
        gridbox.addWidget(self.choice_1, 0, 0)
        gridbox.addWidget(self.choice_2, 0, 1)
        gridbox.addWidget(self.choice_3, 1, 0)
        gridbox.addWidget(self.choice_4, 1, 1)
        
        # add all widgets to main vertical layout
        vbox.addWidget(self.score_label)
        vbox.addLayout(hbox)
        vbox.addLayout(gridbox)
            
        # align widgets
        self.score_label.setAlignment(Qt.AlignRight)
        hbox.setAlignment(Qt.AlignCenter)
        
        self.first_type.setObjectName('first_type')
        
        self.load_stylesheet('./stylesheets/trainer.qss')
        
        return vbox

        
    



        

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
    