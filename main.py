import sys
import pygame


class TetrisGame:
    def __init__(self):
        # initialize pygame modules
        pygame.init()

        # define screen size
        self._screen_width = 700
        self._screen_height = 400
        self._screen = pygame.display.set_mode([self._screen_width, self._screen_height], pygame.RESIZABLE)

        # set caption and icon for screen
        pygame.display.set_caption("Tetris Game")
        tetrisIcon = pygame.image.load("imgs/tetris_logo.png")
        pygame.display.set_icon(tetrisIcon)

    def _get_screen_width(self):
        return pygame.display.get_window_size()[0]

    def _get_screen_height(self):
        return pygame.display.get_window_size()[1]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            self.handle_events()
            pygame.display.flip()



if __name__ == "__main__":
    game = TetrisGame()
    game.run()

