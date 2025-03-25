# 
import sys
from gui.windows import Menu, Trainer, GameOver
from gui import app, QStackedWidget

        

def main():
    
    # instance windows
    window_manager = QStackedWidget()   # keep track of window hierarchy in manager
    menu_window = Menu()                # index 0
    trainer_window = Trainer()          # index 1
    game_over_window = GameOver()       # index 2
    
    # add windows to manager
    window_manager.addWidget(menu_window)
    window_manager.addWidget(trainer_window)
    window_manager.addWidget(game_over_window)
    
    # emit when the user presses the play button
    menu_window.play_button.clicked.connect(lambda: window_manager.setCurrentIndex(1))
    menu_window.play_button.clicked.connect(trainer_window.get_next_type_choice)
    menu_window.play_button.clicked.connect(trainer_window.set_question)
    menu_window.play_button.clicked.connect(trainer_window.start_countdown)
    
    # emit when the user finishes their quiz
    trainer_window.quit_signal.connect(lambda: window_manager.setCurrentIndex(2))
    trainer_window.quit_signal.connect(game_over_window.finalize_run)
    
    # emit when the menu is pressed on the game over screen
    game_over_window.menu_button.clicked.connect(lambda: window_manager.setCurrentIndex(0))
    
    # emit when play again is pressed on the game over screen
    game_over_window.play_again_button.clicked.connect(lambda: window_manager.setCurrentIndex(1))
    game_over_window.play_again_button.clicked.connect(trainer_window.get_next_type_choice)
    game_over_window.play_again_button.clicked.connect(trainer_window.set_question)
    game_over_window.play_again_button.clicked.connect(trainer_window.start_countdown)

    # show window and run app
    window_manager.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
    