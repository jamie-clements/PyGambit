import pygame
from src.chess_engine import ChessEngine

SQUARE = 100
SIZE   = SQUARE * 8

# Board colours (Lichess-style)
LIGHT     = (240, 217, 181)
DARK      = (181, 136,  99)

# Highlight overlays (RGBA)
SELECTED  = (205, 210, 106, 160)
MOVE_DOT  = (106, 135,  75, 160)
MOVE_RING = (106, 135,  75, 180)
CHECK_RED = (220,  50,  50, 120)

# Menu colours
BG_DARK   = ( 30,  30,  30)
BTN_IDLE  = ( 70,  70,  70)
BTN_HOVER = (100, 100, 100)
BTN_TEXT  = (255, 255, 255)

DIFFICULTIES = {
    'Easy':   1,   # depth 1 – looks 1 move ahead
    'Medium': 2,   # depth 2 – looks 2 moves ahead
    'Hard':   3,   # depth 3 – looks 3 moves ahead
}


class ChessGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption("PyGambit")
        self.clock  = pygame.time.Clock()
        self.load_images()
        self.show_menu()

    # ------------------------------------------------------------------ setup

    def load_images(self):
        names = {1:'wp', 2:'wn', 3:'wb', 4:'wr', 5:'wq', 6:'wk',
                -1:'bp',-2:'bn',-3:'bb',-4:'br',-5:'bq',-6:'bk'}
        self.images = {}
        for v, name in names.items():
            img = pygame.image.load(f"assets/images/{name}.png")
            self.images[v] = pygame.transform.scale(img, (SQUARE, SQUARE))

    def show_menu(self):
        """Reset all game state and enter the difficulty-selection screen."""
        self.state       = 'menu'
        self.engine      = None
        self.ai_depth    = 2
        self.selected    = None
        self.legal_moves = []
        self.turn        = 'white'
        self.game_over   = False
        self.status      = ""

    def start_game(self, depth):
        self.ai_depth    = depth
        self.engine      = ChessEngine()
        self.selected    = None
        self.legal_moves = []
        self.turn        = 'white'
        self.game_over   = False
        self.status      = ""
        self.state       = 'game'

    # ------------------------------------------------------------------ coord helpers

    def to_screen(self, col, row):
        """Numpy (col, row) → screen pixel.  White is at the bottom."""
        return col * SQUARE, (7 - row) * SQUARE

    def to_board(self, sx, sy):
        """Screen pixel → numpy (col, row)."""
        return sx // SQUARE, 7 - sy // SQUARE

    # ------------------------------------------------------------------ menu drawing

    def draw_menu(self):
        self.screen.fill(BG_DARK)

        title_font = pygame.font.SysFont("Arial", 52, bold=True)
        sub_font   = pygame.font.SysFont("Arial", 22)
        btn_font   = pygame.font.SysFont("Arial", 28, bold=True)

        # Title
        title = title_font.render("PyGambit", True, BTN_TEXT)
        self.screen.blit(title, (SIZE//2 - title.get_width()//2, 140))

        # Subtitle
        sub = sub_font.render("Select difficulty to start", True, (180, 180, 180))
        self.screen.blit(sub, (SIZE//2 - sub.get_width()//2, 210))

        # Buttons
        btn_w, btn_h = 260, 60
        gap          = 24
        labels       = list(DIFFICULTIES.keys())
        total_h      = len(labels) * btn_h + (len(labels)-1) * gap
        start_y      = SIZE//2 - total_h//2 + 20

        mx, my = pygame.mouse.get_pos()
        self._menu_buttons = {}   # label → rect (used by click handler)

        for i, label in enumerate(labels):
            bx = SIZE//2 - btn_w//2
            by = start_y + i * (btn_h + gap)
            rect = pygame.Rect(bx, by, btn_w, btn_h)
            self._menu_buttons[label] = rect

            colour = BTN_HOVER if rect.collidepoint(mx, my) else BTN_IDLE
            pygame.draw.rect(self.screen, colour, rect, border_radius=10)

            depth = DIFFICULTIES[label]
            text  = btn_font.render(f"{label}  (depth {depth})", True, BTN_TEXT)
            self.screen.blit(text, (bx + btn_w//2 - text.get_width()//2,
                                    by + btn_h//2 - text.get_height()//2))

        # Small hint at bottom
        hint = sub_font.render("Press Esc during a game to return here", True, (120, 120, 120))
        self.screen.blit(hint, (SIZE//2 - hint.get_width()//2, SIZE - 50))

    def handle_menu_click(self, sx, sy):
        for label, rect in self._menu_buttons.items():
            if rect.collidepoint(sx, sy):
                self.start_game(DIFFICULTIES[label])
                return

    # ------------------------------------------------------------------ game drawing

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                colour = LIGHT if (row + col) % 2 == 0 else DARK
                sx, sy = self.to_screen(col, row)
                pygame.draw.rect(self.screen, colour, (sx, sy, SQUARE, SQUARE))

    def draw_highlights(self):
        # King in check
        if self.engine.is_in_check(self.turn):
            king_val = 6 if self.turn == 'white' else -6
            for r in range(8):
                for c in range(8):
                    if self.engine.board[r, c] == king_val:
                        self._fill_square(c, r, CHECK_RED)

        # Selected square
        if self.selected is not None:
            self._fill_square(*self.selected, SELECTED)

        # Legal move indicators
        for mx, my in self.legal_moves:
            c = ord(mx) - ord('a')
            r = my - 1
            sx, sy = self.to_screen(c, r)
            surf = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
            if self.engine.board[r, c] != 0:          # capture → ring
                pygame.draw.rect(surf, MOVE_RING, (0, 0, SQUARE, SQUARE), 8)
            else:                                      # empty → dot
                pygame.draw.circle(surf, MOVE_DOT, (SQUARE//2, SQUARE//2), 18)
            self.screen.blit(surf, (sx, sy))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.engine.board[row, col]
                if piece != 0:
                    sx, sy = self.to_screen(col, row)
                    self.screen.blit(self.images[piece], (sx, sy))

    def draw_status(self):
        if not self.status:
            return
        font = pygame.font.SysFont("Arial", 38, bold=True)
        text = font.render(self.status, True, (255, 255, 255))
        pad  = 18
        w    = text.get_width() + pad * 2
        h    = text.get_height() + pad
        bg   = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 190))
        bx, by = SIZE//2 - w//2, SIZE//2 - h//2
        self.screen.blit(bg, (bx, by))
        self.screen.blit(text, (bx + pad, by + pad//2))

        # Prompt to return to menu
        hint_font = pygame.font.SysFont("Arial", 20)
        hint = hint_font.render("Press Esc to play again", True, (200, 200, 200))
        self.screen.blit(hint, (SIZE//2 - hint.get_width()//2, by + h + 8))

    def _fill_square(self, col, row, rgba):
        surf = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
        surf.fill(rgba)
        self.screen.blit(surf, self.to_screen(col, row))

    # ------------------------------------------------------------------ game logic

    def handle_game_click(self, sx, sy):
        if self.game_over or self.turn != 'white':
            return
        col, row = self.to_board(sx, sy)
        if not (0 <= col < 8 and 0 <= row < 8):
            return

        piece = self.engine.board[row, col]
        x, y  = chr(ord('a') + col), row + 1

        if self.selected is not None:
            sc, sr = self.selected
            from_x = chr(ord('a') + sc)
            from_y = sr + 1

            if (x, y) in self.legal_moves:
                self.engine.make_move(from_x, from_y, x, y)
                self.selected, self.legal_moves = None, []
                if not self.check_game_over('black'):
                    self.turn = 'black'
                    pygame.time.set_timer(pygame.USEREVENT, 150)
                return

            if piece > 0:                            # re-select own piece
                self.selected    = (col, row)
                self.legal_moves = self.engine.get_legal_moves(x, y)
                return

            self.selected, self.legal_moves = None, []  # deselect
            return

        if piece > 0:
            self.selected    = (col, row)
            self.legal_moves = self.engine.get_legal_moves(x, y)

    def ai_move(self):
        move = self.engine.choose_best_move('black', self.ai_depth)
        if move:
            self.engine.make_move(*move)
        if not self.check_game_over('white'):
            self.turn = 'white'

    def check_game_over(self, color):
        if self.engine.is_checkmate(color):
            winner = 'Black' if color == 'white' else 'White'
            self.status    = f"Checkmate — {winner} wins!"
            self.game_over = True
            return True
        if len(self.engine.get_all_moves(color)) == 0:
            self.status    = "Stalemate!"
            self.game_over = True
            return True
        return False

    # ------------------------------------------------------------------ main loop

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.time.set_timer(pygame.USEREVENT, 0)
                        self.show_menu()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.state == 'menu':
                        self.handle_menu_click(*event.pos)
                    else:
                        self.handle_game_click(*event.pos)

                elif event.type == pygame.USEREVENT:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    self.ai_move()

            if self.state == 'menu':
                self.draw_menu()
            else:
                self.draw_board()
                self.draw_highlights()
                self.draw_pieces()
                self.draw_status()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()
