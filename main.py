import sys
import pygame
import random
import const

BLOCK_TYPES = ['i', 'j', 'l', 'o', 's', 't', 'z']
BLOCK_SHAPES = [
    # block i
    [
        [[1,1,1,1]],
        [[1],
         [1],
         [1],
         [1]]
    ],
    # block j
    [
        [[1,0,0],
         [1,1,1]],
        [[1,1],
         [1,0],
         [1,0]],
        [[1,1,1],
         [0,0,1]],
        [[0,1],
         [0,1],
         [1,1]]
    ],
    # block l
    [
        [[0,0,1],
         [1,1,1]],
        [[1,0],
         [1,0],
         [1,1]],
        [[1,1,1],
         [1,0,0]],
        [[1,1],
         [0,1],
         [0,1]]
    ],
    # block o
    [
        [[1,1],
         [1,1]]
    ],
    # block s
    [
        [[0,1,1],
         [1,1,0]],
        [[1,0],
         [1,1],
         [0,1]]
    ],
    # block t
    [
        [[0,1,0],
         [1,1,1]],
        [[1,0],
         [1,1],
         [1,0]],
        [[1,1,1],
         [0,1,0]],
        [[0,1],
         [1,1],
         [0,1]]
    ],
    # block z
    [
        [[1,1,0],
         [0,1,1]],
        [[0,1],
         [1,1],
         [1,0]]
    ]
]

class Block:
    def __init__(self, type: str, rot: int, x: int, y: int):
        self.type = type
        self.rot = rot
        self.x = x
        self.y = y

    def right_most_block(self) -> int:
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self.type)][self.rot]
        return self.x + len(shape_grid[0])

    def bottom_most_block(self) -> int:
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self.type)][self.rot]
        return self.y + len(shape_grid)

