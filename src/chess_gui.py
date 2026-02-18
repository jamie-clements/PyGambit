import pygame
from src.chess_engine import ChessEngine

class ChessGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Chess Engine")
        self.clock = pygame.time.Clock()
        self.engine = ChessEngine()
        self.load_images()

    def load_images(self):
        piece_values = {1: 'wp', 2: 'wn', 3: 'wb', 4: 'wr', 5: 'wq', 6: 'wk',
                        -1: 'bp', -2: 'bn', -3: 'bb', -4: 'br', -5: 'bq', -6: 'bk'}
        self.images = {}
        for value, piece in piece_values.items():
            self.images[value] = pygame.image.load(f"assets/images/{piece}.png")
            self.images[value] = pygame.transform.scale(self.images[value], (100, 100))

    def draw_board(self):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, pygame.Rect(col*100, row*100, 100, 100))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.engine.board[row, col]
                if piece != 0:
                    self.screen.blit(self.images[piece], pygame.Rect(col*100, row*100, 100, 100))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_board()
            self.draw_pieces()
            
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()