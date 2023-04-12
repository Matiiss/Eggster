import functools

import pygame

from src import renderer


class Entity:
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect
    groups: set

    def __init__(self):
        self.groups = set()

    def kill(self):
        for group in self.groups:
            group.remove(self)

    def render(self):
        renderer.render(self.image, self.rect)

    @staticmethod
    @functools.lru_cache()
    def rotate(image, angle):
        return pygame.transform.rotate(image, angle)

