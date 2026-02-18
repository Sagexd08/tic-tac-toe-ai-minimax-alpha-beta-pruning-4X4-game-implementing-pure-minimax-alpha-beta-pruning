"""Unit tests for the Board component."""

import pytest
from tictactoe.board import Board, CellState


class TestBoardInitialization:
    """Tests for board initialization."""
    
    def test_new_board_is_empty(self):
        """Test that a new board has all cells empty."""
        board = Board()
        for row in range(4):
            for col in range(4):
                assert board.get_cell(row, col) == CellState.EMPTY
    
    def test_initialize_clears_board(self):
        """Test that initialize() sets all cells to empty."""
        board = Board()
        board.set_cell(0, 0, CellState.X)
        board.set_cell(1, 1, CellState.O)
        board.initialize()
        for row in range(4):
            for col in range(4):
                assert board.get_cell(row, col) == CellState.EMPTY


class TestBoardCellOperations:
    """Tests for cell get/set operations."""
    
    def test_set_and_get_cell(self):
        """Test setting and getting a cell value."""
        board = Board()
        assert board.set_cell(0, 0, CellState.X) is True
        assert board.get_cell(0, 0) == CellState.X
        
        assert board.set_cell(2, 3, CellState.O) is True
        assert board.get_cell(2, 3) == CellState.O
    
    def test_cannot_overwrite_occupied_cell(self):
        """Test that occupied cells cannot be overwritten."""
        board = Board()
        board.set_cell(1, 1, CellState.X)
        assert board.set_cell(1, 1, CellState.O) is False
        assert board.get_cell(1, 1) == CellState.X
    
    def test_invalid_row_raises_error(self):
        """Test that invalid row indices raise ValueError."""
        board = Board()
        with pytest.raises(ValueError):
            board.get_cell(-1, 0)
        with pytest.raises(ValueError):
            board.get_cell(4, 0)
    
    def test_invalid_col_raises_error(self):
        """Test that invalid column indices raise ValueError."""
        board = Board()
        with pytest.raises(ValueError):
            board.get_cell(0, -1)
        with pytest.raises(ValueError):
            board.get_cell(0, 4)
    
    def test_cannot_set_empty(self):
        """Test that setting a cell to EMPTY raises ValueError."""
        board = Board()
        with pytest.raises(ValueError):
            board.set_cell(0, 0, CellState.EMPTY)


class TestBoardState:
    """Tests for board state queries."""
    
    def test_empty_board_not_full(self):
        """Test that an empty board is not full."""
        board = Board()
        assert board.is_full() is False
    
    def test_full_board_is_full(self):
        """Test that a completely filled board is detected as full."""
        board = Board()
        mark = CellState.X
        for row in range(4):
            for col in range(4):
                board.set_cell(row, col, mark)
                mark = CellState.O if mark == CellState.X else CellState.X
        assert board.is_full() is True
    
    def test_get_empty_cells_on_empty_board(self):
        """Test getting empty cells from an empty board."""
        board = Board()
        empty_cells = board.get_empty_cells()
        assert len(empty_cells) == 16
        assert (0, 0) in empty_cells
        assert (3, 3) in empty_cells
    
    def test_get_empty_cells_after_moves(self):
        """Test getting empty cells after some moves."""
        board = Board()
        board.set_cell(0, 0, CellState.X)
        board.set_cell(1, 1, CellState.O)
        board.set_cell(2, 2, CellState.X)
        
        empty_cells = board.get_empty_cells()
        assert len(empty_cells) == 13
        assert (0, 0) not in empty_cells
        assert (1, 1) not in empty_cells
        assert (2, 2) not in empty_cells
        assert (0, 1) in empty_cells


class TestBoardCopy:
    """Tests for board copying."""
    
    def test_copy_creates_independent_board(self):
        """Test that copy() creates an independent board."""
        board1 = Board()
        board1.set_cell(0, 0, CellState.X)
        board1.set_cell(1, 1, CellState.O)
        
        board2 = board1.copy()
        
        # Verify initial state is copied
        assert board2.get_cell(0, 0) == CellState.X
        assert board2.get_cell(1, 1) == CellState.O
        
        # Modify board2 and verify board1 is unchanged
        board2.set_cell(2, 2, CellState.X)
        assert board2.get_cell(2, 2) == CellState.X
        assert board1.get_cell(2, 2) == CellState.EMPTY
