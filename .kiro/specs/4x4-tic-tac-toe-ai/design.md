# Design Document: 4x4 Tic Tac Toe with AI Opponent

## Overview

This design describes a 4x4 Tic Tac Toe game where a human player competes against an AI opponent. The AI uses the minimax algorithm with alpha-beta pruning to make optimal moves. The system is structured with clear separation between game logic, AI decision-making, and user interface components.

The core challenge is implementing an efficient minimax algorithm that can handle the larger state space of a 4x4 board (compared to 3x3) while maintaining optimal play through alpha-beta pruning optimization.

## Architecture

The system follows a layered architecture:

```
┌─────────────────────────────────┐
│     User Interface Layer        │
│  (Display, Input Handling)      │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│      Game Engine Layer          │
│  (Rules, State, Turn Logic)     │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│       AI Decision Layer         │
│  (Minimax + Alpha-Beta)         │
└─────────────────────────────────┘
```

Each layer has distinct responsibilities:
- **UI Layer**: Handles presentation and user input
- **Game Engine**: Enforces rules, manages state, detects win/draw
- **AI Layer**: Implements minimax with alpha-beta pruning

## Components and Interfaces

### Board Component

Represents the 4x4 game board state.

```
class Board:
    cells: Array[16] of (Empty | X | O)
    
    function initialize():
        set all cells to Empty
    
    function get_cell(row: int, col: int) -> (Empty | X | O):
        return cells[row * 4 + col]
    
    function set_cell(row: int, col: int, mark: (X | O)) -> bool:
        if cells[row * 4 + col] is Empty:
            cells[row * 4 + col] = mark
            return true
        return false
    
    function is_full() -> bool:
        return all cells are not Empty
    
    function get_empty_cells() -> List[(row, col)]:
        return list of (row, col) where cells[row * 4 + col] is Empty
    
    function copy() -> Board:
        return deep copy of this board
```

### Game Engine Component

Manages game flow, rules, and state.

```
class GameEngine:
    board: Board
    current_player: (X | O)
    game_status: (InProgress | XWins | OWins | Draw)
    
    function initialize(starting_player: (X | O)):
        board.initialize()
        current_player = starting_player
        game_status = InProgress
    
    function make_move(row: int, col: int) -> bool:
        if game_status is not InProgress:
            return false
        
        if board.set_cell(row, col, current_player):
            check_game_over()
            if game_status is InProgress:
                switch_player()
            return true
        return false
    
    function check_game_over():
        if check_win(current_player):
            game_status = (XWins if current_player is X else OWins)
        else if board.is_full():
            game_status = Draw
    
    function check_win(player: (X | O)) -> bool:
        return check_rows(player) or 
               check_columns(player) or 
               check_diagonals(player)
    
    function check_rows(player: (X | O)) -> bool:
        for row in 0 to 3:
            if all cells in row equal player:
                return true
        return false
    
    function check_columns(player: (X | O)) -> bool:
        for col in 0 to 3:
            if all cells in column equal player:
                return true
        return false
    
    function check_diagonals(player: (X | O)) -> bool:
        // Main diagonal: (0,0), (1,1), (2,2), (3,3)
        if all main diagonal cells equal player:
            return true
        // Anti-diagonal: (0,3), (1,2), (2,1), (3,0)
        if all anti-diagonal cells equal player:
            return true
        return false
    
    function switch_player():
        current_player = (O if current_player is X else X)
    
    function get_status() -> (InProgress | XWins | OWins | Draw):
        return game_status
```

### AI Opponent Component

Implements minimax algorithm with alpha-beta pruning.

```
class AIOpponent:
    ai_mark: (X | O)
    player_mark: (X | O)
    
    function initialize(mark: (X | O)):
        ai_mark = mark
        player_mark = (O if mark is X else X)
    
    function get_best_move(board: Board) -> (row, col):
        best_score = -infinity
        best_move = null
        
        for each (row, col) in board.get_empty_cells():
            // Try this move
            test_board = board.copy()
            test_board.set_cell(row, col, ai_mark)
            
            // Evaluate using minimax
            score = minimax(test_board, 0, false, -infinity, +infinity)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move
    
    function minimax(board: Board, depth: int, is_maximizing: bool, 
                     alpha: float, beta: float) -> float:
        // Check terminal states
        if check_win(board, ai_mark):
            return 10 - depth  // Prefer faster wins
        if check_win(board, player_mark):
            return depth - 10  // Prefer slower losses
        if board.is_full():
            return 0  // Draw
        
        if is_maximizing:
            max_eval = -infinity
            for each (row, col) in board.get_empty_cells():
                test_board = board.copy()
                test_board.set_cell(row, col, ai_mark)
                eval = minimax(test_board, depth + 1, false, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  // Beta cutoff
            return max_eval
        else:
            min_eval = +infinity
            for each (row, col) in board.get_empty_cells():
                test_board = board.copy()
                test_board.set_cell(row, col, player_mark)
                eval = minimax(test_board, depth + 1, true, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  // Alpha cutoff
            return min_eval
    
    function check_win(board: Board, player: (X | O)) -> bool:
        // Same logic as GameEngine.check_win
        return check_rows(board, player) or 
               check_columns(board, player) or 
               check_diagonals(board, player)
```

