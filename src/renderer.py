import pygame

from . import common


debug_stack = []


def render(
    surf,
    pos,
    camera: pygame.Vector2 = None,
    target: pygame.Surface = None,
    static: bool = False,
    special_flags: int = 0,
) -> None:
    if target is None:
        target = common.screen

    if isinstance(pos, (pygame.Rect, pygame.FRect)):
        pos = pos.topleft

    if not static:
        target.blit(surf, pos - common.camera, special_flags=special_flags)
    elif static:
        target.blit(surf, pos, special_flags=special_flags)


def append_to_stack(
    rect: pygame.Rect | pygame.FRect,
    color: str = "red",
    width=1,
    target: pygame.Surface = None,
):
    if target is None:
        target = common.screen
    debug_stack.append((target, color, rect, width))
