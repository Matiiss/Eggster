from dataclasses import dataclass

import pygame


@dataclass
class Item:
    image: pygame.Surface
    name: str | None = None
