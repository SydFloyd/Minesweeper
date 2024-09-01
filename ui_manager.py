import tkinter as tk
from tkinter import messagebox

class UIManager:
    def __init__(self, root, grid_manager, game_manager, timer, high_score_manager, input_handler, event_manager, window_size):
        self.root = root
        self.grid_manager = grid_manager
        self.game_manager = game_manager
        self.timer = timer
        self.high_score_manager = high_score_manager
        self.input_handler = input_handler
        self.event_manager = event_manager
        self.buttons = []

        self.root.geometry(window_size)  # Set an initial fixed size; adjust according to your grid size
        # self.root.resizable(False, False)  # Disable window resizing from the start

        self.create_widgets()

        # Subscribe to events
        self.event_manager.subscribe('grid_updated', self.update_grid)
        self.event_manager.subscribe('game_won', self.handle_win)
        self.event_manager.subscribe('game_lost', self.handle_loss)
        self.event_manager.subscribe('timer_started', self.update_timer)
        self.event_manager.subscribe('timer_reset', self.reset_timer)
        self.event_manager.subscribe('timer_updated', self.update_timer)

    def create_widgets(self):
        """Create and layout the game grid and UI components."""
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Create a frame for the timer and restart button
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack()

        # Place the restart button to the left
        self.restart_button = tk.Button(self.top_frame, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=0, column=0, padx=5)

        # Place the timer to the right of the restart button
        self.timer_label = tk.Label(self.top_frame, text="Time: 0", font=('Helvetica', 16))
        self.timer_label.grid(row=0, column=1, padx=5)

        self.create_grid_buttons()


    def create_grid_buttons(self):
        """Create buttons for the game grid based on the grid size."""
        for r in range(self.grid_manager.rows):
            row_buttons = []
            for c in range(self.grid_manager.cols):
                button = tk.Button(self.frame, width=3, height=1, font=('Helvetica', 16))
                button.grid(row=r, column=c)
                button.bind('<Button-1>', lambda event, row=r, col=c: self.handle_left_click(row, col))
                button.bind('<Button-3>', lambda event, row=r, col=c: self.handle_right_click(row, col))
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def update_grid(self, updated_grid):
        """Update the UI based on the current state of the grid."""
        for r in range(self.grid_manager.rows):
            for c in range(self.grid_manager.cols):
                cell = updated_grid[r][c]
                button = self.buttons[r][c]
                
                if cell['revealed']:
                    if cell['value'] == 'M':
                        button.config(text="M", state=tk.DISABLED, relief=tk.SUNKEN, bg='red')
                    elif cell['value'] > 0:
                        button.config(text=str(cell['value']), state=tk.DISABLED, relief=tk.SUNKEN)
                    else:
                        button.config(text="", state=tk.DISABLED, relief=tk.SUNKEN)
                elif cell['flagged']:
                    button.config(text="F", bg='yellow')
                else:
                    button.config(text="", state=tk.NORMAL, relief=tk.RAISED, bg='SystemButtonFace')

    def update_timer(self):
        """Update the timer display."""
        elapsed_time = self.timer.get_elapsed_time()
        self.timer_label.config(text=f"Time: {int(elapsed_time)}")

    def reset_timer(self):
        """Reset the timer display."""
        self.timer_label.config(text="Time: 0")

    def restart_game(self):
        """Handle the restart game button click."""
        self.timer.reset()
        self.game_manager.reset_game()
        self.update_grid(self.grid_manager.get_grid())

    def handle_left_click(self, row, col):
        """Handle the left-click event."""
        self.event_manager.dispatch('left_click', row, col)

    def handle_right_click(self, row, col):
        """Handle the right-click event."""
        self.event_manager.dispatch('right_click', row, col)

    def handle_win(self, grid):
        """Handle game won event."""
        self.timer.stop()
        self.animate_win(grid)
        elapsed_time = self.timer.get_elapsed_time()
        player_name = "Player"  # This could be customized
        self.high_score_manager.add_high_score(player_name, score=1, time=elapsed_time)  # Assuming score is always 1 for a win
        self.show_win_message()

    def animate_win(self, grid):
        """Animate a win by flashing the grid."""
        for _ in range(3):  # Flash 3 times
            for r in range(self.grid_manager.rows):
                for c in range(self.grid_manager.cols):
                    button = self.buttons[r][c]
                    button.config(bg='green')
            self.root.update()
            self.root.after(200)
            for r in range(self.grid_manager.rows):
                for c in range(self.grid_manager.cols):
                    button = self.buttons[r][c]
                    button.config(bg='SystemButtonFace')
            self.root.update()
            self.root.after(200)

    def show_win_message(self):
        """Show the win message after the animation."""
        messagebox.showinfo("You Win!", "Congratulations! You've won the game!")

    def handle_loss(self, grid):
        """Handle game lost event."""
        self.timer.stop()
        self.animate_loss(grid)
        self.show_loss_message()
        self.root.after(10)
        self.restart_game()

    def animate_loss(self, grid):
        """Animate a loss by flashing and gradually fading out the grid."""

        try:
            # Flash the grid red a few times
            for _ in range(3):
                for (r, c) in self.grid_manager.mines:
                    button = self.buttons[r][c]
                    button.config(bg='red')
                self.root.update()
                self.root.after(100)

                for (r, c) in self.grid_manager.mines:
                    button = self.buttons[r][c]
                    button.config(bg='black')
                self.root.update()
                self.root.after(100)

            ## Super cool but not good to mix place grid and pack :/
            # # Vibrate the grid (shift buttons slightly)
            # for _ in range(10):
            #     offset = 1 if _ % 2 == 0 else -1
            #     self.frame.place(x=offset, y=offset)
            #     self.root.update()
            #     self.root.after(50)
            # self.frame.place(x=0, y=0)  # Reset position

            # Gradually fade the grid to a dark color
            for intensity in range(255, 50, -5):
                color = f'#{intensity:02x}{intensity:02x}{intensity:02x}'
                for r in range(self.grid_manager.rows):
                    for c in range(self.grid_manager.cols):
                        button = self.buttons[r][c]
                        button.config(bg=color)
                self.root.update()
                self.root.after(50)

            # Disable all buttons
            for r in range(self.grid_manager.rows):
                for c in range(self.grid_manager.cols):
                    button = self.buttons[r][c]
                    button.config(state=tk.DISABLED)
            self.root.update()

        finally:
            # Restore window resizing capability after the animation
            self.root.resizable(True, True)  # Re-enable window resizing

    def show_loss_message(self):
        """Show the loss message after the animation."""
        messagebox.showinfo("Game Over", "Sorry, you lost the game.")
