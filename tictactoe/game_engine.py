"""Game engine for 4x4 Tic Tac Toe."""

from enum import Enum
from tictactoe.board import Board, CellState
from tictactoe.win_detection import check_win


class GameStatus(Enum):
    """Represents the current status of the game."""
    IN_PROGRESS = 0
    X_WINS = 1
    O_WINS = 2
    DRAW = 3


class GameEngine:
    """Manages game flow, rules, and state for 4x4 Tic Tac Toe."""
    
    def __init__(self):
        """Initialize a new game engine."""
        self.board = Board()
        self.current_player = CellState.X
        self.game_status = GameStatus.IN_PROGRESS
    
    def initialize(self, starting_player: CellState):
        """
        Set up a new game.
        
        Args:
            starting_player: The player who goes first (X or O)
        """
        if starting_player not in [CellState.X, CellState.O]:
            raise ValueError("Starting player must be X or O")
        
        self.board.initialize()
        self.current_player = starting_player
        self.game_status = GameStatus.IN_PROGRESS
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Attempt to make a move at the specified position.
        
        Args:
            row: Row index (0-3)
            col: Column index (0-3)
            
        Returns:
            True if the move was successful, False otherwise
        """
        # Check if game is still in progress
        if self.game_status != GameStatus.IN_PROGRESS:
            return False
        
        # Try to place the mark
        if self.board.set_cell(row, col, self.current_player):
            # Check if game is over
            self.check_game_over()
            
            # Switch player if game continues
            if self.game_status == GameStatus.IN_PROGRESS:
                self.switch_player()
            
            return True
        
        return False
    
    def check_game_over(self):
        """Check if the game has ended and update status accordingly."""
        # Check for win
        if check_win(self.board, self.current_player):
            if self.current_player == CellState.X:
                self.game_status = GameStatus.X_WINS
            else:
                self.game_status = GameStatus.O_WINS
        # Check for draw
        elif self.board.is_full():
            self.game_status = GameStatus.DRAW
    
    def switch_player(self):
        """Switch to the other player."""
        if self.current_player == CellState.X:
            self.current_player = CellState.O
        else:
            self.current_player = CellState.X
    
    def get_status(self) -> GameStatus:
        """
        Get the current game status.
        
        Returns:
            The current game status
        """
        return self.game_status
