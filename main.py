import sys
import pygame
import random
import const

BLOCK_TYPES = ['i', 'j', 'l', 'o', 's', 't', 'z']
BLOCK_SHAPES = [
    # block i
    [
        [[0,0,0,0],
         [1,1,1,1],
         [0,0,0,0],
         [0,0,0,0]],
        [[0,0,1,0],
         [0,0,1,0],
         [0,0,1,0],
         [0,0,1,0]]
    ],
    # block j
    [
        [[0,0,0,0],
         [1,0,0,0],
         [1,1,1,0],
         [0,0,0,0]],
        [[0,0,1,1],
         [0,0,1,0],
         [0,0,1,0],
         [0,0,0,0]],
        [[0,0,0,0],
         [1,1,1,0],
         [0,0,1,0],
         [0,0,0,0]],
        [[0,1,0,0],
         [0,1,0,0],
         [1,1,0,0],
         [0,0,0,0]]
    ],
    # block l
    [
        [[0,0,0,0],
         [0,0,0,1],
         [0,1,1,1],
         [0,0,0,0]],
        [[0,0,1,0],
         [0,0,1,0],
         [0,0,1,1],
         [0,0,0,0]],
        [[0,0,0,0],
         [1,1,1,0],
         [1,0,0,0],
         [0,0,0,0]],
        [[1,1,0,0],
         [0,1,0,0],
         [0,1,0,0],
         [0,0,0,0]]
    ],
    # block o
    [
        [[0,0,0,0],
         [0,1,1,0],
         [0,1,1,0],
         [0,0,0,0]]
    ],
    # block s
    [
        [[0,0,0,0],
         [0,1,1,0],
         [1,1,0,0],
         [0,0,0,0]],
        [[1,0,0,0],
         [1,1,0,0],
         [0,1,0,0],
         [0,0,0,0]]
    ],
    # block t
    [
        [[0,0,0,0],
         [0,1,0,0],
         [1,1,1,0],
         [0,0,0,0]],
        [[0,1,0,0],
         [0,1,1,0],
         [0,1,0,0],
         [0,0,0,0]],
        [[0,0,0,0],
         [1,1,1,0],
         [0,1,0,0],
         [0,0,0,0]],
        [[0,1,0,0],
         [1,1,0,0],
         [0,1,0,0],
         [0,0,0,0]]
    ],
    # block z
    [
        [[0,0,0,0],
         [0,1,1,0],
         [0,0,1,1],
         [0,0,0,0]],
        [[0,0,0,1],
         [0,0,1,1],
         [0,0,1,0],
         [0,0,0,0]]
    ]
]

class Block:
    def __init__(self, type: str, rot: int, x: int, y: int):
        self.type = type
        self.rot = rot
        self.x = x
        self.y = y

class TetrisGame:
    def __init__(self):
        self._initialize_pygame()

        # make the custom settings
        self._custom_settings()

        # make the grid
        self._grid = [[0 for _ in range(const.BOARD_WIDTH)] for _ in range(const.BOARD_HEIGHT)]

        self._block_in_motion = self._get_random_block()

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

    def _draw_block(self, x: int, y: int, img_path: str) -> None:
        # draw a single block with a given color at a given (x,y) position
        # the (x,y) position is given should be based of the tetris board, not pixels.
        # for example, the block to the right of (0,0) is (1,0)
        img = pygame.image.load(img_path).convert()
        img = pygame.transform.scale(img, (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self._screen.blit(img, self._convert_board_coordinate(x,y))

    def _erase_block(self, x: int, y: int) -> None:
        # erase the block so it matches background
        img = pygame.image.load("imgs/background.png").convert()
        img = pygame.transform.scale(img, (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self._screen.blit(img, self._convert_board_coordinate(x, y))

    def _erase_block_in_motion(self) -> None:
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if shape_grid[j][i] == 1:
                    self._erase_block(self._block_in_motion.x+1+i,self._block_in_motion.y+1+j)

    def draw_border(self) -> None:
        # draws the top and bottom row
        for i in range(const.BOARD_WIDTH):
            self._draw_block(i, 0, "imgs/border_block.png")
            self._draw_block(i, const.BOARD_HEIGHT - 1, "imgs/border_block.png")
        # draws the side columns
        for i in range(const.BOARD_HEIGHT):
            self._draw_block(0, i, "imgs/border_block.png")
            self._draw_block(const.BOARD_WIDTH-1, i, "imgs/border_block.png")

    def draw_shape(self, block: Block) -> None:
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(block.type)][block.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if shape_grid[j][i] == 1:
                    self._draw_block(block.x+1+i,block.y+1+j,f"imgs/{block.type}_block.png")

    def rotate_shape(self, block: Block) -> None:
        block.rot = (block.rot + 1) % len(BLOCK_SHAPES[BLOCK_TYPES.index(block.type)])

    def _get_random_block(self) -> Block:
        return Block(random.choice(BLOCK_TYPES),0,const.BOARD_WIDTH/2-3,0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # erase the old shape and rotate, then redraw it
                    self._erase_block_in_motion()
                    self.rotate_shape(self._block_in_motion)

    def run(self):
        while True:
            self.draw_border()
            self.draw_shape(self._block_in_motion)
            self.handle_events()
            pygame.display.flip()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()

