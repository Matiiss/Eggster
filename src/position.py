import pygame

from . import settings


class Position(pygame.Vector2):
    @property
    def cx(self) -> int:
        return round(self.x) // settings.TILE_SIZE

    @property
    def cy(self) -> int:
        return round(self.y) // settings.TILE_SIZE

    @property
    def xr(self) -> float:
        return (self.x - self.cx * settings.TILE_SIZE) / settings.TILE_SIZE

    @property
    def yr(self) -> float:
        return (self.y - self.cy * settings.TILE_SIZE) / settings.TILE_SIZE
