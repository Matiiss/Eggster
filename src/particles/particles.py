from dataclasses import dataclass

import pygame


@dataclass
class Particle:
    pos: pygame.Vector2
    velocity: pygame.Vector2
    time: int
    max_time: int | None = None
