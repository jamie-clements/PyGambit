# PyGambit

A chess game written in Python with a fully interactive Pygame GUI and an AI opponent powered by the Minimax algorithm with alpha-beta pruning.

---

## Features

- **Complete chess rules** — legal move generation for all pieces, castling, en passant, and pawn promotion (auto-queens)
- **Check & checkmate detection** — illegal moves that expose your own king are filtered out; checkmate and stalemate are detected and announced
- **Three AI difficulty levels** — Easy, Medium, and Hard, selectable from the start menu
- **Click-to-move GUI** — click a piece to see its legal moves highlighted, then click a destination to move
- **Visual feedback** — selected square highlighted in yellow-green, legal moves shown as dots (empty squares) or rings (captures), king in check shown in red

---

## How to Play

### 1. Install dependencies

```bash
pip install pygame numpy
```

Requires **Python 3.7+**.

### 2. Clone the repository

```bash
git clone https://github.com/yourusername/pygambit.git
cd pygambit
```

### 3. Run the game

```bash
python3 -m src.chess_gui
```

> Always run from the project root directory so the `src/` import path resolves correctly.

### 4. Playing

1. The **difficulty menu** appears first — choose Easy, Medium, or Hard
2. **You play as White** (bottom). Click any white piece to select it
3. **Green dots** show where that piece can legally move — click one to move
4. **The AI** (Black) responds automatically after your move
5. Press **Esc** at any time to return to the difficulty menu and start a new game

---

## How the AI Works

The AI uses **Minimax with alpha-beta pruning**, a standard algorithm in game-playing programs.

### Minimax

Minimax models the game as a tree of future positions. At each node the algorithm alternates between two players:

- **Maximising player (White)** — picks the move that leads to the highest evaluation score
- **Minimising player (Black)** — picks the move that leads to the lowest evaluation score

The algorithm looks ahead a fixed number of moves (the *search depth*), then evaluates the resulting board position using a static evaluation function:

```
score = Σ (piece values) + central control bonus
```

Piece values used: Pawn = 100, Knight = 320, Bishop = 330, Rook = 500, Queen = 900, King = 20 000. White pieces add to the score; black pieces subtract.

### Alpha-Beta Pruning

Alpha-beta pruning dramatically reduces the number of nodes searched without changing the result. It maintains two bounds:

- **α (alpha)** — the best score the maximising player is guaranteed so far
- **β (beta)** — the best score the minimising player is guaranteed so far

When a branch is found that cannot possibly influence the final result (β ≤ α), it is cut off immediately. In practice this can halve the effective search depth for the same computation time.

### Difficulty Levels

| Level  | Search depth | Looks ahead        |
|--------|--------------|--------------------|
| Easy   | 1            | 1 half-move        |
| Medium | 2            | 1 full move        |
| Hard   | 3            | 1.5 full moves     |

Depth 3 can take a few seconds per move as it evaluates tens of thousands of positions.

---

## Project Structure

```
PyGambit/
├── src/
│   ├── chess_engine.py   # Move generation, rules, AI
│   └── chess_gui.py      # Pygame interface
├── tests/
│   └── test_chess_engine.py
├── assets/
│   └── images/           # Piece PNGs
├── requirements.txt
└── README.md
```

---

## Running the Engine Tests

```bash
python3 -m tests.test_chess_engine
```

---

## Contributing

Contributions are welcome. Fork the repository, make your changes, and open a pull request. Please follow Python best practices and keep changes focused.

## License

MIT — see [LICENSE](LICENSE) for details.
