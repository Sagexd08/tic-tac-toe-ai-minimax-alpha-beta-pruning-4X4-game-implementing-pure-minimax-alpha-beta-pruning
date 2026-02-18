# 4x4 Tic Tac Toe AI (Minimax + Alpha-Beta Pruning)

A clean Python implementation of 4x4 Tic Tac Toe with a command-line UI and an AI opponent that uses pure minimax with alpha-beta pruning.

This README is viva-focused: it covers architecture, algorithm design, complexity, testing strategy, likely viva questions, and known implementation trade-offs.

---

## 1) Problem Statement

Build a 4x4 Tic Tac Toe game where:
- Board size is 4x4 (16 cells).
- Win condition is 4 same marks in a row, column, or diagonal.
- Human plays against an AI.
- AI chooses optimal moves using minimax with alpha-beta pruning.

Why 4x4 is interesting:
- State space is much larger than classic 3x3 Tic Tac Toe.
- Minimax remains correct but computationally heavier, making pruning important.

---

## 2) Key Features

- 4x4 board representation using an internal 1D list.
- Strict move validation and turn management.
- Win detection for rows, columns, and both diagonals.
- AI opponent with:
   - Minimax recursion
   - Alpha-beta pruning
   - Depth-sensitive scoring (faster wins, slower losses)
- CLI game loop with user input parsing and board rendering.
- Unit tests for board, engine, win logic, and AI decision behavior.
- Regression coverage for minimax API compatibility.

---

## 3) Tech Stack

- Python 3.x
- pytest for unit tests
- hypothesis listed in dependencies (available for property-based tests)

Dependencies are in requirements.txt:
- pytest>=7.4.0
- hypothesis>=6.82.0

---

## 4) Project Structure

.
├── main.py
├── requirements.txt
├── README.md
├── tictactoe/
│   ├── __init__.py
│   ├── board.py
│   ├── win_detection.py
│   ├── game_engine.py
│   ├── ai_opponent.py
│   └── user_interface.py
└── tests/
      ├── __init__.py
      ├── test_board.py
      ├── test_win_detection.py
      ├── test_game_engine.py
      └── test_ai_opponent.py

Module responsibilities:
- board.py: Data model for board state and low-level operations.
- win_detection.py: Pure functions to check wins.
- game_engine.py: Rules, turns, and game status transitions.
- ai_opponent.py: Minimax + alpha-beta decision making.
- user_interface.py: Console interaction and display.
- main.py: Entry point and exception-safe launch.

---

## 5) How to Run

### Setup

1. Create a virtual environment:
    python -m venv venv

2. Activate:
    - Windows: venv\Scripts\activate
    - Linux/Mac: source venv/bin/activate

3. Install requirements:
    pip install -r requirements.txt

### Start the game

python main.py

### CLI usage notes

- Human = X, AI = O.
- Enter move as: row col
- Valid row/col range: 0 to 3.
- Example input: 2 1

---

## 6) Core Design and Data Model

### Cell states

An enum defines:
- EMPTY = 0
- X = 1
- O = 2

### Board representation

- Internally, board uses a flat list of 16 elements.
- Mapping:
   - index = row * 4 + col
   - row = index // 4
   - col = index % 4

Benefits:
- Compact memory layout.
- Easy copy operation for minimax branching.

### Engine state

Game status enum:
- IN_PROGRESS
- X_WINS
- O_WINS
- DRAW

GameEngine guarantees:
- No move after terminal state.
- Turn alternates only after successful move.
- Status updates immediately after each accepted move.

---

## 7) AI Algorithm (Viva-Important)

### Minimax idea

The AI simulates all possible future games from a candidate move and assumes:
- AI plays optimally to maximize score.
- Opponent plays optimally to minimize score.

### Terminal evaluation

For a board state at recursion depth d:
- AI win: score = 10 - d
- Player win: score = d - 10
- Draw: score = 0

