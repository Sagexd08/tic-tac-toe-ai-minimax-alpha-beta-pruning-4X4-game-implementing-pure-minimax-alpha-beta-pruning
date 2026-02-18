"""Unit tests for the AI opponent."""

import pytest
from tictactoe.ai_opponent import AIOpponent
from tictactoe.board import Board, CellState


class TestAIOpponentInitialization:
    """Tests for AI opponent initialization."""
    
    def test_initialize_with_x(self):
        """Test initializing AI with X mark."""
        ai = AIOpponent(CellState.X)
        assert ai.ai_mark == CellState.X
        assert ai.player_mark == CellState.O
    
    def test_initialize_with_o(self):
        """Test initializing AI with O mark."""
        ai = AIOpponent(CellState.O)
        assert ai.ai_mark == CellState.O
        assert ai.player_mark == CellState.X
    
    def test_initialize_with_invalid_mark(self):
        """Test that initializing with EMPTY raises error."""
        with pytest.raises(ValueError):
            AIOpponent(CellState.EMPTY)


class TestMinimaxBasicScenarios:
    """Tests for minimax algorithm in basic scenarios."""
    
    def test_ai_takes_immediate_win(self):
        """Test that AI takes an immediate winning move."""
        board = Board()
        ai = AIOpponent(CellState.X)
        
        # Set up board where X can win at (0, 3) - fill most of board to speed up test
        # X X X _
        # O O X O
        # X O X O
        # O X O X
        board.set_cell(0, 0, CellState.X)
        board.set_cell(0, 1, CellState.X)
        board.set_cell(0, 2, CellState.X)
        board.set_cell(1, 0, CellState.O)
        board.set_cell(1, 1, CellState.O)
        board.set_cell(1, 2, CellState.X)
        board.set_cell(1, 3, CellState.O)
        board.set_cell(2, 0, CellState.X)
        board.set_cell(2, 1, CellState.O)
        board.set_cell(2, 2, CellState.X)
        board.set_cell(2, 3, CellState.O)
        board.set_cell(3, 0, CellState.O)
        board.set_cell(3, 1, CellState.X)
        board.set_cell(3, 2, CellState.O)
        board.set_cell(3, 3, CellState.X)
        
        move = ai.get_best_move(board)
        assert move == (0, 3)
    
    def test_ai_blocks_opponent_win(self):
        """Test that AI blocks opponent's winning move."""
        board = Board()
        ai = AIOpponent(CellState.X)
        
        # Set up board where O is about to win at (0, 3) - fill most of board
        # O O O _
        # X X O X
        # O X X O
        # X O X O
        board.set_cell(0, 0, CellState.O)
        board.set_cell(0, 1, CellState.O)
        board.set_cell(0, 2, CellState.O)
        board.set_cell(1, 0, CellState.X)
        board.set_cell(1, 1, CellState.X)
        board.set_cell(1, 2, CellState.O)
        board.set_cell(1, 3, CellState.X)
        board.set_cell(2, 0, CellState.O)
        board.set_cell(2, 1, CellState.X)
        board.set_cell(2, 2, CellState.X)
        board.set_cell(2, 3, CellState.O)
        board.set_cell(3, 0, CellState.X)
        board.set_cell(3, 1, CellState.O)
        board.set_cell(3, 2, CellState.X)
        board.set_cell(3, 3, CellState.O)
        
        move = ai.get_best_move(board)
        assert move == (0, 3)
    
    def test_ai_prefers_win_over_block(self):
        """Test that AI prefers winning over blocking."""
        board = Board()
        ai = AIOpponent(CellState.X)
        
        # Set up board where both X and O can win - fill most cells
        # X X X _
        # O O O _
        # X O X O
        # O X O X
        board.set_cell(0, 0, CellState.X)
        board.set_cell(0, 1, CellState.X)
        board.set_cell(0, 2, CellState.X)
        board.set_cell(1, 0, CellState.O)
        board.set_cell(1, 1, CellState.O)
        board.set_cell(1, 2, CellState.O)
        board.set_cell(2, 0, CellState.X)
        board.set_cell(2, 1, CellState.O)
        board.set_cell(2, 2, CellState.X)
        board.set_cell(2, 3, CellState.O)
        board.set_cell(3, 0, CellState.O)
        board.set_cell(3, 1, CellState.X)
        board.set_cell(3, 2, CellState.O)
        board.set_cell(3, 3, CellState.X)
        
        move = ai.get_best_move(board)
        # AI should take the win at (0, 3) rather than block at (1, 3)
        assert move == (0, 3)


