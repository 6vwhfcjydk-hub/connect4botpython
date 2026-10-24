# Connect 4 (Terminal Edition)

A two-player Connect 4 game for the terminal, written in plain Python with no external dependencies. Play a match of as many games as you like with a running scoreboard, then replay any game from the match move by move.

## Features

- Two-player local play on a standard 6×7 board
- Win detection in all four directions: horizontal, vertical, and both diagonals
- Input validation for non-numeric input, out-of-range columns, and full columns
- A match scoreboard that carries over between games, with draws worth half a point
- Every game's moves are recorded, so you can replay any game from the match once it ends

## Requirements

- Python 3.6 or later (the code uses f-strings)

## Getting Started

Clone or download the project, then from the project folder run:

```bash
python Interface.py
```

## How to Play

1. **Player X** always moves first, followed by **Player O**.
2. On your turn, enter a column number from **1 to 7**. Your piece drops to the lowest empty row in that column.
3. The first player to line up **four pieces in a row** (horizontally, vertically, or diagonally) wins the game.
4. If the board fills up with no winner, the game is a **draw**.
5. After each game, you're asked `Do you want to play again? y/n`. Answer `y` to start a new game with the scoreboard carried over. Any other answer ends the match.

Empty cells are shown as `.`:

```
. . . . . . .
. . . . . . .
. . . . . . .
. . . O . . .
. . X O . . .
. X X O X . .
```

### Input handling

| Input | Result |
|-------|--------|
| A number outside 1–7 | `Invalid Column`, try again |
| Something that isn't a number | `Enter a number from 1-7`, try again |
| A column that's already full | `Column full, try again`, still your turn |

## Scoring

| Result | Points |
|--------|--------|
| Win    | 1 point to the winner |
| Draw   | 0.5 points to each player |

The updated scores are shown after every game. When the match ends, the final scores are displayed and the match winner is announced: whoever has more points, or a drawn match if the scores are level.

## Replaying Games

After the match ends, you can revisit any game you played:

1. Enter a game number. Games are numbered from **1** in the order they were played.
2. The game is replayed on a fresh board, showing the position after each move, followed by the winner if there was one.
3. The game's move list is printed. Each entry is the column played, starting with Player X and alternating, for example `[4, 4, 3, 5, 2, 1, 1]`.
4. Enter another game number to see another game, or type `exit` to quit.

## Project Structure

| File | Purpose |
|------|---------|
| `Interface.py` | Entry point. Creates the scoreboard, runs the match, then offers game replays. |
| `Gameloop.py` | Runs games back to back, records each game's moves, asks whether to play again, and announces the match result. |
| `Game.py` | Runs a single game: alternates turns, validates input, records moves, and handles wins and draws. |
| `Initialisation.py` | Builds a fresh empty board and the column-tracking dictionary. |
| `Action.py` | Places a piece in the chosen column. |
| `Outcome.py` | Win detection in all four directions, identifying the winner, and checking for a full board. |
| `Display.py` | Prints the board to the terminal. |
| `Score.py` | Creates, updates, and displays the scoreboard. |
| `Notation.py` | Creates the dictionary that stores each game's move list. |
| `replay.py` | Rebuilds and displays a finished game from its move list. |

## How It Works

- **Board:** a list of 6 rows, each a list of 7 cells. Row index `0` is the top of the board and row index `5` is the bottom.
- **Piece placement:** instead of scanning a column on every turn, the game keeps a dictionary (`possible_placement_of_piece`) that maps each column to the row where the next piece will land. Every column starts at `5` (the bottom row), and the value decreases by 1 after each drop. A value of `-1` means the column is full, so placing a piece takes constant time.
- **Win detection:** `Outcome.py` checks rows, columns, and both diagonal directions. For diagonals, it precomputes the starting cells from which a four-in-a-row fits on the board, so only valid positions are checked.
- **Move recording and replay:** each successful move's column number is added to a move list for that game. The lists are stored in a dictionary keyed by game number. A replay creates a new board and feeds the moves back through the same placement code used in live play.

## Known Limitations

- After answering `y` to play again, the previous game's finished board is displayed once more before the new game begins.
- New games are started through recursion, so an extremely long match (hundreds of games) could hit Python's recursion limit.
- Replays print every position at once rather than stepping through moves one at a time.
