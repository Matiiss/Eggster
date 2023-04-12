import pygame

from src import common, state, player, assets, renderer, settings


class Game(state.State):
    def __init__(self):
        self.player = player.Player((0, 0))
        common.collision_map = assets.maps["level_1"].collision_map or [
            []
        ]  # what if no second layer
        # print(common.collision_map)
        self.level = assets.maps["level_1"]

    def update(self):
        self.player.update()
        cam = (
                      self.player.rect.center
                      - pygame.Vector2(settings.WIDTH, settings.HEIGHT) / 2
                      - common.camera
              ) * 0.05
        common.camera += round(cam)
        # renderer.camera += cam
        common.camera.x, common.camera.y = pygame.math.clamp(
            common.camera.x, 0, len(common.collision_map[0]) * settings.TILE_SIZE - settings.WIDTH
        ), pygame.math.clamp(
            common.camera.y, 0, len(common.collision_map) * settings.TILE_SIZE - settings.HEIGHT
        )

    def render(self):
        for layer in self.level.layers:
            for row_num, row in enumerate(layer):
                for col_num, col in enumerate(row):
                    if col is not None:
                        renderer.render(
                            col,
                            (
                                col_num * settings.TILE_SIZE,
                                row_num * settings.TILE_SIZE,
                            ),
                        )

        self.player.render()
