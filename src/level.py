import json
import os

import pygame

from . import settings, entity, collectibles


class Level:
    def __init__(self, path, image_map):
        with open(path) as file:
            data = json.load(file)

        w, h = data["width"], data["height"]

        self.layers: list[list[list[pygame.Surface | None]]] = [
            [[None for _ in range(w)] for _ in range(h)]
        ]
        self.collision_map = [[False for _ in range(w)] for _ in range(h)]
        self.mask_map = [
            [
                pygame.Surface(
                    (settings.TILE_SIZE, settings.TILE_SIZE), flags=pygame.SRCALPHA
                )
                for _ in range(w)
            ]
            for _ in range(h)
        ]

        self.collectibles = entity.Group()
        self.mission_group = entity.Group()

        self.level_map = pygame.Surface((w, h))
        self.level_map.fill("#C8AD7F")

        data = {layer["name"]: layer for layer in data["layers"]}

        for group in ["background", "collisions", "overlay"]:
            layers = data[group]["layers"]
            for layer in layers:
                self.layers.append([[None for _ in range(w)] for _ in range(h)])
                layer_data = layer["data"]
                for y in range(h):
                    for x in range(w):
                        # numbering is off by one when exporting from Tiled as json
                        img_id = layer_data[y * w + x] - 1

                        self.layers[-1][y][x] = image_map.get(img_id)
                        if group == "collisions":
                            collide = img_id in image_map
                            if not self.collision_map[y][x]:
                                self.collision_map[y][x] = collide
                            if collide:
                                self.mask_map[y][x].blit(image_map[img_id], (0, 0))

        collectible_map = {96: collectibles.Basket}

        for layer in data["collectibles"]["layers"]:
            layer_data = layer["data"]
            for y in range(h):
                for x in range(w):
                    # numbering is off by one when exporting from Tiled as json
                    img_id = layer_data[y * w + x] - 1
                    image = image_map.get(img_id)
                    if image is None:
                        continue

                    collectible = collectible_map[img_id](
                        (x * settings.TILE_SIZE, y * settings.TILE_SIZE), image
                    )
                    self.collectibles.add(collectible)

        for layer in data["mission"]["layers"]:
            layer_data = layer["data"]
            for y in range(h):
                for x in range(w):
                    # numbering is off by one when exporting from Tiled as json
                    img_id = layer_data[y * w + x] - 1
                    image = image_map.get(img_id)
                    if image is None:
                        continue

                    target = entity.Entity()
                    target.image = image
                    target.rect = image.get_rect(
                        topleft=(x * settings.TILE_SIZE, y * settings.TILE_SIZE)
                    )
                    target.hit = False
                    self.mission_group.add(target)

                    self.level_map.set_at((x, y), "red")

        self.level_map = pygame.transform.scale_by(self.level_map, 4)

        self.mask_map = [
            [pygame.mask.from_surface(surf, threshold=1) for surf in row]
            for row in self.mask_map
        ]
        self.world_surf = pygame.Surface(
            (w * settings.TILE_SIZE, h * settings.TILE_SIZE)
        )
        for layer in self.layers:
            for row_num, row in enumerate(layer):
                for col_num, col in enumerate(row):
                    if col is not None:
                        self.world_surf.blit(
                            col,
                            (
                                col_num * settings.TILE_SIZE,
                                row_num * settings.TILE_SIZE,
                            ),
                        )
