import pygame

from . import states, entity


screen: pygame.Surface
clock: pygame.Clock
current_state: states.State

camera: pygame.Vector2 = pygame.Vector2()

dt: float = 0
events: list[pygame.Event] = []

collision_map: list[list[bool]] = [[]]
mask_collision_map: list[list[pygame.Mask]] = [[]]
collectibles: entity.Group
mission_group: entity.Group
mission_started: bool = False
level_map: pygame.Surface

mouse_world_pos: pygame.Vector2
mouse_direction: pygame.Vector2