### User Interface Component

Handles display and input.

```
class UserInterface:
    game_engine: GameEngine
    ai_opponent: AIOpponent
    
    function start_game():
        game_engine.initialize(X)  // Player is X, AI is O
        ai_opponent.initialize(O)
        
        while game_engine.get_status() is InProgress:
            display_board()
            
            if game_engine.current_player is X:
                handle_player_turn()
            else:
                handle_ai_turn()
        
        display_game_result()
    
    function display_board():
        // Display 4x4 grid with current marks
        for row in 0 to 3:
            for col in 0 to 3:
                cell = game_engine.board.get_cell(row, col)
                print cell value (X, O, or empty indicator)
    
    function handle_player_turn():
        display "Your turn (X)"
        (row, col) = get_player_input()
        
        if not game_engine.make_move(row, col):
            display "Invalid move, try again"
            handle_player_turn()
    
    function handle_ai_turn():
        display "AI is thinking..."
        (row, col) = ai_opponent.get_best_move(game_engine.board)
        game_engine.make_move(row, col)
        display "AI played at position (row, col)"
    
    function get_player_input() -> (row, col):
        // Get row and column from user
        // Implementation depends on UI type (CLI, GUI, web)
    
    function display_game_result():
        status = game_engine.get_status()
        if status is XWins:
            display "You win!"
        else if status is OWins:
            display "AI wins!"
        else:
            display "It's a draw!"
```

## Data Models

### Cell State
```
enum CellState:
    Empty
    X
    O
```

### Game Status
```
enum GameStatus:
    InProgress
    XWins
    OWins
    Draw
```

### Move
```
struct Move:
    row: int (0-3)
    col: int (0-3)
```

