import typing as t

import pygame

if t.TYPE_CHECKING:
    from .entity import Entity


class Group:
    entities: set

    def __init__(self):
        self.entities = set()

    def add(self, entity: "Entity"):
        self.entities.add(entity)
        entity.groups.add(self)

    def remove(self, entity: "Entity"):
        self.entities.remove(entity)

    def render(self):
        for entity in self.entities:
            entity.render()
