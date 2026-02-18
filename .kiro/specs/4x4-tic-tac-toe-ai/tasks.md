# Implementation Plan: 4x4 Tic Tac Toe with AI Opponent

## Overview

This implementation plan breaks down the 4x4 Tic Tac Toe game with minimax AI into discrete coding tasks. The approach is incremental: build the board, add game rules, implement the AI, and finally create the user interface. Each step validates functionality through tests before moving forward.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create Python project directory structure
  - Set up virtual environment
  - Install testing framework (pytest)
  - Install property-based testing library (Hypothesis)
  - Create main package directory and __init__.py files
  - _Requirements: All_

- [ ] 2. Implement Board component
  - [x] 2.1 Create Board class with cell storage and initialization
    - Implement `__init__` method to create 16-cell array
    - Implement `initialize()` to set all cells to empty
    - Implement `get_cell(row, col)` to retrieve cell state
    - Implement `set_cell(row, col, mark)` to place marks with validation
    - Implement `is_full()` to check if board is complete
    - Implement `get_empty_cells()` to return list of available positions
    - Implement `copy()` for deep copying board state
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  
  - [ ]* 2.2 Write property test for board initialization
    - **Property 1: Board Initialization**
    - **Validates: Requirements 1.2**
  
  - [ ]* 2.3 Write property test for board state round trip
    - **Property 2: Board State Round Trip**
    - **Validates: Requirements 1.3, 1.4**
  
  - [ ]* 2.4 Write property test for occupied cell immutability
    - **Property 3: Occupied Cell Immutability**
    - **Validates: Requirements 1.5**
  
  - [ ]* 2.5 Write unit tests for Board edge cases
    - Test out-of-bounds access handling
    - Test empty board state
    - Test full board detection
    - _Requirements: 1.1, 1.2, 1.5_

- [ ] 3. Implement win detection logic
  - [x] 3.1 Create helper functions for win checking
    - Implement `check_row_win(board, player)` for all 4 rows
    - Implement `check_column_win(board, player)` for all 4 columns
    - Implement `check_diagonal_win(board, player)` for both diagonals
    - Implement `check_win(board, player)` that combines all checks
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [ ]* 3.2 Write property test for row win detection
    - **Property 8: Row Win Detection**
    - **Validates: Requirements 5.1**
  
  - [ ]* 3.3 Write property test for column win detection
    - **Property 9: Column Win Detection**
    - **Validates: Requirements 5.2**
  
  - [ ]* 3.4 Write property test for main diagonal win detection
    - **Property 10: Main Diagonal Win Detection**
    - **Validates: Requirements 5.3**
  
  - [ ]* 3.5 Write property test for anti-diagonal win detection
    - **Property 11: Anti-Diagonal Win Detection**
    - **Validates: Requirements 5.4**
  
  - [ ]* 3.6 Write unit tests for specific win patterns
    - Test each row win scenario
    - Test each column win scenario
    - Test both diagonal win scenarios
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 4. Implement GameEngine component
  - [x] 4.1 Create GameEngine class with state management
    - Implement `__init__` to initialize board and game state
    - Implement `initialize(starting_player)` to set up new game
    - Implement `make_move(row, col)` with validation
    - Implement `check_game_over()` to detect terminal states
    - Implement `switch_player()` for turn alternation
    - Implement `get_status()` to return current game status
    - Integrate win detection functions from step 3
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 5.5, 5.6, 6.1, 6.2, 6.3, 7.1, 7.2, 7.3, 7.4, 7.5_
  
  - [ ]* 4.2 Write property test for valid move acceptance
    - **Property 4: Valid Move Acceptance**
    - **Validates: Requirements 2.1**
  
  - [ ]* 4.3 Write property test for invalid move rejection
    - **Property 5: Invalid Move Rejection**
    - **Validates: Requirements 2.2**
  
  - [ ]* 4.4 Write property test for turn alternation
    - **Property 6: Turn Alternation**
    - **Validates: Requirements 2.3, 7.2**
  
  - [ ]* 4.5 Write property test for turn enforcement
    - **Property 7: Turn Enforcement**
    - **Validates: Requirements 2.4**
  
  - [ ]* 4.6 Write property test for draw detection
    - **Property 12: Draw Detection**
    - **Validates: Requirements 6.1**
  
  - [ ]* 4.7 Write property test for game termination
    - **Property 13: Game Termination**
    - **Validates: Requirements 5.5, 6.2, 7.4**
  
  - [ ]* 4.8 Write property test for win detection timing
    - **Property 14: Win Detection Timing**
    - **Validates: Requirements 2.5, 5.6**
  
  - [ ]* 4.9 Write property test for game status accuracy
    - **Property 21: Game Status Accuracy**
    - **Validates: Requirements 7.5**
  
  - [ ]* 4.10 Write unit tests for GameEngine
    - Test game initialization
    - Test move validation edge cases
    - Test status transitions
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 7.1, 7.4, 7.5_