### Board State
```
struct BoardState:
    cells: Array[16] of CellState
    
    invariant: 0 <= row < 4 and 0 <= col < 4 for all cell accesses
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Board Initialization
*For any* newly created board, all 16 cells should be empty.
**Validates: Requirements 1.2**

### Property 2: Board State Round Trip
*For any* cell position and mark (X or O), setting that mark in the cell and then querying the cell should return the same mark.
**Validates: Requirements 1.3, 1.4**

### Property 3: Occupied Cell Immutability
*For any* cell that already contains a mark, attempting to place a different mark should fail and leave the cell unchanged.
**Validates: Requirements 1.5**

### Property 4: Valid Move Acceptance
*For any* empty cell and valid game state, placing a mark in that cell should succeed and the cell should contain the mark.
**Validates: Requirements 2.1**

### Property 5: Invalid Move Rejection
*For any* occupied cell, attempting to place a mark should fail and the entire board state should remain unchanged.
**Validates: Requirements 2.2**

### Property 6: Turn Alternation
*For any* sequence of valid moves starting from a known player, the current player should alternate between X and O after each move.
**Validates: Requirements 2.3, 7.2**

### Property 7: Turn Enforcement
*For any* game state where it is player X's turn, attempting to make a move as player O should fail.
**Validates: Requirements 2.4**

### Property 8: Row Win Detection
*For any* board configuration where four consecutive cells in the same row contain the same mark, the game should detect that mark's owner as the winner.
**Validates: Requirements 5.1**

### Property 9: Column Win Detection
*For any* board configuration where four consecutive cells in the same column contain the same mark, the game should detect that mark's owner as the winner.
**Validates: Requirements 5.2**

### Property 10: Main Diagonal Win Detection
*For any* board configuration where all four cells on the main diagonal (0,0), (1,1), (2,2), (3,3) contain the same mark, the game should detect that mark's owner as the winner.
**Validates: Requirements 5.3**

### Property 11: Anti-Diagonal Win Detection
*For any* board configuration where all four cells on the anti-diagonal (0,3), (1,2), (2,1), (3,0) contain the same mark, the game should detect that mark's owner as the winner.
**Validates: Requirements 5.4**

### Property 12: Draw Detection
*For any* board configuration where all 16 cells are filled and no win condition exists, the game should detect a draw.
**Validates: Requirements 6.1**

### Property 13: Game Termination
*For any* game state that reaches a terminal condition (win or draw), no further moves should be accepted and the game status should reflect the terminal state.
**Validates: Requirements 5.5, 6.2, 7.4**

### Property 14: Win Detection Timing
*For any* move that creates a winning configuration, the win should be detected immediately after that move is made.
**Validates: Requirements 2.5, 5.6**

### Property 15: Minimax Optimal Play
*For any* game position with a known optimal move (e.g., immediate win available, must block opponent's win), the minimax algorithm should select an optimal move.
**Validates: Requirements 3.1, 3.4, 4.1, 4.2, 4.3, 4.4**

### Property 16: Minimax Terminal State Scoring
*For any* terminal game state (win, loss, or draw), the minimax algorithm should assign the correct score: positive for AI win, negative for AI loss, zero for draw.
**Validates: Requirements 4.2**

### Property 17: Alpha-Beta Pruning Correctness
*For any* game position, the minimax result with alpha-beta pruning should be identical to the result without pruning, but evaluate fewer nodes.
**Validates: Requirements 3.2, 4.5, 4.6, 4.7**

### Property 18: Alpha-Beta Pruning Efficiency
*For any* game position where a cutoff is possible, alpha-beta pruning should stop evaluating remaining branches once beta <= alpha.
**Validates: Requirements 4.6**

### Property 19: AI Move Validity
*For any* board state where it's the AI's turn, the move selected by the AI should be a valid empty cell.
**Validates: Requirements 3.1**

### Property 20: Board Display Completeness
*For any* board state, the display output should contain representations of all 16 cells with their current marks (X, O, or empty).
**Validates: Requirements 8.1, 8.2**

### Property 21: Game Status Accuracy
*For any* game state, querying the game status should return the correct value: in-progress if the game can continue, or the appropriate terminal status (X wins, O wins, draw) if the game has ended.
**Validates: Requirements 7.5**

## Error Handling

The system handles several error conditions:

1. **Invalid Move Attempts**: When a player attempts to place a mark in an occupied cell, the move is rejected and the game state remains unchanged. The UI should inform the player of the invalid move.

2. **Out of Turn Moves**: If a move is attempted when it's not that player's turn, the move is rejected. This prevents race conditions in the game flow.

3. **Moves After Game End**: Once the game reaches a terminal state (win or draw), all further move attempts are rejected. The game status clearly indicates the game has ended.

4. **Invalid Cell Coordinates**: If a move specifies coordinates outside the 0-3 range for row or column, the move is rejected. Input validation should prevent this at the UI layer.

5. **AI Computation Errors**: If the AI encounters an unexpected state during minimax evaluation, it should handle gracefully (though this should not occur with correct implementation).

## Testing Strategy

The testing strategy employs both unit tests and property-based tests to ensure comprehensive coverage.

### Unit Testing Approach

Unit tests focus on:
- Specific board configurations with known outcomes (e.g., specific winning patterns)
- Edge cases like empty board, full board, single move remaining
- Integration between components (e.g., game engine coordinating with board and AI)
- Specific minimax scenarios with known optimal moves
- Error conditions (invalid moves, out of bounds, etc.)

Example unit test cases:
- Test that a new board has 16 empty cells
- Test that placing X at (0,0) on an empty board succeeds
- Test that a full row of X's is detected as a win
- Test that AI blocks an immediate opponent win
- Test that attempting to play in an occupied cell fails

### Property-Based Testing Approach

Property-based tests verify universal properties across randomly generated inputs. Each property test should run a minimum of 100 iterations to ensure comprehensive coverage.

The property-based testing library should be selected based on the implementation language:
- Python: Hypothesis
- JavaScript/TypeScript: fast-check
- Java: jqwik
- Other languages: appropriate PBT library

Each property test must include a comment tag referencing the design document:
```
// Feature: 4x4-tic-tac-toe-ai, Property 2: Board State Round Trip
```

Property test focus areas:
- **Board Operations**: Generate random cell positions and marks, verify round-trip consistency
- **Game State Transitions**: Generate random move sequences, verify turn alternation and state consistency
- **Win Detection**: Generate random winning configurations, verify all are detected
- **Minimax Correctness**: Generate random board positions, verify optimal moves in known scenarios
- **Alpha-Beta Pruning**: Generate random positions, verify pruning produces same results as full minimax

Example property tests:
- For any cell and mark, set then get should return the same mark (Property 2)
- For any sequence of valid moves, turns should alternate (Property 6)
- For any board with 4 in a row, win should be detected (Property 8)
- For any position, minimax with pruning equals minimax without pruning (Property 17)

### Test Coverage Goals

- 100% coverage of win detection logic (all rows, columns, diagonals)
- 100% coverage of move validation logic
- Comprehensive coverage of minimax algorithm including all branches
- Alpha-beta pruning verification with various board configurations
- Edge cases: empty board, full board, one move from win/draw

### Testing the Minimax Algorithm

Special attention is needed for testing the minimax implementation:

1. **Known Position Tests**: Use positions with known optimal moves (e.g., immediate win available, must block opponent)
2. **Symmetry Tests**: Symmetric positions should yield symmetric optimal moves
3. **Depth Tests**: Verify the algorithm explores to appropriate depths
4. **Pruning Verification**: Track node evaluations to confirm pruning reduces search space
5. **Optimality Tests**: In simple endgame positions, verify the AI makes the mathematically optimal choice

### Integration Testing

Integration tests verify the complete game flow:
- Full game simulation from start to finish
- Player vs AI game with scripted player moves
- AI vs AI game to verify both sides work correctly
- Game state persistence and restoration (if implemented)

The dual testing approach ensures both specific correctness (unit tests) and general correctness across all inputs (property tests), providing confidence in the system's reliability and correctness.
