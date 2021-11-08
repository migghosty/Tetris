import sys
import pygame
import random

BLOCK_TYPES = ['i', 'j', 'l', 'o', 's', 't', 'z']
WIDTH = 12
HEIGHT = 22
BORDER_COLOR = (81,87,97)

class Block:
    def __init__(self, block_type):
        self.block_type = block_type

    def get_image(self) -> pygame.Surface:
        if self.block_type == 'i':
            return pygame.image.load("imgs/i_block.png").convert()
        elif self.block_type == 'j':
            return pygame.image.load("imgs/j_block.png").convert()
        elif self.block_type == 'l':
            return pygame.image.load("imgs/l_block.png").convert()
        elif self.block_type == 'o':
            return pygame.image.load("imgs/o_block.png").convert()
        elif self.block_type == 's':
            return pygame.image.load("imgs/s_block.png").convert()
        elif self.block_type == 't':
            return pygame.image.load("imgs/t_block.png").convert()
        elif self.block_type == 'z':
            return pygame.image.load("imgs/z_block.png").convert()


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

    def _get_screen_width(self) -> int:
        return pygame.display.get_window_size()[0]

    def _get_screen_height(self) -> int:
        return pygame.display.get_window_size()[1]

    def _get_block_width(self) -> int:
        return self._get_screen_width()/WIDTH

    def _get_block_height(self) -> int:
        return self._get_screen_height()/HEIGHT

    def _get_block_size(self) -> (int,int):
        return (self._get_block_width(), self._get_block_height())

    def _draw_border_block(self, x: int, y: int, img_path) -> None:
        # draw a single block with a given color at a given (x,y) position
        # the (x,y) position is given should be based of the tetris board, not pixels.
        # for example, the block to the right of (0,0) is (1,0)
        img = pygame.image.load(img_path).convert()
        img = pygame.transform.scale(img, self._get_block_size())
        self._screen.blit(img, (self._get_block_width()*x,
                                self._get_block_height()*y))

    def draw_border(self) -> None:
        # draws the top and bottom row
        for i in range(WIDTH):
            self._draw_border_block(i, 0, "imgs/border_block.png")
            self._draw_border_block(i, HEIGHT - 1, "imgs/border_block.png")
        # draws the side columns
        for i in range(HEIGHT):
            self._draw_border_block(0, i, "imgs/border_block.png")
            self._draw_border_block(WIDTH-1, i, "imgs/border_block.png")

    def _get_random_block(self) -> Block:
        return Block(random.choice(BLOCK_TYPES))

    def _draw_block(self, block: Block, x: int, y: int) -> None:
        img = block.get_image()
        img = pygame.transform.scale(img, self._get_block_size())
        self._screen.blit(img, (self._get_block_width()*x,
                                self._get_block_height()*y))

    def spawn_random_block(self):
        # spawn a random block at the top row, middle column
        block = self._get_random_block()
        self._draw_block(block, WIDTH/2, 2)

    def handle_keys(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        self.handle_keys()

    def run(self):
        self.spawn_random_block()
        while True:
            self.draw_border()
            self.handle_events()
            pygame.display.flip()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()