- [x] 5. Checkpoint - Ensure core game logic works
  - Run all tests to verify board and game engine functionality
  - Ensure all tests pass, ask the user if questions arise

- [ ] 6. Implement Minimax algorithm without pruning
  - [x] 6.1 Create AIOpponent class with basic minimax
    - Implement `__init__(ai_mark)` to set AI and player marks
    - Implement `minimax(board, depth, is_maximizing)` recursive function
    - Implement terminal state evaluation (win/loss/draw scoring)
    - Implement `get_best_move(board)` to find optimal move
    - Use win detection functions from step 3
    - _Requirements: 3.1, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4_
  
  - [ ]* 6.2 Write property test for minimax terminal state scoring
    - **Property 16: Minimax Terminal State Scoring**
    - **Validates: Requirements 4.2**
  
  - [ ]* 6.3 Write unit tests for minimax on known positions
    - Test immediate win detection
    - Test blocking opponent's win
    - Test simple endgame scenarios
    - _Requirements: 3.1, 3.4, 4.1, 4.2, 4.3, 4.4_

- [ ] 7. Add alpha-beta pruning optimization
  - [x] 7.1 Enhance minimax with alpha-beta pruning
    - Add alpha and beta parameters to minimax function
    - Implement alpha updates in maximizing nodes
    - Implement beta updates in minimizing nodes
    - Implement cutoff logic when beta <= alpha
    - Update `get_best_move` to initialize alpha and beta
    - _Requirements: 3.2, 4.5, 4.6, 4.7_
  
  - [ ]* 7.2 Write property test for alpha-beta pruning correctness
    - **Property 17: Alpha-Beta Pruning Correctness**
    - **Validates: Requirements 3.2, 4.5, 4.6, 4.7**
  
  - [ ]* 7.3 Write property test for alpha-beta pruning efficiency
    - **Property 18: Alpha-Beta Pruning Efficiency**
    - Track node evaluations to verify pruning reduces search
    - **Validates: Requirements 4.6**
  
  - [ ]* 7.4 Write property test for AI move validity
    - **Property 19: AI Move Validity**
    - **Validates: Requirements 3.1**
  
  - [ ]* 7.5 Write property test for minimax optimal play
    - **Property 15: Minimax Optimal Play**
    - Test on positions with known optimal moves
    - **Validates: Requirements 3.1, 3.4, 4.1, 4.2, 4.3, 4.4**
  
  - [ ]* 7.6 Write unit tests for alpha-beta pruning
    - Test that pruning produces same results as full minimax
    - Test cutoff scenarios
    - Verify alpha and beta value propagation
    - _Requirements: 3.2, 4.5, 4.6, 4.7_

- [ ] 8. Checkpoint - Ensure AI works correctly
  - Run all tests including AI tests
  - Verify AI makes optimal moves in test scenarios
  - Ensure all tests pass, ask the user if questions arise

- [ ] 9. Implement User Interface
  - [x] 9.1 Create CLI-based UserInterface class
    - Implement `display_board()` to show 4x4 grid with marks
    - Implement `get_player_input()` to read row and column from user
    - Implement `handle_player_turn()` for player move processing
    - Implement `handle_ai_turn()` for AI move processing with feedback
    - Implement `display_game_result()` to show final outcome
    - Implement `start_game()` main game loop
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.6_
  
  - [ ]* 9.2 Write property test for board display completeness
    - **Property 20: Board Display Completeness**
    - **Validates: Requirements 8.1, 8.2**
  
  - [ ]* 9.3 Write unit tests for UI components
    - Test board display formatting
    - Test input parsing
    - Test game result display
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 10. Create main entry point and wire components together
  - [x] 10.1 Create main.py with game initialization
    - Import all components (Board, GameEngine, AIOpponent, UserInterface)
    - Create main() function that instantiates and starts the game
    - Add command-line argument parsing for options (who goes first, etc.)
    - Add proper error handling and graceful exit
    - _Requirements: All_
  
  - [ ]* 10.2 Write integration tests for full game flow
    - Test complete game from start to player win
    - Test complete game from start to AI win
    - Test complete game from start to draw
    - _Requirements: All_

- [ ] 11. Final checkpoint and polish
  - Run complete test suite (unit + property tests)
  - Verify game plays correctly end-to-end
  - Add docstrings and code comments
  - Create README with instructions to run the game
  - Ensure all tests pass, ask the user if questions arise

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests should run minimum 100 iterations each
- The minimax algorithm is the core of this project - steps 6-8 are critical
- Alpha-beta pruning should not change the AI's move selection, only improve performance
- All property tests must include comment tags: `# Feature: 4x4-tic-tac-toe-ai, Property N: [title]`
