import sys
import pygame

BLOCK_TYPES = ['i', 'j', 'l', 'o', 's', 't', 'z']
BLOCK_WIDTH = 12
BLOCK_HEIGHT = 22
BORDER_COLOR = (81,87,97)

class Blocks:
    def __init__(self):
        block_type = None

    def draw_block(self):
        if block_type == 'i':
            pass
        elif block_type == 'j':
            pass
        elif block_type == 'l':
            pass
        elif block_type == 'o':
            pass
        elif block_type == 's':
            pass
        elif block_type == 't':
            pass
        elif block_type == 'z':
            pass

class TetrisGame:
    def __init__(self):
        # initialize pygame modules
        pygame.init()

        # define screen size
        self._screen_width = 500
        self._screen_height = 750
        self._screen = pygame.display.set_mode([self._screen_width, self._screen_height], pygame.RESIZABLE)

        # set caption and icon for screen
        pygame.display.set_caption("Tetris Game")
        tetrisIcon = pygame.image.load("imgs/tetris_logo.png")
        pygame.display.set_icon(tetrisIcon)

    def _get_screen_width(self):
        return pygame.display.get_window_size()[0]

    def _get_screen_height(self):
        return pygame.display.get_window_size()[1]

    def _draw_block(self, x: int, y: int, img_path):
        # draw a single block with a given color at a given (x,y) position
        # the (x,y) position is given should be based of the tetris board, not pixels.
        # for example, the block to the right of (0,0) is (1,0)
        img = pygame.image.load(img_path).convert()
        img = pygame.transform.scale(img, (self._get_screen_width()/BLOCK_WIDTH,
                                           self._get_screen_height()/BLOCK_HEIGHT))
        self._screen.blit(img, (self._get_screen_width()/BLOCK_WIDTH*x,
                                self._get_screen_height()/BLOCK_HEIGHT*y))

    def draw_border(self):
        # draws the top and bottom row
        for i in range(BLOCK_WIDTH):
            self._draw_block(i, 0, "imgs/border_block.png")
            self._draw_block(i, BLOCK_HEIGHT - 1, "imgs/border_block.png")
        # draws the side columns
        for i in range(BLOCK_HEIGHT):
            self._draw_block(0, i, "imgs/border_block.png")
            self._draw_block(BLOCK_WIDTH-1, i, "imgs/border_block.png")

    def handle_keys(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        self.handle_keys()

    def run(self):
        while True:
            self.draw_border()
            self.handle_events()
            pygame.display.flip()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()