class TestMinimaxTerminalStates:
    """Tests for minimax terminal state evaluation."""
    
    def test_minimax_detects_ai_win(self):
        """Test that minimax correctly scores AI wins."""
        board = Board()
        ai = AIOpponent(CellState.X)
        
        # Create a winning board for X
        for col in range(4):
            board.set_cell(0, col, CellState.X)
        
        score = ai.minimax(board, 0, True)
        assert score > 0  # Positive score for AI win
    
    def test_minimax_detects_player_win(self):
        """Test that minimax correctly scores player wins."""
        board = Board()
        ai = AIOpponent(CellState.X)
        
        # Create a winning board for O
        for col in range(4):
            board.set_cell(0, col, CellState.O)
        
        score = ai.minimax(board, 0, True)
        assert score < 0  # Negative score for player win
    
    def test_minimax_detects_draw(self):
        """Test that minimax correctly scores draws."""
        board = Board()
        ai = AIOpponent(CellState.X)
        
        # Create a draw board
        # X X O O
        # O O X X
        # X X O O
        # O O X X
        pattern = [
            (CellState.X, CellState.X, CellState.O, CellState.O),
            (CellState.O, CellState.O, CellState.X, CellState.X),
            (CellState.X, CellState.X, CellState.O, CellState.O),
            (CellState.O, CellState.O, CellState.X, CellState.X)
        ]
        
        for row in range(4):
            for col in range(4):
                board.set_cell(row, col, pattern[row][col])
        
        score = ai.minimax(board, 0, True)
        assert score == 0  # Zero score for draw

    def test_minimax_legacy_signature_compatibility(self):
        """Regression: minimax should work with legacy call signature."""
        board = Board()
        ai = AIOpponent(CellState.X)

        # Terminal winning position for X to keep evaluation fast and deterministic
        for col in range(4):
            board.set_cell(0, col, CellState.X)

        legacy_score = ai.minimax(board, 0, True)
        explicit_score = ai.minimax(board, 0, True, float('-inf'), float('inf'))

        assert legacy_score == explicit_score
        assert legacy_score > 0


class TestAIMoveValidity:
    """Tests for AI move validity."""
    
    def test_ai_only_selects_empty_cells(self):
        """Test that AI only selects empty cells."""
        board = Board()
        ai = AIOpponent(CellState.X)
        
        # Fill most of the board to speed up test
        board.set_cell(0, 0, CellState.X)
        board.set_cell(0, 1, CellState.O)
        board.set_cell(0, 2, CellState.X)
        board.set_cell(0, 3, CellState.O)
        board.set_cell(1, 0, CellState.X)
        board.set_cell(1, 1, CellState.O)
        board.set_cell(1, 2, CellState.X)
        board.set_cell(1, 3, CellState.O)
        board.set_cell(2, 0, CellState.O)
        board.set_cell(2, 1, CellState.X)
        board.set_cell(2, 2, CellState.O)
        board.set_cell(2, 3, CellState.X)
        board.set_cell(3, 0, CellState.O)
        board.set_cell(3, 1, CellState.X)
        # Leave (3, 2) and (3, 3) empty
        
        move = ai.get_best_move(board)
        row, col = move
        
        # Verify the selected cell is empty
        assert board.get_cell(row, col) == CellState.EMPTY
    
    def test_ai_makes_valid_move_on_nearly_full_board(self):
        """Test that AI makes a valid move on a nearly full board."""
        board = Board()
        ai = AIOpponent(CellState.X)
        
        # Fill board except for a few cells
        board.set_cell(0, 0, CellState.X)
        board.set_cell(0, 1, CellState.O)
        board.set_cell(0, 2, CellState.X)
        board.set_cell(0, 3, CellState.O)
        board.set_cell(1, 0, CellState.O)
        board.set_cell(1, 1, CellState.X)
        board.set_cell(1, 2, CellState.O)
        board.set_cell(1, 3, CellState.X)
        board.set_cell(2, 0, CellState.X)
        board.set_cell(2, 1, CellState.O)
        board.set_cell(2, 2, CellState.X)
        board.set_cell(2, 3, CellState.O)
        board.set_cell(3, 0, CellState.O)
        board.set_cell(3, 1, CellState.X)
        board.set_cell(3, 2, CellState.O)
        # Leave (3, 3) empty
        
        move = ai.get_best_move(board)
        row, col = move
        
        # Verify move is within bounds and cell is empty
        assert 0 <= row < 4
        assert 0 <= col < 4
        assert board.get_cell(row, col) == CellState.EMPTY
