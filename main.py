import tkinter as tk
from event_manager import EventManager
from grid_manager import GridManager
from game_manager import GameManager
from timer import Timer
from high_score_manager import HighScoreManager
from input_handler import InputHandler
from persistence_manager import PersistenceManager
from settings_manager import SettingsManager
from ui_manager import UIManager

def main():
    # Initialize root window
    root = tk.Tk()
    root.title("Minesweeper")

    # Initialize managers
    event_manager = EventManager()
    persistence_manager = PersistenceManager()
    settings_manager = SettingsManager(persistence_manager)

    # Retrieve game settings
    grid_size = settings_manager.get_setting('grid_size')
    num_mines = settings_manager.get_setting('num_mines')

    # Initialize game components
    grid_manager = GridManager(grid_size, num_mines)
    game_manager = GameManager(grid_manager, event_manager)
    timer = Timer(event_manager)
    high_score_manager = HighScoreManager(persistence_manager)
    input_handler = InputHandler(grid_manager, game_manager, event_manager)

    # Initialize and start UI manager
    ui_manager = UIManager(root, grid_manager, game_manager, timer, high_score_manager, input_handler, event_manager)

    # Start the game
    game_manager.initialize_game()

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
