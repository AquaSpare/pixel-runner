import pygame.sprite
from pygame.math import Vector2
from pygame.surface import Surface


class Obstacle:
    def __init__(self, position: tuple, sprite: pygame.Surface, velocity: tuple):
        self.position = Vector2(position)
        self.sprite = sprite
        self.velocity = Vector2(velocity)

    def draw(self, surface: Surface):
        surface.blit(self.sprite, self.position)

    def move(self):
        self.position = self.position + self.velocity

    def collides_with(self, other):
        return self.position.distance_to()