Why depth term matters:
- Earlier win gives larger positive score.
- Earlier loss gives more negative score.
- So AI prefers fast wins and delayed losses.

### Alpha-beta pruning

At each node:
- alpha = best guaranteed score so far for maximizing player.
- beta = best guaranteed score so far for minimizing player.

If beta <= alpha, further exploration of that branch is unnecessary and is pruned.

### Complexity discussion

Let b = branching factor (remaining empty cells), d = search depth.
- Plain minimax worst case: O(b^d)
- Space (recursion): O(d)
- Alpha-beta best-case pruning can reduce effective explored nodes significantly.

In 4x4, early game branching is high, so full-depth search from the initial position is expensive. Practical tests use near-terminal boards to keep execution fast and deterministic.

---

## 8) API Notes and Compatibility

Current minimax signature accepts explicit alpha/beta and also supports legacy calls:

minimax(board, depth, is_maximizing, alpha=-inf, beta=inf, max_depth=None)

Compatibility behavior:
- Legacy style minimax(board, depth, is_maximizing) remains valid.
- Explicit alpha/beta calls are supported for advanced control.

Regression protection:
- tests/test_ai_opponent.py includes a regression test that ensures legacy and explicit calls produce identical results on a deterministic terminal state.

---

## 9) Testing Strategy

Run all tests:

pytest -q

Current status at last verification:
- 55 passed

Test coverage by area:
- test_board.py:
   - initialization
   - set/get operations
   - bounds checks and invalid values
   - full-board detection
   - empty-cell listing
   - deep copy independence
- test_win_detection.py:
   - all row/column wins
   - both diagonal wins
   - non-winning patterns
   - combined check_win behavior
- test_game_engine.py:
   - game initialization
   - turn alternation
   - move rejection rules
   - win and draw status transitions
- test_ai_opponent.py:
   - AI initialization and mark assignment
   - immediate win selection
   - opponent threat blocking
   - win-vs-block prioritization
   - terminal scoring correctness
   - move validity on constrained boards
   - minimax API compatibility regression

---

## 10) Error Handling and Validation

Implemented safeguards:
- Invalid board indices raise ValueError.
- Attempt to set EMPTY mark raises ValueError.
- Invalid starting player raises ValueError.
- Invalid AI mark raises ValueError.
- Occupied cell move returns False (no overwrite).
- main.py catches KeyboardInterrupt for graceful exit.
- main.py catches unexpected exceptions and exits with error code.

---

## 11) Limitations and Future Extensions

Current limitations:
- CLI only (no GUI).
- No transposition table or memoization in minimax.
- No opening-book heuristics.
- Full-depth search on sparse 4x4 boards can be slow.

Reasonable future improvements:
- Add memoization (hash board states).
- Add iterative deepening with time budget.
- Add heuristic evaluation for depth-limited search.
- Add optional GUI (Tkinter/PyGame/Web).
- Add benchmarking script for node counts and pruning efficiency.

---

## 12) Quick Viva Q&A Cheat Sheet

Q: Why minimax here?
A: Tic Tac Toe is a deterministic, zero-sum, perfect-information game, so minimax gives optimal play under optimal opponent assumptions.

Q: Why alpha-beta pruning?
A: It preserves optimality while avoiding exploration of provably irrelevant branches, reducing practical compute cost.

Q: Why use depth in score?
A: To break ties among terminal outcomes by preferring faster wins and slower losses.

Q: How do you ensure game correctness?
A: Separation of concerns plus dedicated tests for board rules, win logic, state transitions, and AI decisions.

Q: Why store board as 1D list instead of 2D list?
A: Simpler contiguous storage, straightforward index math, and easy cloning for minimax branches.

Q: What ensures compatibility after API changes?
A: A regression test locks minimax legacy-call behavior to prevent accidental breaking changes.

---

## 13) License

Provided for educational and academic use.
