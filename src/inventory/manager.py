import functools
import typing

import pygame

from src import common, renderer, settings

if typing.TYPE_CHECKING:
    from .item import Item


class InventoryManager:
    def __init__(self, items: list["Item"] | None = None):
        self.items = items or []

    def render(self, pos, size=(16, 16), target: pygame.Surface | None = None):
        if target is None:
            target = common.screen
        x, y = pos
        initial_x = x

        for col, item in enumerate(self.items):
            pos = (x, y)
            img = self.resize(item.image, size)
            rect = img.get_rect(topleft=pos).inflate(2, 2)
            x += rect.width + 1
            renderer.render(img, pos, target=target, static=True)
            pygame.draw.rect(target, "white", rect, width=1)

        if self.items:
            rect = pygame.Rect(initial_x - 1, y, x - initial_x - 1, size[1])
            rect.inflate_ip(4, 6)
            pygame.draw.rect(target, "white", rect, width=1)

    @staticmethod
    @functools.cache
    def resize(surf, size):
        return pygame.transform.scale(surf, size)

    def update(self, items: list["Item"]):
        self.items = items
