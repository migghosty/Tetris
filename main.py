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

    '''
    Initializing Tetris Game
    '''

    def __init__(self):
        self._initialize_pygame()

        # make the custom settings
        self._custom_settings()

        # make the grid and get block
        self._grid = [[None for _ in range(const.BOARD_HEIGHT)] for _ in range(const.BOARD_WIDTH)]
        self._next_block = self._get_random_block()

    def _initialize_pygame(self):
        # initialize pygame modules
        pygame.init()

        # define screen size
        self._screen = pygame.display.set_mode([const.SCREEN_WIDTH, const.SCREEN_HEIGHT])

        # initialize the timer so the pieces go down
        self.drop_block_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.drop_block_event, 500)

    def _custom_settings(self):
        # set caption and icon, and title for screen
        pygame.display.set_caption("Tetris Game")
        tetrisIcon = pygame.image.load("imgs/tetris_logo.png")
        pygame.display.set_icon(tetrisIcon)

        img = pygame.image.load("imgs/tetris_title.png").convert()
        img = pygame.transform.scale(img, (200, 60))

        self._screen.blit(img, (50, 50))

        # next block text
        font = pygame.font.SysFont("timesnewroman", 24)
        green = (0,255,0)
        nextBlockText = font.render("Next Block", True, green)
        nextBlockRect = nextBlockText.get_rect()
        nextBlockRect.center = (const.SCREEN_WIDTH // 2 + const.SCREEN_WIDTH // 4,
                                const.SCREEN_HEIGHT // 2 - const.SCREEN_HEIGHT // 8)

        self._screen.blit(nextBlockText, nextBlockRect)

    '''
    Miscellaneous
    '''

    def _get_random_block(self) -> Block:
        return Block(random.choice(BLOCK_TYPES),0,13,4)

    def change_block_in_motion(self) -> None:
        self._block_in_motion = self._next_block
        self._block_in_motion.y = 0
        self._block_in_motion.x = int(const.BOARD_WIDTH/2-3)
        self._erase_next_block()
        self._next_block = self._get_random_block()
        self.draw_shape(self._next_block)

    def _convert_board_coordinate(self, x: int, y: int) -> (int, int):
        return ( x*const.BLOCK_SIZE + const.TOP_LEFT[0], y*const.BLOCK_SIZE + const.TOP_LEFT[1] )

    '''
    Drawing
    '''

    def _draw_block(self, x: int, y: int, img_path: str) -> None:
        # draw a single block with a given color at a given (x,y) position
        # the (x,y) position is given should be based of the tetris board, not pixels.
        # for example, the block to the right of (0,0) is (1,0)
        img = pygame.image.load(img_path).convert()
        img = pygame.transform.scale(img, (const.BLOCK_SIZE, const.BLOCK_SIZE))
        self._screen.blit(img, self._convert_board_coordinate(x,y))

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

    '''
    Erasing
    '''

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

    def _erase_next_block(self) -> None:
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._next_block.type)][self._next_block.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if shape_grid[i][j] == 1:
                    self._erase_block(14+j,5+i) # this is where the next block is located

    '''
    Movement of the block in motion
    '''

    def rotate_shape(self) -> None:
        self._block_in_motion.rot = (self._block_in_motion.rot + 1) \
                                   % len(BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)])

    def rotate_shape_back(self) -> None:
        self._block_in_motion.rot = (self._block_in_motion.rot - 1) % \
                                   len(BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)])

    def drop_block(self) -> None:
        self._block_in_motion.y += 1

    def block_left(self) -> None:
        self._block_in_motion.x -= 1

    def block_right(self) -> None:
        self._block_in_motion.x += 1

    def block_in_motion_can_move_left(self) -> bool:
        self.block_left()
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if (shape_grid[i][j] == 1 and
                        self._grid[self._block_in_motion.x+1+j][self._block_in_motion.y+1+i] != None):
                    self.block_right()
                    return False

        self.block_right()
        return self._block_in_motion.x > 0

    def block_in_motion_can_move_right(self) -> bool:
        self.block_right()
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if (shape_grid[i][j] == 1 and
                        self._grid[self._block_in_motion.x+1+j][self._block_in_motion.y+1+i] != None):
                    self.block_left()
                    return False

        self.block_left()
        return self._block_in_motion.right_most_block() < const.BOARD_WIDTH - 2

    def block_in_motion_can_move_down(self) -> bool:
        self.drop_block()
        shape_grid = BLOCK_SHAPES[BLOCK_TYPES.index(self._block_in_motion.type)][self._block_in_motion.rot]
        for i in range(len(shape_grid)):
            for j in range(len(shape_grid[i])):
                if (shape_grid[i][j] == 1 and
                        self._grid[self._block_in_motion.x+1+j][self._block_in_motion.y+1+i] != None):
                    self._block_in_motion.y -= 1
                    return False

        self._block_in_motion.y -= 1
        return self._block_in_motion.bottom_most_block() < const.BOARD_HEIGHT - 2

    def move_block_in_motion_left(self):
        # check if there is anything to the left of the block
        if self.block_in_motion_can_move_left():
            # erase the old shape and drop the new one down 1
            self._erase_block_in_motion()
            self.block_left()

    def move_block_in_motion_right(self):
        # check if there is anything to the right of the block
        if self.block_in_motion_can_move_right():
            # erase the old shape and drop the new one down 1
            self._erase_block_in_motion()
            self.block_right()

    def move_block_in_motion_down(self):
        if self.block_in_motion_can_move_down():
            # erase the old shape and drop the new one down 1
            self._erase_block_in_motion()
            self.drop_block()

    '''
    Deleting rows
    '''

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
            self.move_block_in_motion_left()

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.move_block_in_motion_right()

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.move_block_in_motion_down()

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
                    self.rotate_shape()
                    if (self._block_in_motion.x < 0 or
                            self._block_in_motion.right_most_block() > const.BOARD_WIDTH - 2 or
                            self._block_in_motion.bottom_most_block() > const.BOARD_HEIGHT - 2):
                        self.rotate_shape_back()

                if event.key == pygame.K_c:
                    # respawn a new motion block
                    self._erase_block_in_motion()
                    self.change_block_in_motion()

            # automatically move the block down
            if event.type == self.drop_block_event:
                self.move_block_in_motion_down()

        self.handle_keys()

    def run(self):
        self.change_block_in_motion()
        self.draw_border()

        while True:
            pygame.time.Clock().tick(15)

            self.handle_events()
            self.draw_grid()
            self.draw_shape(self._block_in_motion)
            pygame.display.flip()

            if not self.block_in_motion_can_move_down():
                # allow the player to move left/right for one second, then lock the block

                # lock the block in motion
                self.place_block_in_motion_on_grid()
                self.clear_filled_rows()
                # spawn new block in motion
                self.change_block_in_motion()



if __name__ == "__main__":
    game = TetrisGame()
    game.run()

