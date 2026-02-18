"""Unit tests for win detection logic."""

import pytest
from tictactoe.board import Board, CellState
from tictactoe.win_detection import (
    check_row_win, check_column_win, check_diagonal_win, check_win
)


class TestRowWinDetection:
    """Tests for row win detection."""
    
    def test_row_0_win(self):
        """Test win detection for row 0."""
        board = Board()
        for col in range(4):
            board.set_cell(0, col, CellState.X)
        assert check_row_win(board, CellState.X) is True
        assert check_row_win(board, CellState.O) is False
    
    def test_row_1_win(self):
        """Test win detection for row 1."""
        board = Board()
        for col in range(4):
            board.set_cell(1, col, CellState.O)
        assert check_row_win(board, CellState.O) is True
        assert check_row_win(board, CellState.X) is False
    
    def test_row_2_win(self):
        """Test win detection for row 2."""
        board = Board()
        for col in range(4):
            board.set_cell(2, col, CellState.X)
        assert check_row_win(board, CellState.X) is True
    
    def test_row_3_win(self):
        """Test win detection for row 3."""
        board = Board()
        for col in range(4):
            board.set_cell(3, col, CellState.O)
        assert check_row_win(board, CellState.O) is True
    
    def test_no_row_win(self):
        """Test that incomplete rows don't trigger win."""
        board = Board()
        board.set_cell(0, 0, CellState.X)
        board.set_cell(0, 1, CellState.X)
        board.set_cell(0, 2, CellState.X)
        # Missing (0, 3)
        assert check_row_win(board, CellState.X) is False


class TestColumnWinDetection:
    """Tests for column win detection."""
    
    def test_column_0_win(self):
        """Test win detection for column 0."""
        board = Board()
        for row in range(4):
            board.set_cell(row, 0, CellState.X)
        assert check_column_win(board, CellState.X) is True
        assert check_column_win(board, CellState.O) is False
    
    def test_column_1_win(self):
        """Test win detection for column 1."""
        board = Board()
        for row in range(4):
            board.set_cell(row, 1, CellState.O)
        assert check_column_win(board, CellState.O) is True
    
    def test_column_2_win(self):
        """Test win detection for column 2."""
        board = Board()
        for row in range(4):
            board.set_cell(row, 2, CellState.X)
        assert check_column_win(board, CellState.X) is True
    
    def test_column_3_win(self):
        """Test win detection for column 3."""
        board = Board()
        for row in range(4):
            board.set_cell(row, 3, CellState.O)
        assert check_column_win(board, CellState.O) is True
    
    def test_no_column_win(self):
        """Test that incomplete columns don't trigger win."""
        board = Board()
        board.set_cell(0, 0, CellState.X)
        board.set_cell(1, 0, CellState.X)
        board.set_cell(2, 0, CellState.X)
        # Missing (3, 0)
        assert check_column_win(board, CellState.X) is False


class TestDiagonalWinDetection:
    """Tests for diagonal win detection."""
    
    def test_main_diagonal_win(self):
        """Test win detection for main diagonal."""
        board = Board()
        for i in range(4):
            board.set_cell(i, i, CellState.X)
        assert check_diagonal_win(board, CellState.X) is True
        assert check_diagonal_win(board, CellState.O) is False
    
    def test_anti_diagonal_win(self):
        """Test win detection for anti-diagonal."""
        board = Board()
        for i in range(4):
            board.set_cell(i, 3 - i, CellState.O)
        assert check_diagonal_win(board, CellState.O) is True
        assert check_diagonal_win(board, CellState.X) is False
    
    def test_no_diagonal_win(self):
        """Test that incomplete diagonals don't trigger win."""
        board = Board()
        board.set_cell(0, 0, CellState.X)
        board.set_cell(1, 1, CellState.X)
        board.set_cell(2, 2, CellState.X)
        # Missing (3, 3)
        assert check_diagonal_win(board, CellState.X) is False


class TestOverallWinDetection:
    """Tests for the combined check_win function."""
    
    def test_check_win_with_row(self):
        """Test check_win detects row wins."""
        board = Board()
        for col in range(4):
            board.set_cell(1, col, CellState.X)
        assert check_win(board, CellState.X) is True
    
    def test_check_win_with_column(self):
        """Test check_win detects column wins."""
        board = Board()
        for row in range(4):
            board.set_cell(row, 2, CellState.O)
        assert check_win(board, CellState.O) is True
    
    def test_check_win_with_diagonal(self):
        """Test check_win detects diagonal wins."""
        board = Board()
        for i in range(4):
            board.set_cell(i, i, CellState.X)
        assert check_win(board, CellState.X) is True
    
    def test_check_win_no_win(self):
        """Test check_win returns False when no win exists."""
        board = Board()
        board.set_cell(0, 0, CellState.X)
        board.set_cell(1, 1, CellState.O)
        board.set_cell(2, 2, CellState.X)
        assert check_win(board, CellState.X) is False
        assert check_win(board, CellState.O) is False
