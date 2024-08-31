import random

class GridManager:
    def __init__(self, grid_size, num_mines):
        self.rows, self.cols = grid_size
        self.num_mines = num_mines
        self.grid = []
        self.mines = set()
        self.revealed = set()  # Track revealed cells
        self.flagged = set()   # Track flagged cells

    def create_grid(self):
        """Creates an empty grid, places mines, and calculates adjacent mines."""
        self.grid = [[{'value': 0, 'revealed': False, 'flagged': False} for _ in range(self.cols)] for _ in range(self.rows)]
        self.mines = self._place_mines()
        self._calculate_adjacent_mines()

    def _place_mines(self):
        """Places mines randomly on the grid."""
        mines = set()
        while len(mines) < self.num_mines:
            row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (row, col) not in mines:
                mines.add((row, col))
                self.grid[row][col]['value'] = 'M'
        return mines

    def _calculate_adjacent_mines(self):
        """Calculates the number of adjacent mines for each cell."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col]['value'] != 'M':
                    mine_count = sum(1 for dr, dc in directions if (row + dr, col + dc) in self.mines)
                    self.grid[row][col]['value'] = mine_count

    def reveal_cell(self, row, col):
        """Reveals the cell and connected cells if there are no adjacent mines."""
        if self.grid[row][col]['revealed']:
            return
        if self.grid[row][col]['revealed'] or self.grid[row][col]['flagged']:
            return
        self._reveal_recursive(row, col)

    def _reveal_recursive(self, row, col):
        """Recursively reveals cells with zero adjacent mines."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        if self.grid[row][col]['revealed'] or self.grid[row][col]['flagged']:
            return
        self.grid[row][col]['revealed'] = True
        self.revealed.add((row, col))

        if self.grid[row][col]['value'] == 0:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                self._reveal_recursive(row + dr, col + dc)

    def flag_cell(self, row, col):
        """Flags or unflags a cell."""
        if self.grid[row][col]['revealed']:
            return 0

        if self.grid[row][col]['flagged']:
            self.grid[row][col]['flagged'] = False
            self.flagged.remove((row, col))
            return -1
        else:
            self.grid[row][col]['flagged'] = True
            self.flagged.add((row, col))
            return 1

    def _auto_flag(self):
        """Automatically flags cells if all unrevealed neighbors match the cell's value."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col]['revealed'] and self.grid[row][col]['value'] > 0:
                    unrevealed_neighbors = self._get_unrevealed_neighbors(row, col)
                    if len(unrevealed_neighbors) + len(self._get_flagged_neighbors(row, col)) == self.grid[row][col]['value']:
                        for r, c in unrevealed_neighbors:
                            self.flag_cell(r, c)

    def _get_unrevealed_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = [(row + dr, col + dc) for dr, dc in directions]
        return [(r, c) for r, c in neighbors if 0 <= r < self.rows and 0 <= c < self.cols and not self.grid[r][c]['revealed']]

    def _get_flagged_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = [(row + dr, col + dc) for dr, dc in directions]
        return [(r, c) for r, c in neighbors if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c]['flagged']]

    def is_mine(self, row, col):
        """Checks if the cell at the given position is a mine."""
        return (row, col) in self.mines

    def get_grid_size(self):
        """Returns the grid size."""
        return self.rows, self.cols

    def get_num_mines(self):
        """Returns the number of mines."""
        return self.num_mines

    def get_total_cells(self):
        """Returns the total number of cells."""
        return self.rows * self.cols

    def get_grid(self):
        """Returns the current state of the grid."""
        return self.grid
