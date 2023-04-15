import abc

import pygame

from src import common


class State:
    def __init__(self, reset_cam: bool = True):
        if reset_cam:
            common.camera = pygame.Vector2()

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def render(self, *args, **kwargs):
        pass
