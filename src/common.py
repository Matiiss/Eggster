import pygame

from . import state


screen: pygame.Surface
clock: pygame.Clock
current_state: state.State

camera: pygame.Vector2 = pygame.Vector2()

dt: float = 0
events: list[pygame.Event] = []

collision_map: list[list[bool]] = [[]]
mask_collision_map: list[list[pygame.Mask]] = [[]]
