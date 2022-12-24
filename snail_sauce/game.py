import pygame
from utils import load_sprite


class SnailSauce:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snail Sauce')

        self.screen = pygame.display.set_mode((800, 400))

        self.sky = load_sprite('Sky', False)
        self.ground = load_sprite('ground', False)

    def main_loop(self):
        while True:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    def _game_logic(self):
        ...

    def _draw(self):
        self.screen.blit(self.sky, (0, 0))
        self.screen.blit(self.ground, (0, self.sky.get_height()))

        pygame.display.update()
