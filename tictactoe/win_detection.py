"""Win detection logic for 4x4 Tic Tac Toe."""

from tictactoe.board import Board, CellState


def check_row_win(board: Board, player: CellState) -> bool:
    """
    Check if the player has won with four in a row.
    
    Args:
        board: The game board
        player: The player to check (X or O)
        
    Returns:
        True if the player has four in a row, False otherwise
    """
    for row in range(4):
        if all(board.get_cell(row, col) == player for col in range(4)):
            return True
    return False


def check_column_win(board: Board, player: CellState) -> bool:
    """
    Check if the player has won with four in a column.
    
    Args:
        board: The game board
        player: The player to check (X or O)
        
    Returns:
        True if the player has four in a column, False otherwise
    """
    for col in range(4):
        if all(board.get_cell(row, col) == player for row in range(4)):
            return True
    return False


def check_diagonal_win(board: Board, player: CellState) -> bool:
    """
    Check if the player has won with four in a diagonal.
    
    Args:
        board: The game board
        player: The player to check (X or O)
        
    Returns:
        True if the player has four in a diagonal, False otherwise
    """
    # Main diagonal: (0,0), (1,1), (2,2), (3,3)
    if all(board.get_cell(i, i) == player for i in range(4)):
        return True
    
    # Anti-diagonal: (0,3), (1,2), (2,1), (3,0)
    if all(board.get_cell(i, 3 - i) == player for i in range(4)):
        return True
    
    return False


def check_win(board: Board, player: CellState) -> bool:
    """
    Check if the player has won the game.
    
    Args:
        board: The game board
        player: The player to check (X or O)
        
    Returns:
        True if the player has won, False otherwise
    """
    return (check_row_win(board, player) or 
            check_column_win(board, player) or 
            check_diagonal_win(board, player))
