# 4x4 Tic Tac Toe with AI Opponent

A Python implementation of 4x4 Tic Tac Toe featuring an AI opponent that uses the minimax algorithm with alpha-beta pruning optimization.

## Features

- 4x4 game board (16 cells instead of the traditional 9)
- Intelligent AI opponent using minimax with alpha-beta pruning
- Command-line interface
- Comprehensive test suite with unit and property-based tests

## Requirements

- Python 3.7 or higher
- pytest (for running tests)
- hypothesis (for property-based tests)

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Play

Run the game with:
```
python main.py
```

### Game Rules

- The board is a 4x4 grid with positions numbered 0-3 for both rows and columns
- You play as X, the AI plays as O
- Players alternate turns
- To win, get 4 marks in a row (horizontally, vertically, or diagonally)
- If all 16 cells are filled with no winner, the game is a draw

### Making Moves

When it's your turn, enter your move as two numbers separated by a space:
```
Enter your move (row col): 0 1
```

This places your mark at row 0, column 1.

## Running Tests

Run the complete test suite:
```
pytest tests/ -v
```

Run specific test files:
```
pytest tests/test_board.py -v
pytest tests/test_game_engine.py -v
pytest tests/test_win_detection.py -v
pytest tests/test_ai_opponent.py -v
```

## Project Structure

```
.
├── tictactoe/
│   ├── __init__.py
│   ├── board.py              # Board component
│   ├── game_engine.py        # Game logic and state management
│   ├── win_detection.py      # Win condition checking
│   ├── ai_opponent.py        # AI with minimax + alpha-beta pruning
│   └── user_interface.py     # CLI interface
├── tests/
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_game_engine.py
│   ├── test_win_detection.py
│   └── test_ai_opponent.py
├── main.py                   # Entry point
├── requirements.txt
└── README.md
```

## AI Algorithm

The AI uses the minimax algorithm with alpha-beta pruning:

- **Minimax**: Explores all possible game states to find the optimal move
- **Alpha-Beta Pruning**: Optimizes the search by eliminating branches that cannot affect the final decision
- **Scoring**: Prefers faster wins and slower losses

The AI plays optimally, making it very challenging to beat!

## Development

This project follows a spec-driven development approach with:
- Comprehensive requirements documentation
- Detailed design specifications
- Property-based testing for correctness verification
- Unit tests for specific scenarios

## License

This project is provided as-is for educational purposes.
