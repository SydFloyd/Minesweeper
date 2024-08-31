# Minesweeper Official Rules

## General Definitions

- **Standard Levels**: There are three standard levels in Minesweeper:
  - **Beginner**: 8x8 grid with 10 mines.
  - **Intermediate**: 16x16 grid with 40 mines.
  - **Expert**: 30x16 grid with 99 mines.

- **Square States**: During the game, a square can be in one of the following states:
  - **Closed**: At the start of the game, all squares are 'closed'.
  - **Open**: A square showing either a number or a blank cell is 'open'. Each square can only be opened once. Further clicking on an already open square won't affect the board's status.
  - **Marked as Mine**: A square that has been marked as a mine won't be affected by further clicks that would normally open squares.

- **Mouse Actions**: The following actions are allowed to play and solve Minesweeper:
  - **Left Click**: Carried out when the left mouse button is released over a square inside the Minesweeper window. A left click on a closed square opens that square.
  - **Right Click**: Marks or unmarks a square as a mine.
  - **Double Click**: Opens all surrounding squares if the number of surrounding mines matches the number on the square.

## Allowed Mouse Button Functions

- **Button States**:
  - **Depressed**: The state of the button when it is pressed.
  - **Released**: The state of the button when it is released.
  - **Null**: The state of the button when it is not being interacted with.

- **LMB (Left Mouse Button)**:
  - May open a square only if the sequence of states is `Depress & Release` while the state of other buttons is `Null`.

## Interface

- **Clone Interface**:
  - A clone may process all information that is displayed to the player in an explicit way.
  - The interface is divided into:
    - **Field**: Consists of a grid of squares, each with a state (closed, open, marked as mine).
    - **Rest**: Other elements of the interface that are not part of the field.

## Minesweeper Reveal Algorithm

- The Minesweeper reveal algorithm works as follows:
  1. **Flagging Mines**:
     - If the sum of unrevealed neighbors and flagged neighbors equals the value of the cell, flag the unrevealed neighbors.
  2. **Revealing Squares**:
     - If the number of flagged neighbors equals the cell value, reveal the remaining unrevealed neighbors.
  3. **Recursive Reveal**:
     - If a cell has no adjacent mines, recursively reveal all eight adjacent tiles.
     - When revealing a square with zero adjacent mines, automatically reveal all adjacent squares.
  4. **Displaying Numbers**:
     - If a cell has one or more adjacent mines, display the number of mines next to it.
