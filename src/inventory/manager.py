import functools
import typing as t

import pygame

from src import common, renderer, settings

if t.TYPE_CHECKING:
    from .item import Item


class InventoryManager:
    def __init__(self, items: list["Item"] | None = None):
        self.items = items or []
        self.rects: list[pygame.Rect] = []
        self.images: list[pygame.Surface] = []
        self.active_item: t.Optional["Item"] = None
        self.just_collided: bool = False
        self.collided_index: int | None = None

    def update(self, pos: tuple[int, int], size: tuple[int, int] = (16, 16)):
        x, y = pos
        initial_x = x

        self.just_collided = False
        self.collided_index = None

        self.rects = []
        self.images = []
        collisions = []
        for idx, item in enumerate(self.items.copy()):
            pos = (x, y)
            img = self.resize(item.image, size)
            rect = img.get_rect(topleft=pos).inflate(2, 2)
            x += rect.width + 1

            self.collision(rect, item, idx)
            collided = rect.collidepoint(pygame.mouse.get_pos())
            collisions.append(collided)

            self.rects.append(rect)
            self.images.append(img)

        if any(collisions):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.items:
            rect = pygame.Rect(initial_x - 1, y, x - initial_x - 1, size[1])
            rect.inflate_ip(4, 6)
            self.rects.append(rect)

    def render(self, target: pygame.Surface | None = None):
        if target is None:
            target = common.screen

        for image, rect, item in zip(self.images, self.rects, self.items):
            renderer.render(
                image, image.get_rect(center=rect.center), target=target, static=True
            )
            pygame.draw.rect(target, "white", rect, width=1)
            if self.active_item is item:
                pygame.draw.rect(target, "blue", rect.inflate(2, 2), width=2)

        if self.rects:
            # rect = self.rects[-1]
            # initial_x = x = rect.x
            # for rect in self.rects[:-1]:
            #     x += rect.width + 1
            # rect.width = x - initial_x - 1
            # pygame.draw.rect(target, "white", self.rects[-1], width=1)
            pass

    @staticmethod
    @functools.cache
    def resize(surf, size):
        return pygame.transform.scale(surf, size)

    def update_inventory(self, items: list["Item"]):
        self.items = items

    def collision(self, rect: pygame.Rect | pygame.FRect, item: "Item", idx: int):
        for event in common.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and rect.collidepoint(event.pos):
                    self.active_item = None if self.active_item is item else item
                    self.just_collided = True
                    self.collided_index = idx

    def remove_just_collided(self):
        if self.just_collided:
            self.items.pop(self.collided_index)
            self.rects.pop(self.collided_index)
            self.active_item = None
