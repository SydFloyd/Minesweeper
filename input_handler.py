class InputHandler:
    def __init__(self, grid_manager, game_manager, event_manager):
        self.grid_manager = grid_manager
        self.game_manager = game_manager
        self.event_manager = event_manager
        self.timer_started = False  # Track if the timer has started

        # Subscribe to relevant events
        self.event_manager.subscribe('left_click', self.handle_left_click)
        self.event_manager.subscribe('right_click', self.handle_right_click)

    def start_timer_if_needed(self):
        """Start the timer if it hasn't been started yet."""
        if not self.timer_started:
            self.event_manager.dispatch('start_timer')
            self.timer_started = True

    def handle_left_click(self, row, col):
        """Handles the left-click event for revealing a tile."""
        if self.game_manager.is_game_over():
            return

        self.start_timer_if_needed()
        self.game_manager.reveal_cell(row, col)
        self.event_manager.dispatch('grid_updated', self.grid_manager.get_grid())

    def handle_right_click(self, row, col):
        """Handles the right-click event for flagging a tile."""
        if self.game_manager.is_game_over():
            return

        self.start_timer_if_needed()
        self.game_manager.flag_cell(row, col)
        self.event_manager.dispatch('grid_updated', self.grid_manager.get_grid())
