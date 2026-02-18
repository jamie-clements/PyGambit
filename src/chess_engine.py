import numpy as np

# python -m venv venv
# source venv/bin/activate

class ChessEngine:
    def __init__(self):
        self.board = self.initalize_board()
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rooks_moved = [False, False]  # [queenside, kingside]
        self.black_rooks_moved = [False, False]  # [queenside, kingside]
        self.move_history = []
        self.en_passant_target = None

    def initalize_board(self):
        # Initalize 8x8 chess board
        # 0 represents empty squares
        # Positive numbers for white pieces, negative for black
        # 1: Pawn, 2: Knight, 3: Bishop, 4: Rook, 5: Queen, 6:King
        board = np.zeros((8,8), dtype=int)

        # Set up pawns
        board[1, :] = 1 # White pawns
        board[6, :] = -1 # Black pawns

        # Set up other pieces
        pieces = [4, 2, 3, 5, 6, 3, 2, 4]
        board[0, :] = pieces # White pieces
        board[7, :] = [-p for p in pieces] # Black pieces 

        return board
    
    def print_board(self):
        # Display current board state
        piece_symbols = {
            0: '.',
            1: '♙', -1: '♟',
            2: '♘', -2: '♞',
            3: '♗', -3: '♝',
            4: '♖', -4: '♜',
            5: '♕', -5: '♛',
            6: '♔', -6: '♚'
        }
        print('  a b c d e f g h')
        for y in range(7, -1, -1):
            print(f"{y+1} {' '.join(piece_symbols[self.board[y, x]] for x in range(8))} {y+1}")
        print('  a b c d e f g h')

    def is_valid_position(self, x, y):
        return 'a' <= x <= 'h' and 1 <= y <= 8

    def get_pawn_moves(self, x, y, color):
        moves = []
        x_idx = ord(x) - ord('a')
        y_idx = y - 1
        direction = 1 if color == 'white' else -1
        
        # Move forward
        if self.is_valid_position(x, y + direction) and self.board[y_idx + direction, x_idx] == 0:
            moves.append((x, y + direction))
            
            # Double move from starting position
            if (color == 'white' and y == 2) or (color == 'black' and y == 7):
                if self.board[y_idx + 2*direction, x_idx] == 0:
                    moves.append((x, y + 2*direction))
        
        # Capture diagonally
        for dx in [-1, 1]:
            new_x = chr(ord(x) + dx)
            if self.is_valid_position(new_x, y + direction):
                if color == 'white' and self.board[y_idx + direction, x_idx + dx] < 0:
                    moves.append((new_x, y + direction))
                elif color == 'black' and self.board[y_idx + direction, x_idx + dx] > 0:
                    moves.append((new_x, y + direction))

        # En passant
        if self.en_passant_target:
            en_passant_x, en_passant_y = self.en_passant_target
            if abs(ord(x) - ord(en_passant_x)) == 1 and ((color == 'white' and y == 5) or (color == 'black' and y == 4)):
                moves.append((en_passant_x, en_passant_y + (1 if color == 'white' else -1)))

        return moves
    
    def get_knight_moves(self, x, y):
        moves = []
        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        for dx, dy in knight_moves:
            new_x = chr(ord(x) + dx)
            new_y = y + dy
            if self.is_valid_position(new_x, new_y):
                x_idx, y_idx = ord(new_x) - ord('a'), new_y - 1
                if self.board[y_idx, x_idx] * self.board[y - 1, ord(x) - ord('a')] <= 0:  # Empty or opponent's piece
                    moves.append((new_x, new_y))
        return moves

    def get_bishop_moves(self, x, y):
        return self.get_diagonal_moves(x, y)

    def get_rook_moves(self, x, y):
        return self.get_straight_moves(x, y)

    def get_queen_moves(self, x, y):
        return self.get_diagonal_moves(x, y) + self.get_straight_moves(x, y)

    def get_diagonal_moves(self, x, y):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_x = chr(ord(x) + i*dx)
                new_y = y + i*dy
                if not self.is_valid_position(new_x, new_y):
                    break
                x_idx, y_idx = ord(new_x) - ord('a'), new_y - 1
                if self.board[y_idx, x_idx] == 0:
                    moves.append((new_x, new_y))
                elif self.board[y_idx, x_idx] * self.board[y - 1, ord(x) - ord('a')] < 0:  # Opponent's piece
                    moves.append((new_x, new_y))
                    break
                else:
                    break
        return moves

    def get_straight_moves(self, x, y):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for i in range(1, 8):
                new_x = chr(ord(x) + i*dx)
                new_y = y + i*dy
                if not self.is_valid_position(new_x, new_y):
                    break
                x_idx, y_idx = ord(new_x) - ord('a'), new_y - 1
                if self.board[y_idx, x_idx] == 0:
                    moves.append((new_x, new_y))
                elif self.board[y_idx, x_idx] * self.board[y - 1, ord(x) - ord('a')] < 0:  # Opponent's piece
                    moves.append((new_x, new_y))
                    break
                else:
                    break
        return moves

    def get_basic_king_moves(self, x, y):
        moves = []
        king_moves = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]
        for dx, dy in king_moves:
            new_x = chr(ord(x) + dx)
            new_y = y + dy
            if self.is_valid_position(new_x, new_y):
                x_idx, y_idx = ord(new_x) - ord('a'), new_y - 1
                if self.board[y_idx, x_idx] * self.board[y - 1, ord(x) - ord('a')] <= 0:  # Empty or opponent's piece
                    moves.append((new_x, new_y))
        return moves
    
    def is_square_attacked(self, x, y, attacking_color):
        for i in range(8):
            for j in range(8):
                piece = self.board[i, j]
                if (piece > 0 and attacking_color == 'black') or (piece < 0 and attacking_color == 'white'):
                    moves = self.get_basic_moves(chr(ord('a') + j), i + 1)
                    if (x, y) in moves:
                        return True
        return False
    
    def can_castle(self, color, side):
        y = 1 if color == 'white' else 8
        king_x = 'e'
        
        # Check if king or rook has moved
        if color == 'white':
            if self.white_king_moved or self.white_rooks_moved[0 if side == 'queenside' else 1]:
                return False
        else:
            if self.black_king_moved or self.black_rooks_moved[0 if side == 'queenside' else 1]:
                return False

        # Check if squares between king and rook are empty
        if side == 'queenside':
            empty_squares = ['d', 'c', 'b']
            rook_x = 'a'
        else:  # kingside
            empty_squares = ['f', 'g']
            rook_x = 'h'

        for x in empty_squares:
            if self.board[y-1, ord(x)-ord('a')] != 0:
                return False

        # Check if king is in check or passes through attacked squares
        enemy_color = 'black' if color == 'white' else 'white'
        check_squares = [king_x] + empty_squares[:2]  # King's current square and the two it passes through
        for x in check_squares:
            if self.is_square_attacked(x, y, enemy_color):
                return False

        return True
    
    def get_basic_moves(self, x, y):
        x_idx = ord(x) - ord('a')
        y_idx = y - 1
        piece = self.board[y_idx, x_idx]
        color = 'white' if piece > 0 else 'black'
        
        if abs(piece) == 1:  # Pawn
            return self.get_pawn_moves(x, y, color)
        elif abs(piece) == 2:  # Knight
            return self.get_knight_moves(x, y)
        elif abs(piece) == 3:  # Bishop
            return self.get_bishop_moves(x, y)
        elif abs(piece) == 4:  # Rook
            return self.get_rook_moves(x, y)
        elif abs(piece) == 5:  # Queen
            return self.get_queen_moves(x, y)
        elif abs(piece) == 6:  # King
            return self.get_basic_king_moves(x, y)
        else:
            return []
        
    def get_moves(self, x, y):
        moves = self.get_basic_moves(x, y)
        if abs(self.board[y-1, ord(x)-ord('a')]) == 6:  # If it's a king
            color = 'white' if self.board[y-1, ord(x)-ord('a')] > 0 else 'black'
            # Check castling
            if self.can_castle(color, 'kingside'):
                moves.append(('g', y))
            if self.can_castle(color, 'queenside'):
                moves.append(('c', y))
        return moves

    def make_move(self, from_x, from_y, to_x, to_y):
        # Capture the piece at the destination (if any)
        captured_piece = self.board[to_y-1, ord(to_x)-ord('a')]
        
        # Move the piece
        piece = self.board[from_y-1, ord(from_x)-ord('a')]
        color = 'white' if piece > 0 else 'black'
        
        # Record the move in history (include en passant info)
        self.move_history.append((from_x, from_y, to_x, to_y, captured_piece, self.en_passant_target))
        
        self.board[to_y-1, ord(to_x)-ord('a')] = piece
        self.board[from_y-1, ord(from_x)-ord('a')] = 0

        # Update king and rook move flags
        if abs(piece) == 6:  # King
            if piece > 0:
                self.white_king_moved = True
            else:
                self.black_king_moved = True

            # Handle castling
            if abs(ord(to_x) - ord(from_x)) == 2:
                if to_x == 'g':  # Kingside
                    rook_from, rook_to = ('h', 'f')
                else:  # Queenside
                    rook_from, rook_to = ('a', 'd')
                self.make_move(rook_from, from_y, rook_to, to_y)

        elif abs(piece) == 4:  # Rook
            if from_x == 'a':  # Queenside
                if piece > 0:
                    self.white_rooks_moved[0] = True
                else:
                    self.black_rooks_moved[0] = True
            elif from_x == 'h':  # Kingside
                if piece > 0:
                    self.white_rooks_moved[1] = True
                else:
                    self.black_rooks_moved[1] = True

        # Handle pawn promotion
        if abs(piece) == 1 and (to_y == 8 or to_y == 1):
            self.board[to_y-1, ord(to_x)-ord('a')] = 5 if piece > 0 else -5  # Promote to queen

        # Handle en passant
        if abs(piece) == 1 and abs(from_y - to_y) == 2:
            self.en_passant_target = (to_x, (from_y + to_y) // 2)
        elif abs(piece) == 1 and to_x != from_x and captured_piece == 0:
            # En passant capture
            captured_pawn_y = to_y - 1 if color == 'white' else to_y + 1
            self.board[captured_pawn_y-1, ord(to_x)-ord('a')] = 0
        else:
            self.en_passant_target = None

        # Clear en passant target after any non-pawn move or non-double-step pawn move
        if abs(piece) != 1 or abs(from_y - to_y) != 2:
            self.en_passant_target = None

    
    def evaluate_board(self):
        # Function to evaluate board state.
        # To be used by minmax algo to assess pos.
        if self.is_checkmate('white'):
            return -float('int')
        if self.is_checkmate('black'):
            return float('int')
        
        value = 0
        piece_values = {1: 100, 2: 320, 3: 330, 4: 500, 5: 900, 6: 20000}
        
        for y in range(8):
            for x in range(8):
                piece = self.board[y, x]
                if piece != 0:
                    # Add or subtract piece value
                    value += piece_values[abs(piece)] * (1 if piece > 0 else -1)
                    
                    # Bonus for central control (simplified)
                    if 2 <= x <= 5 and 2 <= y <= 5:
                        value += 10 * (1 if piece > 0 else -1)
        
        return value
    
    def is_checkmate(self, color):
        # First, check if the king is in check
        if not self.is_in_check(color):
            return False
        
        # If in check, see if there are any legal moves that get out of check
        for y in range(8):
            for x in range(8):
                piece = self.board[y, x]
                if (piece > 0 and color == 'white') or (piece < 0 and color == 'black'):
                    moves = self.get_moves(chr(ord('a') + x), y + 1)
                    for move in moves:
                        # Make the move
                        captured_piece = self.board[move[1]-1, ord(move[0])-ord('a')]
                        self.make_move(chr(ord('a') + x), y + 1, move[0], move[1])
                        
                        # Check if still in check
                        still_in_check = self.is_in_check(color)
                        
                        # Undo the move
                        self.undo_move()
                        
                        # If this move gets out of check, it's not checkmate
                        if not still_in_check:
                            return False
    
        # If we've checked all moves and none get out of check, it's checkmate
        return True

    def is_in_check(self, color):
        # Find the king
        king_pos = None
        king_value = 6 if color == 'white' else -6
        for y in range(8):
            for x in range(8):
                if self.board[y, x] == king_value:
                    king_pos = (x, y)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False  # This shouldn't happen in a valid game state
        
        # Check if any opponent's piece can attack the king
        opponent_color = 'black' if color == 'white' else 'white'
        for y in range(8):
            for x in range(8):
                piece = self.board[y, x]
                if (piece < 0 and opponent_color == 'black') or (piece > 0 and opponent_color == 'white'):
                    moves = self.get_moves(chr(ord('a') + x), y + 1)
                    if (chr(ord('a') + king_pos[0]), king_pos[1] + 1) in moves:
                        return True
        
        return False
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_board()
        
        if maximizing_player:
            max_eval = -float('inf')
            for move in self.get_all_moves('white'):
                self.make_move(*move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move()  # You'll need to implement this
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_all_moves('black'):
                self.make_move(*move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move()  # You'll need to implement this
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_all_moves(self, color):
        moves = []
        for y in range(8):
            for x in range(8):
                piece = self.board[y, x]
                if (piece > 0 and color == 'white') or (piece < 0 and color == 'black'):
                    for move in self.get_moves(chr(ord('a') + x), y + 1):
                        moves.append((chr(ord('a') + x), y + 1, move[0], move[1]))
        return moves

    def choose_best_move(self, color, depth):
        best_move = None
        best_eval = -float('inf') if color == 'white' else float('inf')
        
        for move in self.get_all_moves(color):
            self.make_move(*move)
            eval = self.minimax(depth - 1, -float('inf'), float('inf'), color == 'black')
            self.undo_move()  # You'll need to implement this
            
            if color == 'white' and eval > best_eval:
                best_eval = eval
                best_move = move
            elif color == 'black' and eval < best_eval:
                best_eval = eval
                best_move = move
        
        return best_move
    
    def undo_move(self):
        if not self.move_history:
            return
        last_move = self.move_history.pop()
        from_x, from_y, to_x, to_y, captured_piece, old_en_passant_target = last_move
        
        # Restore the moved piece
        self.board[from_y-1, ord(from_x)-ord('a')] = self.board[to_y-1, ord(to_x)-ord('a')]
        # Restore the captured piece (if any)
        self.board[to_y-1, ord(to_x)-ord('a')] = captured_piece
        
        # Restore the old en passant target
        self.en_passant_target = old_en_passant_target

        # Undo castling if it was a castling move
        if abs(self.board[from_y-1, ord(from_x)-ord('a')]) == 6 and abs(ord(to_x) - ord(from_x)) == 2:
            if to_x == 'g':  # Kingside
                self.undo_move()  # Undo rook move
            elif to_x == 'c':  # Queenside
                self.undo_move()  # Undo rook move

        # Reset king and rook move flags if necessary
        if abs(self.board[from_y-1, ord(from_x)-ord('a')]) == 6:  # King
            if self.board[from_y-1, ord(from_x)-ord('a')] > 0:
                self.white_king_moved = False
            else:
                self.black_king_moved = False
        elif abs(self.board[from_y-1, ord(from_x)-ord('a')]) == 4:  # Rook
            if from_x == 'a':  # Queenside
                if self.board[from_y-1, ord(from_x)-ord('a')] > 0:
                    self.white_rooks_moved[0] = False
                else:
                    self.black_rooks_moved[0] = False
            elif from_x == 'h':  # Kingside
                if self.board[from_y-1, ord(from_x)-ord('a')] > 0:
                    self.white_rooks_moved[1] = False
                else:
                    self.black_rooks_moved[1] = False

        # Undo en passant capture
        if abs(self.board[from_y-1, ord(from_x)-ord('a')]) == 1 and to_x != from_x and captured_piece == 0:
            captured_pawn_y = from_y if self.board[from_y-1, ord(from_x)-ord('a')] > 0 else from_y - 2
            self.board[captured_pawn_y-1, ord(to_x)-ord('a')] = -1 if self.board[from_y-1, ord(from_x)-ord('a')] > 0 else 1

        # Undo pawn promotion
        if abs(self.board[from_y-1, ord(from_x)-ord('a')]) == 5 and abs(captured_piece) == 1:
            self.board[from_y-1, ord(from_x)-ord('a')] = captured_piece