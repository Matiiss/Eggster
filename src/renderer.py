import pygame

from . import common


debug_stack = []


def render(surf, pos, camera: pygame.Vector2 = None, target: pygame.Surface = None) -> None:
    if target is None:
        target = common.screen

    if isinstance(pos, (pygame.Rect, pygame.FRect)):
        pos = pos.topleft

    target.blit(surf, pos - common.camera)


def append_to_stack(rect: pygame.Rect | pygame.FRect, color: str = "red", width=1, target: pygame.Surface = None):
    if target is None:
        target = common.screen
    debug_stack.append((target, color, rect, width))
