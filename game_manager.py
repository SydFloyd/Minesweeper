class GameManager:
    def __init__(self, grid_manager, event_manager):
        self.grid_manager = grid_manager
        self.event_manager = event_manager
        self.game_state = 'idle'  # Possible states: 'idle', 'playing', 'won', 'lost'
        self.mines_flagged = 0
        self.cells_revealed = 0
        self.first_click = True

    def initialize_game(self):
        """Initializes the game by creating the grid and placing mines."""
        self.grid_manager.create_grid()
        self.game_state = 'playing'
        self.mines_flagged = 0
        self.cells_revealed = 0
        self.first_click = True
        self.event_manager.dispatch('start_new_game', self.grid_manager.get_grid_size())

    def reveal_cell(self, row, col):
        """Reveals a cell and updates the game state accordingly."""
        if self.game_state != 'playing':
            return

        if self.first_click:
            self.grid_manager.fill_grid((row, col))
            self.first_click = False
            self.reveal_cell(row, col)
            return
        
        if self.grid_manager.is_flag(row, col):
            return
        elif self.grid_manager.is_mine(row, col):
            self.game_state = 'lost'
            self.event_manager.dispatch('game_lost', self.grid_manager.get_grid())
        else:
            previous_revealed = len(self.grid_manager.revealed)
            self.grid_manager.reveal_cell(row, col)
            newly_revealed = len(self.grid_manager.revealed) - previous_revealed

            self.cells_revealed += newly_revealed
            self.event_manager.dispatch('cell_revealed', row, col, newly_revealed)
            self.check_win_condition()

    def flag_cell(self, row, col):
        """Flags or unflags a cell as containing a mine."""
        if self.game_state != 'playing':
            return

        flag_change = self.grid_manager.flag_cell(row, col)
        self.mines_flagged += flag_change
        self.event_manager.dispatch('cell_flagged', row, col, flag_change)
        self.check_win_condition()

    def check_win_condition(self):
        """Checks if the player has won the game."""
        if self.cells_revealed == self.grid_manager.get_total_cells() - self.grid_manager.get_num_mines():
            self.game_state = 'won'
            self.event_manager.dispatch('game_won', self.grid_manager.get_grid())

    def is_game_over(self):
        """Returns True if the game is over (either won or lost), False otherwise."""
        return self.game_state in ['won', 'lost']

    def reset_game(self):
        """Resets the game to its initial state."""
        self.initialize_game()
        self.event_manager.dispatch('game_reset')
