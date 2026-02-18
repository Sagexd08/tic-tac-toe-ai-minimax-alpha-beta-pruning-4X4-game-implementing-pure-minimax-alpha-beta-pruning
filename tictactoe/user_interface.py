"""User interface for 4x4 Tic Tac Toe game."""

from tictactoe.game_engine import GameEngine, GameStatus
from tictactoe.ai_opponent import AIOpponent
from tictactoe.board import CellState


class UserInterface:
    """CLI-based user interface for the game."""
    
    def __init__(self):
        """Initialize the user interface."""
        self.game_engine = GameEngine()
        self.ai_opponent = None
    
    def start_game(self):
        """Start and run the game loop."""
        print("Welcome to 4x4 Tic Tac Toe!")
        print("You are X, AI is O")
        print()
        
        # Initialize game with player going first
        self.game_engine.initialize(CellState.X)
        self.ai_opponent = AIOpponent(CellState.O)
        
        # Main game loop
        while self.game_engine.get_status() == GameStatus.IN_PROGRESS:
            self.display_board()
            
            if self.game_engine.current_player == CellState.X:
                self.handle_player_turn()
            else:
                self.handle_ai_turn()
        
        # Game over
        self.display_board()
        self.display_game_result()
    
    def display_board(self):
        """Display the current board state."""
        print("\n  0   1   2   3")
        print("  " + "-" * 15)
        
        for row in range(4):
            print(f"{row}|", end="")
            for col in range(4):
                cell = self.game_engine.board.get_cell(row, col)
                if cell == CellState.X:
                    symbol = " X "
                elif cell == CellState.O:
                    symbol = " O "
                else:
                    symbol = "   "
                
                print(symbol, end="")
                if col < 3:
                    print("|", end="")
            print("|")
            if row < 3:
                print("  " + "-" * 15)
        print()
    
    def get_player_input(self):
        """
        Get move input from the player.
        
        Returns:
            Tuple of (row, col)
        """
        while True:
            try:
                move_input = input("Enter your move (row col): ").strip()
                parts = move_input.split()
                
                if len(parts) != 2:
                    print("Please enter row and column separated by space (e.g., '0 1')")
                    continue
                
                row = int(parts[0])
                col = int(parts[1])
                
                if not (0 <= row < 4 and 0 <= col < 4):
                    print("Row and column must be between 0 and 3")
                    continue
                
                return row, col
            
            except ValueError:
                print("Please enter valid numbers")
            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")
                exit(0)
    
    def handle_player_turn(self):
        """Handle the player's turn."""
        print("Your turn (X)")
        
        while True:
            row, col = self.get_player_input()
            
            if self.game_engine.make_move(row, col):
                break
            else:
                print("Invalid move! That cell is already occupied. Try again.")
    
    def handle_ai_turn(self):
        """Handle the AI's turn."""
        print("AI is thinking...")
        
        row, col = self.ai_opponent.get_best_move(self.game_engine.board)
        self.game_engine.make_move(row, col)
        
        print(f"AI played at position ({row}, {col})")
    
    def display_game_result(self):
        """Display the final game result."""
        status = self.game_engine.get_status()
        
        print("=" * 30)
        if status == GameStatus.X_WINS:
            print("Congratulations! You win!")
        elif status == GameStatus.O_WINS:
            print("AI wins! Better luck next time.")
        else:
            print("It's a draw!")
        print("=" * 30)
