import csv
import os
import random
import shutil
import sys

import chess
import chess.engine


def main():
    if find_stockfish() is None:
        sys.exit(
            "Stockfish not found. Install it and either add it to your PATH "
            "or set the STOCKFISH_PATH environment variable (see README)."
        )

    board = chess.Board()
    moves = []
    move = 1

    while True:
        try:
            level = get_level(input("Level: ").strip())
        except ValueError:
            print("Level must be between 1 and 10 (1 being extremely hard)")
        else:
            break

    display_chess_board(board)

    while not board.is_game_over():
        computer_move = ""

        try:
            while True:
                try:
                    user_move = get_user_move(board, input("Your move: ").strip())

                except chess.IllegalMoveError:
                    print("Illegal move!\n", f"Legal moves: {[board.san(m) for m in board.legal_moves]}")
                    print("If you would like to resign type (ctrl + d)/(ctrl + z)")

                else:
                    board.push_san(user_move)
                    display_chess_board(board)
                    break

        except EOFError:
            # The user resigned: mark the last computer move with "#"
            if moves:
                moves[-1]["black"] = moves[-1]["black"] + "#"
            break

        if not board.is_game_over():
            computer_move = random.choice(get_computer_move(board, level))
            board.push_san(computer_move)
            display_chess_board(board)
            print("Computer move:", computer_move)

        moves.append({"move": move, "white": user_move, "black": computer_move})
        move += 1

    save = input("Do you want to save the game?\n").lower()
    if save == "yes" or save == "y":
        file_name = input("File name: ")
        save_game(moves, file_name)


def find_stockfish():
    """Return the path to the Stockfish executable, or None if it is not found.

    Looks at the STOCKFISH_PATH environment variable first, then at the PATH.
    """
    return os.environ.get("STOCKFISH_PATH") or shutil.which("stockfish")


def get_user_move(b, m):
    legal_moves = [b.san(move) for move in b.legal_moves]

    if m in legal_moves:
        return m
    else:
        raise chess.IllegalMoveError


def get_computer_move(b, num_moves=1):
    engine_path = find_stockfish()
    if engine_path is None:
        raise FileNotFoundError(
            "Stockfish not found. Install it and set STOCKFISH_PATH (see README)."
        )

    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        if num_moves == 1:
            result = engine.play(b, chess.engine.Limit(time=2.0))
            return [b.san(result.move)]

        legal_moves_count = b.legal_moves.count()
        actual_num_moves = min(num_moves, legal_moves_count)

        analysis = engine.analyse(b, chess.engine.Limit(time=2.0), multipv=actual_num_moves)
        return [b.san(move_info["pv"][0]) for move_info in analysis]


def get_level(l):
    l = int(l)

    if not 1 <= l <= 10:
        raise ValueError
    return l


def save_game(m, f_n):
    with open(f"{f_n}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["move", "white", "black"])
        writer.writeheader()

        for move in m:
            writer.writerow(move)


def display_chess_board(b):
    pieces = {
        "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
        "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙",
        ".": "·",
    }

    board_rows = []
    fen = b.board_fen()
    for row in fen.split("/"):
        converted_row = ""
        for char in row:
            if char.isdigit():
                converted_row += "." * int(char)
            else:
                converted_row += char
        board_rows.append(converted_row)

    print("=" * 45)
    print("    a b c d e f g h")
    print("  " + "─" * 17)

    for i, row in enumerate(board_rows):
        print(f"{8-i} │", end=" ")
        for char in row:
            print(pieces[char], end=" ")
        print(f"│ {8-i}")

    print("  " + "─" * 17)
    print("    a b c d e f g h")
    print("=" * 45)


if __name__ == "__main__":
    main()
