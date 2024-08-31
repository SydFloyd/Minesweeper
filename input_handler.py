class InputHandler:
    def __init__(self, grid_manager, game_manager, event_manager):
        self.grid_manager = grid_manager
        self.game_manager = game_manager
        self.event_manager = event_manager

        # Subscribe to relevant events
        self.event_manager.subscribe('left_click', self.handle_left_click)
        self.event_manager.subscribe('right_click', self.handle_right_click)

    def handle_left_click(self, row, col):
        """Handles the left-click event for revealing a tile."""
        if self.game_manager.is_game_over():
            return

        self.game_manager.reveal_cell(row, col)
        self.event_manager.dispatch('grid_updated', self.grid_manager.get_grid())

    def handle_right_click(self, row, col):
        """Handles the right-click event for flagging a tile."""
        if self.game_manager.is_game_over():
            return

        self.game_manager.flag_cell(row, col)
        self.event_manager.dispatch('grid_updated', self.grid_manager.get_grid())