class TetrisGame:
    def __init__(self):
        self._initialize_pygame()

        # make the custom settings
        self._custom_settings()

        # make the grid
        self._grid = [[None for _ in range(const.BOARD_HEIGHT)] for _ in range(const.BOARD_WIDTH)]

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
                if shape_grid[i][j] == 1:
                    self._erase_block(self._block_in_motion.x+1+j,self._block_in_motion.y+1+i)

    def draw_border(self) -> None:
        # draws the top and bottom row
        for i in range(const.BOARD_WIDTH):
            self._draw_block(i, 0, "imgs/border_block.png")
            self._draw_block(i, const.BOARD_HEIGHT - 1, "imgs/border_block.png")
            self._grid[i][0] = "imgs/border_block.png"
            self._grid[i][const.BOARD_HEIGHT-1] = "imgs/border_block.png"

        # draws the side columns
        for i in range(const.BOARD_HEIGHT):
            self._draw_block(0, i, "imgs/border_block.png")
            self._draw_block(const.BOARD_WIDTH-1, i, "imgs/border_block.png")
            self._grid[0][i] = "imgs/border_block.png"
            self._grid[const.BOARD_WIDTH-1][i] = "imgs/border_block.png"

    def draw_shape(self, block: Block) -> None:
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(block.type)][block.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if shape_grid[i][j] == 1:
                    self._draw_block(block.x+1+j,block.y+1+i,f"imgs/{block.type}_block.png")

    def draw_grid(self) -> None:
        for i in range(len(self._grid)):
            for j in range(len(self._grid[i])):
                if (self._grid[i][j] != None and self._grid[i][j] != "imgs/border_block.png"):
                    self._draw_block(i,j,self._grid[i][j])

    def place_block_in_motion_on_grid(self) -> None:
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if shape_grid[i][j] == 1:
                    self._grid[self._block_in_motion.x+1+j][self._block_in_motion.y+1+i] = \
                        f"imgs/{self._block_in_motion.type}_block.png"

    def rotate_shape(self, block: Block) -> None:
        block.rot = (block.rot + 1) % len(BLOCK_SHAPES[BLOCK_TYPES.index(block.type)])

    def rotate_shape_back(self, block: Block) -> None:
        block.rot = (block.rot - 1) % len(BLOCK_SHAPES[BLOCK_TYPES.index(block.type)])

    def drop_block(self, block: Block) -> None:
        block.y += 1

    def block_left(self, block: Block) -> None:
        block.x -= 1

    def block_right(self, block: Block) -> None:
        block.x += 1

    def _get_random_block(self) -> Block:
        return Block(random.choice(BLOCK_TYPES),0,int(const.BOARD_WIDTH/2-3),0)

    def block_in_motion_can_move_left(self) -> bool:
        self.block_left(self._block_in_motion)
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if (shape_grid[i][j] == 1 and
                        self._grid[self._block_in_motion.x+1+j][self._block_in_motion.y+1+i] != None):
                    self.block_right(self._block_in_motion)
                    return False

        self.block_right(self._block_in_motion)
        return self._block_in_motion.x > 0

    def block_in_motion_can_move_right(self) -> bool:
        self.block_right(self._block_in_motion)
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if (shape_grid[i][j] == 1 and
                        self._grid[self._block_in_motion.x+1+j][self._block_in_motion.y+1+i] != None):
                    self.block_left(self._block_in_motion)
                    return False

        self.block_left(self._block_in_motion)
        return self._block_in_motion.right_most_block() < const.BOARD_WIDTH - 2

    def block_in_motion_can_move_down(self) -> bool:
        self.drop_block(self._block_in_motion)
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if (shape_grid[i][j] == 1 and
                        self._grid[self._block_in_motion.x+1+j][self._block_in_motion.y+1+i] != None):
                    self._block_in_motion.y -= 1
                    return False

        self._block_in_motion.y -= 1
        return self._block_in_motion.bottom_most_block() < const.BOARD_HEIGHT - 2

    def get_rows_of_block_in_motion(self) -> [int]:
        rows = []
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            rows.append(self._block_in_motion.y + 1 + i)

        return rows

    def row_is_filled(self, row: int) -> bool:
        for i in range(const.BOARD_WIDTH):
            if self._grid[i][row] == None:
                return False
        return True

    def _amount_to_drop(self, row: int, filled_rows: [int]) -> int:
        amount = 0
        for i in filled_rows:
            if i > row:
                amount += 1

        return amount

    def drop_column(self, col: int, filled_rows: [int]) -> None:
        if filled_rows == []:
            return

        for row in range(const.BOARD_HEIGHT-3, 1, -1):
            if self._grid[col][row] != None:
                if self._amount_to_drop(row, filled_rows) != 0:
                    self._grid[col][row+self._amount_to_drop(row, filled_rows)] = self._grid[col][row]
                    self._grid[col][row] = None
                    self._erase_block(col, row)

    def drop_columns(self, filled_rows: [int]) -> None:
        for i in range(1, const.BOARD_WIDTH-1):
            self.drop_column(i, filled_rows)

    def clear_filled_rows(self):
        rows = self.get_rows_of_block_in_motion()

        filled_rows = []

        for row in rows:
            if self.row_is_filled(row):
                filled_rows.append(row)

                # clear this row
                for i in range(const.BOARD_WIDTH-2):
                    self._grid[i+1][row] = None
                    self._erase_block(i+1,row)

        self.drop_columns(filled_rows)



    def handle_keys(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            # check if there is anything to the left of the block
            if self.block_in_motion_can_move_left():
                # erase the old shape and drop the new one down 1
                self._erase_block_in_motion()
                self.block_left(self._block_in_motion)

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            # check if there is anything to the right of the block
            if self.block_in_motion_can_move_right():
                # erase the old shape and drop the new one down 1
                self._erase_block_in_motion()
                self.block_right(self._block_in_motion)

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if self.block_in_motion_can_move_down():
                # erase the old shape and drop the new one down 1
                self._erase_block_in_motion()
                self.drop_block(self._block_in_motion)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # exit game
                    sys.exit()

                if event.key == pygame.K_UP:
                    # rotate the block
                    self._erase_block_in_motion()
                    self.rotate_shape(self._block_in_motion)
                    if (self._block_in_motion.x < 0 or
                            self._block_in_motion.right_most_block() > const.BOARD_WIDTH - 2 or
                            self._block_in_motion.bottom_most_block() > const.BOARD_HEIGHT - 2):
                        self.rotate_shape_back(self._block_in_motion)

                if event.key == pygame.K_c:
                    # respawn a new motion block
                    self._erase_block_in_motion()
                    self._block_in_motion = self._get_random_block()

        self.handle_keys()

    def run(self):
        self._block_in_motion = self._get_random_block()
        self.draw_border()
        while True:
            pygame.time.Clock().tick(20)
            self.handle_events()

            if not self.block_in_motion_can_move_down():
                # lock the block in motion
                self.place_block_in_motion_on_grid()
                self.clear_filled_rows()
                # spawn new block in motion
                self._block_in_motion = self._get_random_block()

            self.draw_grid()
            self.draw_shape(self._block_in_motion)
            pygame.display.flip()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()

