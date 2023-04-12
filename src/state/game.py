import random

import pygame

from src import common, state, player, assets, renderer, settings, particles


class Game(state.State):
    def __init__(self):
        self.player = player.Player((50, 50))
        common.collision_map = assets.maps["level_1"].collision_map or [
            []
        ]  # what if no second layer
        # print(common.collision_map)
        self.level = assets.maps["level_1"]

        self.night = pygame.Surface(settings.SIZE, flags=pygame.SRCALPHA)
        self.night.fill("grey10")

        self.darkener = pygame.Surface(settings.SIZE)
        self.darkener.fill("grey10")
        self.darkener.set_alpha(120)

        self.particle_manager = particles.ParticleManager(assets.images["particles"])
        self.fast_particle_manager = particles.ParticleManager(
            assets.images["particles_fast"]
        )

    def update(self):
        self.particle_manager.update()
        self.fast_particle_manager.update()
        self.player.update()
        cam = (
            self.player.rect.center
            - pygame.Vector2(settings.WIDTH, settings.HEIGHT) / 2
            - common.camera
        ) * 0.05
        common.camera += round(cam)
        # easter egg??? nope
        common.camera.x, common.camera.y = pygame.math.clamp(
            common.camera.x,
            0,
            len(common.collision_map[0]) * settings.TILE_SIZE - settings.WIDTH,
        ), pygame.math.clamp(
            common.camera.y,
            0,
            len(common.collision_map) * settings.TILE_SIZE - settings.HEIGHT,
        )
        # self.particle_manager.spawn(
        #     self.player.pos.copy(),
        #     pygame.Vector2(1, 0).rotate(random.randint(0, 359)),
        # )

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
                        if settings.DEBUG:
                            renderer.append_to_stack(
                                col.get_rect(
                                    topleft=(
                                        col_num * settings.TILE_SIZE,
                                        row_num * settings.TILE_SIZE,
                                    )
                                )
                            )

        self.player.render()

        # todo turning this off could be an easter egg
        self.night.fill("grey10")

        pygame.draw.circle(
            self.night, (0, 0, 0, 40), self.player.pos - common.camera, 35
        )
        pygame.draw.circle(
            self.night, (0, 0, 0, 20), self.player.pos - common.camera, 25
        )
        pygame.draw.circle(
            self.night, (0, 0, 0, 0), self.player.pos - common.camera, 15
        )

        for _ in range(5):
            self.fast_particle_manager.spawn(
                self.player.pos.copy(),
                pygame.Vector2(1, 0).rotate(random.randint(0, 359)),
            )
        self.fast_particle_manager.render(self.night, pygame.BLEND_RGBA_SUB)
        pygame.draw.circle(
            self.night, "grey10", self.player.pos - common.camera, 100, width=65
        )

        # add those other particles here, so they're drawn on top of the surface
        self.particle_manager.render(self.night, pygame.BLEND_RGBA_SUB)

        renderer.render(self.night, (0, 0), static=True)
        renderer.render(self.darkener, (0, 0), static=True)
