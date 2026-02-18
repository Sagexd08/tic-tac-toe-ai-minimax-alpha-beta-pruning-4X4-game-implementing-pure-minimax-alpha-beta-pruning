"""AI opponent using minimax algorithm for 4x4 Tic Tac Toe."""

from typing import Tuple
from tictactoe.board import Board, CellState
from tictactoe.win_detection import check_win


class AIOpponent:
    """AI opponent that uses minimax algorithm to make optimal moves."""
    
    def __init__(self, ai_mark: CellState):
        """
        Initialize the AI opponent.
        
        Args:
            ai_mark: The mark the AI uses (X or O)
        """
        if ai_mark not in [CellState.X, CellState.O]:
            raise ValueError("AI mark must be X or O")
        
        self.ai_mark = ai_mark
        self.player_mark = CellState.O if ai_mark == CellState.X else CellState.X
    
    def get_best_move(self, board: Board, max_depth: int = None) -> Tuple[int, int]:
        """
        Find the best move using minimax algorithm with alpha-beta pruning.
        
        Args:
            board: The current game board
            max_depth: Maximum search depth (None for unlimited)
            
        Returns:
            Tuple of (row, col) for the best move
        """
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for row, col in board.get_empty_cells():
            # Try this move
            test_board = board.copy()
            test_board.set_cell(row, col, self.ai_mark)
            
            # Evaluate using minimax with alpha-beta pruning
            score = self.minimax(test_board, 0, False, alpha, beta, max_depth)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
            
            alpha = max(alpha, score)
        
        return best_move
    
    def minimax(self, board: Board, depth: int, is_maximizing: bool, 
                alpha: float, beta: float, max_depth: int = None) -> float:
        """
        Minimax algorithm with alpha-beta pruning to evaluate board positions.
        
        Args:
            board: The board to evaluate
            depth: Current depth in the search tree
            is_maximizing: True if maximizing player's turn, False otherwise
            alpha: Best score for maximizing player
            beta: Best score for minimizing player
            max_depth: Maximum search depth (None for unlimited)
            
        Returns:
            The score of the position
        """
        # Check terminal states
        if check_win(board, self.ai_mark):
            return 10 - depth  # Prefer faster wins
        if check_win(board, self.player_mark):
            return depth - 10  # Prefer slower losses
        if board.is_full():
            return 0  # Draw
        
        # Check depth limit
        if max_depth is not None and depth >= max_depth:
            return 0  # Neutral evaluation at depth limit
        
        if is_maximizing:
            max_eval = float('-inf')
            for row, col in board.get_empty_cells():
                test_board = board.copy()
                test_board.set_cell(row, col, self.ai_mark)
                eval_score = self.minimax(test_board, depth + 1, False, alpha, beta, max_depth)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in board.get_empty_cells():
                test_board = board.copy()
                test_board.set_cell(row, col, self.player_mark)
                eval_score = self.minimax(test_board, depth + 1, True, alpha, beta, max_depth)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
