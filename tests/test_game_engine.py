"""Unit tests for the GameEngine component."""

import pytest
from tictactoe.game_engine import GameEngine, GameStatus
from tictactoe.board import CellState


class TestGameEngineInitialization:
    """Tests for game engine initialization."""
    
    def test_new_game_engine(self):
        """Test that a new game engine is properly initialized."""
        engine = GameEngine()
        assert engine.game_status == GameStatus.IN_PROGRESS
        assert engine.current_player == CellState.X
    
    def test_initialize_with_x(self):
        """Test initializing a game with X as starting player."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        assert engine.current_player == CellState.X
        assert engine.game_status == GameStatus.IN_PROGRESS
    
    def test_initialize_with_o(self):
        """Test initializing a game with O as starting player."""
        engine = GameEngine()
        engine.initialize(CellState.O)
        assert engine.current_player == CellState.O
        assert engine.game_status == GameStatus.IN_PROGRESS
    
    def test_initialize_with_invalid_player(self):
        """Test that initializing with EMPTY raises error."""
        engine = GameEngine()
        with pytest.raises(ValueError):
            engine.initialize(CellState.EMPTY)


class TestGameEngineMoves:
    """Tests for move handling."""
    
    def test_valid_move(self):
        """Test that valid moves are accepted."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        assert engine.make_move(0, 0) is True
        assert engine.board.get_cell(0, 0) == CellState.X
    
    def test_invalid_move_occupied_cell(self):
        """Test that moves to occupied cells are rejected."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        engine.make_move(0, 0)
        assert engine.make_move(0, 0) is False
    
    def test_turn_alternation(self):
        """Test that turns alternate between players."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        
        engine.make_move(0, 0)
        assert engine.current_player == CellState.O
        
        engine.make_move(0, 1)
        assert engine.current_player == CellState.X
        
        engine.make_move(1, 0)
        assert engine.current_player == CellState.O
    
    def test_move_after_game_ends(self):
        """Test that moves are rejected after game ends."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        
        # Create a winning position for X
        engine.make_move(0, 0)  # X
        engine.make_move(1, 0)  # O
        engine.make_move(0, 1)  # X
        engine.make_move(1, 1)  # O
        engine.make_move(0, 2)  # X
        engine.make_move(1, 2)  # O
        engine.make_move(0, 3)  # X wins
        
        # Try to make another move
        assert engine.make_move(2, 0) is False


class TestGameEngineWinDetection:
    """Tests for win detection."""
    
    def test_row_win_detection(self):
        """Test that row wins are detected."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        
        # X wins with row 0
        engine.make_move(0, 0)  # X
        engine.make_move(1, 0)  # O
        engine.make_move(0, 1)  # X
        engine.make_move(1, 1)  # O
        engine.make_move(0, 2)  # X
        engine.make_move(1, 2)  # O
        engine.make_move(0, 3)  # X wins
        
        assert engine.game_status == GameStatus.X_WINS
    
    def test_column_win_detection(self):
        """Test that column wins are detected."""
        engine = GameEngine()
        engine.initialize(CellState.O)
        
        # O wins with column 0
        engine.make_move(0, 0)  # O
        engine.make_move(0, 1)  # X
        engine.make_move(1, 0)  # O
        engine.make_move(1, 1)  # X
        engine.make_move(2, 0)  # O
        engine.make_move(2, 1)  # X
        engine.make_move(3, 0)  # O wins
        
        assert engine.game_status == GameStatus.O_WINS
    
    def test_diagonal_win_detection(self):
        """Test that diagonal wins are detected."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        
        # X wins with main diagonal
        engine.make_move(0, 0)  # X
        engine.make_move(0, 1)  # O
        engine.make_move(1, 1)  # X
        engine.make_move(0, 2)  # O
        engine.make_move(2, 2)  # X
        engine.make_move(0, 3)  # O
        engine.make_move(3, 3)  # X wins
        
        assert engine.game_status == GameStatus.X_WINS


class TestGameEngineDrawDetection:
    """Tests for draw detection."""
    
    def test_draw_detection(self):
        """Test that draws are detected when board is full."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        
        # Create a draw scenario - pattern that avoids 4 in a row/col/diagonal
        # X X O O
        # O O X X
        # X X O O
        # O O X X
        moves = [
            (0, 0), (0, 2), (0, 1), (0, 3),  # X, O, X, O
            (1, 2), (1, 0), (1, 3), (1, 1),  # X, O, X, O
            (2, 0), (2, 2), (2, 1), (2, 3),  # X, O, X, O
            (3, 2), (3, 0), (3, 3), (3, 1)   # X, O, X, O
        ]
        
        for row, col in moves:
            engine.make_move(row, col)
        
        assert engine.game_status == GameStatus.DRAW


class TestGameEngineStatus:
    """Tests for game status queries."""
    
    def test_get_status_in_progress(self):
        """Test getting status during game."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        engine.make_move(0, 0)
        assert engine.get_status() == GameStatus.IN_PROGRESS
    
    def test_get_status_after_win(self):
        """Test getting status after a win."""
        engine = GameEngine()
        engine.initialize(CellState.X)
        
        # X wins
        for col in range(4):
            engine.make_move(0, col)
            if col < 3:
                engine.make_move(1, col)
        
        assert engine.get_status() == GameStatus.X_WINS
