# Chess Bot

A command-line chess game where you play against the [Stockfish](https://stockfishchess.org/) engine at ten difficulty levels. Final project for Harvard's [CS50P: Introduction to Programming with Python](https://cs50.harvard.edu/python/).

**Video demo:** [Watch on YouTube](https://youtu.be/P1AOS6DxWe4)

## Features

- **Ten difficulty levels.** Level 1 always plays Stockfish's best move. At higher levels the bot asks Stockfish for its top *N* candidate moves (multi-PV analysis, where *N* is the level) and picks one at random, so the play gets weaker and less predictable.
- **Move validation.** Only legal moves in standard algebraic notation are accepted. After an illegal move the game lists all legal moves.
- **Board display.** The board is drawn in the terminal with Unicode chess pieces and coordinates.
- **Resign** with `Ctrl+D` (Linux/macOS) or `Ctrl+Z` then `Enter` (Windows).
- **Game export.** Save the move history to a CSV file (`move,white,black`).
- **Unit tests** with `pytest`.

## Requirements

- Python 3.10 or newer
- [python-chess](https://python-chess.readthedocs.io/) (installed from `requirements.txt`)
- The Stockfish engine

## Installation

```bash
git clone https://github.com/ammarjamaleh/chess-bot.git
cd chess-bot
pip install -r requirements.txt
```

Download Stockfish from [stockfishchess.org/download](https://stockfishchess.org/download/). The program finds it in one of two ways:

1. Add the Stockfish executable to your `PATH`, or
2. Set the `STOCKFISH_PATH` environment variable to the full path of the executable.

Example on Windows (PowerShell):

```powershell
$env:STOCKFISH_PATH = "C:\tools\stockfish\stockfish.exe"
```

Example on Linux/macOS:

```bash
export STOCKFISH_PATH=/usr/local/bin/stockfish
```

## Usage

```bash
python project.py
```

1. Enter a level from 1 (hardest) to 10 (easiest).
2. Type your moves in standard algebraic notation, for example `e4`, `Nf3`, `O-O`. Moves that give check or mate must include the symbol, for example `Qh5+`.
3. At the end of the game you can save the move history to a CSV file.

## Tests

```bash
pytest
```

Tests that need the engine are skipped automatically when Stockfish is not found.

## Project structure

| File | Purpose |
| --- | --- |
| `project.py` | Game loop and helper functions (`get_level`, `get_user_move`, `get_computer_move`, `save_game`, `display_chess_board`, `find_stockfish`) |
| `test_project.py` | `pytest` tests |
| `requirements.txt` | Python dependencies |

## Design notes

- **Difficulty by move selection, not only by time.** Limiting Stockfish's thinking time was not enough to get a smooth progression, so each level samples from a different number of the engine's best candidate moves.
- **No graphics library.** Unicode pieces keep the game runnable in any terminal.
- **CSV for saved games.** It is human-readable and opens in any spreadsheet.

## Known limitations and ideas

- The engine process is started again for every computer move. Keeping one engine session open for the whole game would be faster.
- Moves must be typed exactly as shown in the list of legal moves, including `+` and `#`.
- Resignation is stored in the CSV by adding `#` to the last computer move; a dedicated result field would be clearer.

## Project history
Originally submitted in October 2025 as my CS50P final project. Later improved: portable Stockfish path via STOCKFISH_PATH, bug fixes in the game loop, and more reliable tests.

## License

MIT, see [LICENSE](LICENSE).

## Acknowledgments

Thanks to the [Stockfish](https://stockfishchess.org/) team and the [python-chess](https://github.com/niklasf/python-chess) project.
