# test_chess_engine.py

from src.chess_engine import ChessEngine

def test_initial_board():
    engine = ChessEngine()
    print("Initial board:")
    engine.print_board()

def test_pawn_moves():
    engine = ChessEngine()
    print("\nPossible moves for white pawn at e2:")
    print(engine.get_moves('e', 2))
    print("\nPossible moves for black pawn at e7:")
    print(engine.get_moves('e', 7))

def test_knight_moves():
    engine = ChessEngine()
    print("\nPossible moves for white knight at b1:")
    print(engine.get_moves('b', 1))

def test_bishop_moves():
    engine = ChessEngine()
    # Clear some spaces for the bishop
    engine.board[1, 3] = 0  # Remove pawn at d2
    print("\nPossible moves for white bishop at c1:")
    print(engine.get_moves('c', 1))

def test_rook_moves():
    engine = ChessEngine()
    # Clear some spaces for the rook
    engine.board[1, 0] = 0  # Remove pawn at a2
    print("\nPossible moves for white rook at a1:")
    print(engine.get_moves('a', 1))

def test_queen_moves():
    engine = ChessEngine()
    # Clear some spaces for the queen
    engine.board[1, 3] = 0  # Remove pawn at d2
    print("\nPossible moves for white queen at d1:")
    print(engine.get_moves('d', 1))

def test_king_moves():
    engine = ChessEngine()
    print("\nPossible moves for white king at e1:")
    print(engine.get_moves('e', 1))

def test_castling():
    engine = ChessEngine()
    print("\nPossible moves for white king at e1 (should include castling):")
    print(engine.get_moves('e', 1))

    # Clear the path for castling
    engine.board[0, 5] = 0  # Remove bishop at f1
    engine.board[0, 6] = 0  # Remove knight at g1

    print("\nPossible moves for white king at e1 (should now include kingside castling):")
    print(engine.get_moves('e', 1))

    # Make the castling move
    engine.make_move('e', 1, 'g', 1)
    print("\nBoard after white kingside castle:")
    engine.print_board()

def test_en_passant():
    engine = ChessEngine()
    # Set up an en passant situation
    engine.board[4, 4] = 1  # White pawn at e5
    engine.board[6, 3] = -1  # Black pawn at d7
    engine.board[4, 3] = -1  # Black pawn at d5 (just moved)
    engine.en_passant_target = ('d', 6)
    
    print("\nBoard before en passant:")
    engine.print_board()
    
    print("\nPossible moves for white pawn at e5 (should include en passant):")
    print(engine.get_moves('e', 5))
    
    # Make the en passant move
    engine.make_move('e', 5, 'd', 6)
    
    print("\nBoard after en passant capture:")
    engine.print_board()

def test_pawn_promotion():
    engine = ChessEngine()
    # Set up a pawn promotion situation
    engine.board[6, 4] = 1  # White pawn at e7
    engine.board[7, :] = 0  # Clear the back rank
    
    print("\nBoard before pawn promotion:")
    engine.print_board()
    
    # Make the promotion move
    engine.make_move('e', 7, 'e', 8)
    
    print("\nBoard after pawn promotion (should be a queen):")
    engine.print_board()

def test_checkmate():
    engine = ChessEngine()
    # Set up a checkmate situation (fool's mate)
    engine.make_move('f', 2, 'f', 3)
    engine.make_move('e', 7, 'e', 5)
    engine.make_move('g', 2, 'g', 4)
    engine.make_move('d', 8, 'h', 4)
    
    print("\nBoard in checkmate position:")
    engine.print_board()
    
    print("\nIs white in checkmate?", engine.is_checkmate('white'))
    print("Is black in checkmate?", engine.is_checkmate('black'))

def test_ai_move():
    engine = ChessEngine()
    print("\nInitial board:")
    engine.print_board()
    
    best_move = engine.choose_best_move('white', 3)  # Depth 3
    print("\nBest move for white:", best_move)
    
    engine.make_move(*best_move)
    print("\nBoard after AI move:")
    engine.print_board()

def run_all_tests():
#    test_initial_board()
#    test_pawn_moves()
#    test_knight_moves()
#    test_bishop_moves()
#    test_rook_moves()
#    test_queen_moves()
#    test_king_moves()
#    test_castling()

    test_en_passant()
    test_pawn_promotion()
    test_checkmate()
    test_ai_move()

if __name__ == "__main__":
    run_all_tests()