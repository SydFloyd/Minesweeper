import random

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self):
        self.is_revealed = True

    def flag(self):
        self.is_flagged = not self.is_flagged

class Board:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]
        self._place_mines()
        self._calculate_adjacent_numbers()

    def _place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.cells[y][x].is_mine:
                self.cells[y][x].is_mine = True
                mines_placed += 1

    def _calculate_adjacent_numbers(self):
        for y in range(self.height):
            for x in range(self.width):
                if not self.cells[y][x].is_mine:
                    self.cells[y][x].adjacent_mines = self._count_adjacent_mines(x, y)

    def _count_adjacent_mines(self, x, y):
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.cells[ny][nx].is_mine:
                        count += 1
        return count

    def reveal_cell(self, x, y):
        if self.cells[y][x].is_flagged:
            return False  # Do nothing if the cell is flagged

        if self.cells[y][x].is_mine:
            return True  # Game over if the cell is a mine

        self._reveal_recursive(x, y)
        return False

    def _reveal_recursive(self, x, y):
        if self.cells[y][x].is_revealed or self.cells[y][x].is_flagged:
            return

        self.cells[y][x].reveal()

        if self.cells[y][x].adjacent_mines == 0:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self._reveal_recursive(nx, ny)

    def flag_cell(self, x, y):
        self.cells[y][x].flag()

    def check_win_condition(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_revealed and not cell.is_mine:
                    return False
        return True

    def render(self):
        print("   " + " ".join([str(i) for i in range(self.width)]))
        print("  +" + "-+" * self.width)
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = self.cells[y][x]
                if cell.is_flagged:
                    row.append("F")
                elif not cell.is_revealed:
                    row.append("?")
                elif cell.is_mine:
                    row.append("*")
                else:
                    row.append(str(cell.adjacent_mines) if cell.adjacent_mines > 0 else " ")
            print(f"{y} |" + "|".join(row) + "|")
        print("  +" + "-+" * self.width)

class Game:
    def __init__(self, width=10, height=10, num_mines=10):
        self.board = Board(width, height, num_mines)
        self.is_game_over = False

    def start_game(self):
        while not self.is_game_over:
            self.board.render()
            action, x, y = self.get_user_input()

            if action == "r":
                if self.board.reveal_cell(x, y):
                    self.is_game_over = True
                    print("Game Over! You hit a mine.")
            elif action == "f":
                self.board.flag_cell(x, y)

            if self.board.check_win_condition():
                self.board.render()
                print("Congratulations! You've won!")
                break

    def get_user_input(self):
        while True:
            try:
                action = input("Enter 'r' to reveal or 'f' to flag/unflag, followed by coordinates (e.g., 'r 3 4'): ").strip().lower()
                action_type, x, y = action.split()
                x, y = int(x), int(y)
                if action_type in ["r", "f"] and 0 <= x < self.board.width and 0 <= y < self.board.height:
                    return action_type, x, y
                else:
                    print("Invalid input. Try again.")
            except ValueError:
                print("Invalid input. Try again.")

if __name__ == "__main__":
    game = Game(width=10, height=10, num_mines=10)
    game.start_game()
