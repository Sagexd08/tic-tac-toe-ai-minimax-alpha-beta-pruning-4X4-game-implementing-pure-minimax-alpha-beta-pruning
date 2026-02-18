"""Board component for 4x4 Tic Tac Toe game."""

from typing import List, Tuple, Optional
from enum import Enum


class CellState(Enum):
    """Represents the state of a cell on the board."""
    EMPTY = 0
    X = 1
    O = 2


class Board:
    """Represents a 4x4 Tic Tac Toe board."""
    
    def __init__(self):
        """Initialize a new board with all cells empty."""
        self.cells = [CellState.EMPTY] * 16
    
    def initialize(self):
        """Set all cells to empty."""
        self.cells = [CellState.EMPTY] * 16
    
    def get_cell(self, row: int, col: int) -> CellState:
        """
        Retrieve the state of a cell.
        
        Args:
            row: Row index (0-3)
            col: Column index (0-3)
            
        Returns:
            The state of the cell (EMPTY, X, or O)
        """
        if not (0 <= row < 4 and 0 <= col < 4):
            raise ValueError(f"Invalid cell position: ({row}, {col})")
        return self.cells[row * 4 + col]
    
    def set_cell(self, row: int, col: int, mark: CellState) -> bool:
        """
        Place a mark in a cell if it's empty.
        
        Args:
            row: Row index (0-3)
            col: Column index (0-3)
            mark: The mark to place (X or O)
            
        Returns:
            True if the mark was placed, False if the cell was occupied
        """
        if not (0 <= row < 4 and 0 <= col < 4):
            raise ValueError(f"Invalid cell position: ({row}, {col})")
        
        if mark == CellState.EMPTY:
            raise ValueError("Cannot set cell to EMPTY")
        
        index = row * 4 + col
        if self.cells[index] == CellState.EMPTY:
            self.cells[index] = mark
            return True
        return False
    
    def is_full(self) -> bool:
        """
        Check if the board is completely filled.
        
        Returns:
            True if all cells are occupied, False otherwise
        """
        return all(cell != CellState.EMPTY for cell in self.cells)
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get a list of all empty cell positions.
        
        Returns:
            List of (row, col) tuples for empty cells
        """
        empty_cells = []
        for i, cell in enumerate(self.cells):
            if cell == CellState.EMPTY:
                row = i // 4
                col = i % 4
                empty_cells.append((row, col))
        return empty_cells
    
    def copy(self) -> 'Board':
        """
        Create a deep copy of the board.
        
        Returns:
            A new Board instance with the same state
        """
        new_board = Board()
        new_board.cells = self.cells.copy()
        return new_board
