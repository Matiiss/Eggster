import random

import pygame

from src import common, state, player, assets, renderer, settings, particles


class Game(state.State):
    SHOOT_LIGHT = pygame.event.custom_type()

    def __init__(self):
        self.player = player.Player((50, 50))
        common.collision_map = assets.maps["level_1"].collision_map or [
            []
        ]  # what if no second layer
        common.mask_collision_map = assets.maps["level_1"].mask_map or [[]]
        # print(*common.mask_collision_map, sep="\n")
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

        self.hud_surf = pygame.Surface((settings.WIDTH, settings.HEIGHT), flags=pygame.SRCALPHA)

        self.shooting_light = False

        self.total_time = 60 * 5  # seconds * minutes = total seconds
        self.time_left = self.total_time

    def update(self):
        self.time_left -= common.dt
        if self.time_left <= 0:
            common.current_state = state.State()

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

        common.mouse_world_pos = pygame.mouse.get_pos() + common.camera
        common.mouse_direction = (
            (common.mouse_world_pos - self.player.pos) or pygame.Vector2(1, 0)
        ).normalize()

        for event in common.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shooting_light = not self.shooting_light
                    if self.shooting_light:
                        pygame.time.set_timer(self.SHOOT_LIGHT, 50)
                    elif not self.shooting_light:
                        pygame.time.set_timer(self.SHOOT_LIGHT, 0)

            elif event.type == self.SHOOT_LIGHT:
                for _ in range(10):
                    self.particle_manager.spawn(
                        self.player.pos.copy(),
                        common.mouse_direction.rotate(random.randint(-30, 30)) * 150,
                    )

    def render(self):
        for layer in self.level.layers:
            for row_num, row in enumerate(layer):
                for col_num, col in enumerate(row):
                    if col is not None:
                        # renderer.render(
                        #     col,
                        #     (
                        #         col_num * settings.TILE_SIZE,
                        #         row_num * settings.TILE_SIZE,
                        #     ),
                        # )
                        if settings.DEBUG:
                            renderer.append_to_stack(
                                col.get_rect(
                                    topleft=(
                                        col_num * settings.TILE_SIZE,
                                        row_num * settings.TILE_SIZE,
                                    )
                                )
                            )

        renderer.render(self.level.world_surf, (0, 0))

        self.player.render()
        if self.shooting_light:
            img = pygame.transform.rotate(
                assets.images["headlamp"], common.mouse_direction.angle_to(pygame.Vector2(1, 0))
            )
            renderer.render(img, img.get_rect(center=self.player.rect.center))

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
                pygame.Vector2(1, 0).rotate(random.randint(0, 359)) * 60,
            )
        self.fast_particle_manager.render(self.night, pygame.BLEND_RGBA_SUB)
        pygame.draw.circle(
            self.night, "grey10", self.player.pos - common.camera, 300, width=265
        )

        # add those other particles here, so they're drawn on top of the surface
        self.particle_manager.render(self.night, pygame.BLEND_RGBA_SUB)
        # self.particle_manager.render(self.night, pygame.BLEND_RGBA_MAX)

        renderer.render(self.night, (0, 0), static=True)
        renderer.render(self.darkener, (0, 0), static=True)

        # hud
        self.hud_surf.fill((0, 0, 0, 0))

        self.timer_bar()

        renderer.render(self.hud_surf, (0, 0), static=True)

    def timer_bar(self):
        rect = pygame.FRect(0, 0, 60, 10)
        rect.center = self.hud_surf.get_rect().midtop + pygame.Vector2(0, 10)

        timer_rect = rect.copy()
        timer_rect.width = round(rect.width * (self.time_left / self.total_time))
        timer_rect.right = rect.right

        color = pygame.Color("#0e4d92")
        h, s, v, a = color.hsva
        diff = 360 - h
        color.hsva = (360 - (diff * (self.time_left / self.total_time)), s, v, a)
        pygame.draw.rect(self.hud_surf, color, timer_rect)
        pygame.draw.rect(self.hud_surf, "grey2", rect, width=1)
