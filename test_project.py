import chess
import pytest

from project import (
    display_chess_board,
    find_stockfish,
    get_computer_move,
    get_level,
    get_user_move,
    save_game,
)

needs_stockfish = pytest.mark.skipif(
    find_stockfish() is None, reason="Stockfish is not installed (see README)"
)

MIDDLEGAME_MOVES = [
    "e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "d3", "Nf6",
    "c3", "O-O", "b4", "Bb6", "a4", "d6", "Bg5", "h5",
]


def test_get_level():
    assert get_level("1") == 1
    assert get_level("5") == 5
    assert get_level("10") == 10

    with pytest.raises(ValueError):
        get_level("0")

    with pytest.raises(ValueError):
        get_level("11")

    with pytest.raises(ValueError):
        get_level("cat")


def test_get_user_move():
    board = chess.Board()

    assert get_user_move(board, "e4") == "e4"
    assert get_user_move(board, "a3") == "a3"
    assert get_user_move(board, "Nf3") == "Nf3"

    with pytest.raises(chess.IllegalMoveError):
        get_user_move(board, "a5")

    with pytest.raises(chess.IllegalMoveError):
        get_user_move(board, "Qf3")

    with pytest.raises(chess.IllegalMoveError):
        get_user_move(board, "cat")

    with pytest.raises(chess.IllegalMoveError):
        get_user_move(board, "100")


def test_save_game(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_game([{"move": 1, "white": "e4", "black": "e5"}], "game")

    lines = (tmp_path / "game.csv").read_text().splitlines()
    assert lines[0] == "move,white,black"
    assert lines[1] == "1,e4,e5"


def test_display_chess_board(capsys):
    display_chess_board(chess.Board())
    output = capsys.readouterr().out

    assert "a b c d e f g h" in output
    assert "♜" in output
    assert "♔" in output


@needs_stockfish
def test_get_computer_move_returns_legal_moves():
    board = chess.Board()

    for num_moves in (1, 2, 5):
        moves = get_computer_move(board, num_moves)
        assert len(moves) == num_moves
        for move in moves:
            # parse_san raises an error if the move is illegal
            assert board.parse_san(move) in board.legal_moves


@needs_stockfish
def test_get_computer_move_midgame():
    board = chess.Board()
    for move in MIDDLEGAME_MOVES:
        board.push_san(move)

    moves = get_computer_move(board, 10)
    assert len(moves) == 10
    assert all(board.parse_san(move) in board.legal_moves for move in moves)
