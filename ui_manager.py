import tkinter as tk
from tkinter import messagebox, Menu, simpledialog, TclError
import random

class UIManager:
    def __init__(self, root, grid_manager, game_manager, timer, high_score_manager, input_handler, event_manager, settings_manager):
        self.root = root
        self.grid_manager = grid_manager
        self.game_manager = game_manager
        self.timer = timer
        self.high_score_manager = high_score_manager
        self.input_handler = input_handler
        self.event_manager = event_manager
        self.settings_manager = settings_manager
        self.buttons = []

        self.root.geometry(self.settings_manager.get_setting("window_size"))  # Set an initial fixed size; adjust according to your grid size
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
        self.create_menu()  # Create the menu bar

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

    def create_menu(self):
        """Create a menu bar with a high scores option."""
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Add a menu item for high scores
        game_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=game_menu)
        game_menu.add_command(label="High Scores", command=self.show_high_scores)

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

    def show_high_scores(self):
        """Display a dialog showing the high scores."""
        high_scores = self.high_score_manager.get_high_scores(self.settings_manager.get_active_level())
        scores_text = "\n".join([f"{score['name']}: {score['time']}s" for score in high_scores])
        if not scores_text:
            scores_text = "No high scores yet."
        messagebox.showinfo("High Scores", scores_text)

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
        active_level = self.settings_manager.get_active_level()
        if elapsed_time < self.high_score_manager.get_high_score_time(active_level):
            message = "New High Score!!"
        else:
            message = "Congratulations!"
        player_name = simpledialog.askstring("You Win!", f"{message}\nEnter your name:")
        if player_name:  # If the user provided a name
            self.high_score_manager.add_high_score(active_level, player_name, time=elapsed_time)
        else:  # Default name if no input is given
            self.high_score_manager.add_high_score(active_level,"A", time=elapsed_time)

    def animate_win(self, grid):
        """Animate a win."""
        colors = [
            "#4CAF50",  # Vibrant green, representing success and accomplishment
            "#FFD700",  # Bright gold, symbolizing victory and reward
            "#00BCD4",  # Calm cyan, associated with clarity and cool triumph
            "#8BC34A",  # Light green, reflecting a fresh and positive outcome
            "#FFEB3B",  # Bright yellow, symbolizing energy, excitement, and success
            "#FFC107",  # Warm amber, evoking a sense of achievement and positivity
            "#81C784",  # Soft green, representing tranquility and a well-earned win
            "#CDDC39",  # Lime green, conveying a fresh and victorious result
            "#2196F3",  # Strong blue, symbolizing clarity and decisive victory
            "#E1BEE7",  # Light lavender, representing a smooth and joyful triumph
        ]

        rows, cols = self.grid_manager.get_grid_size()
        try:
            for _ in range(18):
                for r in range(rows):
                    for c in range(cols):
                        button = self.buttons[r][c]
                        bg_color = random.choice(colors) if random.random() < 0.10 else 'SystemButtonFace'
                        button.config(bg=bg_color)
                self.root.update()
                self.root.after(15)
            #Reset
            for r in range(rows):
                for c in range(cols):
                    button = self.buttons[r][c]
                    button.config(bg='SystemButtonFace')
            self.root.update()
            self.root.after(200)
        except TclError:
            pass

    def handle_loss(self, grid):
        """Handle game lost event."""
        self.timer.stop()
        self.animate_loss(grid)
        self.show_loss_message()
        self.root.after(10)
        self.restart_game()

    def animate_loss(self, grid):
        """Animate a loss by flashing and gradually fading out the grid."""
        # Flash the grid red a few times
        try:
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
        except TclError:
            pass

    def show_loss_message(self):
        """Show the loss message after the animation."""
        messagebox.showinfo("Game Over", "Sorry, you lost the game.")
