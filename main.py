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
    settings_manager = SettingsManager()

    # Level selection
    selected_level = tk.simpledialog.askstring("Select Leve", "Choose a level (Easy/E, Medium/M, Hard/H)", initialvalue='M')
    settings_manager.set_active_level(selected_level.title() or "Medium")

    # Initialize root window
    root = tk.Tk()
    root.title("Minesweeper")

    # Initialize managers
    event_manager = EventManager(root)
    persistence_manager = PersistenceManager()

    # Retrieve game settings
    grid_size = settings_manager.get_setting('grid_size')
    num_mines = settings_manager.get_setting('num_mines')
    window_size = settings_manager.get_setting('window_size')

    # Initialize game components
    grid_manager = GridManager(grid_size, num_mines)
    game_manager = GameManager(grid_manager, event_manager)
    timer = Timer(event_manager)
    high_score_manager = HighScoreManager(persistence_manager)
    input_handler = InputHandler(grid_manager, game_manager, event_manager)

    # Initialize and start UI manager
    ui_manager = UIManager(root, grid_manager, game_manager, timer, high_score_manager, input_handler, event_manager, settings_manager)

    # Start the game
    game_manager.initialize_game()
    timer.start()

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
