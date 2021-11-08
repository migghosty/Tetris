import sys
import pygame
import random
import const

BLOCK_TYPES = ['i', 'j', 'l', 'o', 's', 't', 'z']


class TetrisGame:
    def __init__(self):
        self._initialize_pygame()

        # make the custom settings
        self._custom_settings()

        # make the grid
        self._grid = [[0 for _ in range(const.BOARD_WIDTH)] for _ in range(const.BOARD_HEIGHT)]

    def _initialize_pygame(self):
        # initialize pygame modules
        pygame.init()

        # define screen size
        self._screen = pygame.display.set_mode([const.SCREEN_WIDTH, const.SCREEN_HEIGHT])

    def _custom_settings(self):
        # set caption and icon, and title for screen
        pygame.display.set_caption("Tetris Game")
        tetrisIcon = pygame.image.load("imgs/tetris_logo.png")
        pygame.display.set_icon(tetrisIcon)

        img = pygame.image.load("imgs/tetris_title.png").convert()
        img = pygame.transform.scale(img, (200, 60))

        self._screen.blit(img, (50, 50))

    def _convert_board_coordinate(self, x: int, y: int) -> (int, int):
        return ( x*const.BLOCK_SIZE + const.TOP_LEFT[0], y*const.BLOCK_SIZE + const.TOP_LEFT[1] )

    def _draw_border_block(self, x: int, y: int) -> None:
        # draw a single block with a given color at a given (x,y) position
        # the (x,y) position is given should be based of the tetris board, not pixels.
        # for example, the block to the right of (0,0) is (1,0)
        img = pygame.image.load("imgs/border_block.png").convert()
        img = pygame.transform.scale(img, (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self._screen.blit(img, self._convert_board_coordinate(x,y))

    def draw_border(self) -> None:
        # draws the top and bottom row
        for i in range(const.BOARD_WIDTH):
            self._draw_border_block(i, 0)
            self._draw_border_block(i, const.BOARD_HEIGHT - 1)
        # draws the side columns
        for i in range(const.BOARD_HEIGHT):
            self._draw_border_block(0, i)
            self._draw_border_block(const.BOARD_WIDTH-1, i)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.draw_border()
            self.handle_events()
            pygame.display.flip()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()

