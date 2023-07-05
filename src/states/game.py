import itertools
import random

import pygame

from src import (
    common,
    states,
    player,
    assets,
    renderer,
    settings,
    particles,
    level as level_module,
    ui,
)


class Game(states.State):
    def __init__(self, level_name="level_1"):
        super().__init__()

        self.level_name = level_name
        level = level_module.Level(assets.level_path(level_name), assets.load_tiles())
        common.collision_map = level.collision_map
        common.mask_collision_map = level.mask_map
        common.collectibles = level.collectibles
        common.mission_group = level.mission_group
        common.level_map = level.level_map

        common.mission_started = False

        self.level = level
        initial_pos = {
            "level_1": (
                14 * settings.TILE_SIZE + settings.TILE_SIZE / 2,
                settings.TILE_SIZE + settings.TILE_SIZE / 2,
            ),
            "level_2": (
                12 * settings.TILE_SIZE + settings.TILE_SIZE / 2,
                settings.TILE_SIZE + settings.TILE_SIZE / 2,
            ),
            "level_3": (
                23 * settings.TILE_SIZE + settings.TILE_SIZE / 2,
                22 * settings.TILE_SIZE + settings.TILE_SIZE / 2,
            ),
        }
        initial_rotation = {"level_1": -90, "level_2": -90, "level_3": 90}
        self.player = player.Player(
            initial_pos[level_name], initial_rotation[level_name]
        )

        self.night = pygame.Surface(settings.SIZE, flags=pygame.SRCALPHA)
        self.night.fill("grey10")

        self.darkener = pygame.Surface(settings.SIZE)
        # self.darkener.fill("#fff600")  # grey10
        # self.darkener.fill("#FFFF7D")  # grey10
        # self.darkener.fill("#FFFFB3")  # grey10
        self.darkener.fill("grey10")  # grey10
        self.darkener.set_alpha(100)  # 120

        self.particle_manager = particles.ParticleManager(assets.images["particles"])
        self.fast_particle_manager = particles.ParticleManager(
            assets.images["particles_fast"]
        )
        self.info_particle_managers: dict[str, particles.ParticleManager] = {
            "invalid location": particles.ParticleManager.from_string(
                assets.fonts["forward"][8],
                "not on target",
                10,
                delay=[350, 200, 50, 25, 20, 20, 20, 20, 10, 10],
                alpha=range(255, 5, -25),
                color="white",
            ),
            "basket": particles.ParticleManager.from_string(
                assets.fonts["forward"][8],
                "basket",
                10,
                delay=[350, 200, 50, 25, 20, 20, 20, 20, 10, 10],
                alpha=range(255, 5, -25),
                color="white",
            ),
        }

        self.hud_surf = pygame.Surface(
            (settings.WIDTH, settings.HEIGHT), flags=pygame.SRCALPHA
        )

        self.shooting_light = False
        self.last_shot = 0

        self.show_map = False

        level_times = {"level_1": 60 * 10, "level_2": 60 * 10, "level_3": 60 * 10}
        self.total_time = level_times[level_name]  # seconds * minutes = total seconds
        self.time_left = self.total_time

        self.paused = False

        self.ui_manager = ui.UIManagerLite()
        self.ui_manager.add(
            [
                ui.Label(
                    (settings.WIDTH / 2, 70),
                    "Paused",
                    font=assets.fonts["forward"][20],
                    bg=(0, 0, 0, 0),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 270),
                    "Resume",
                    font=assets.fonts["forward"][10],
                    width=100,
                    height=40,
                    command=lambda: setattr(self, "paused", False),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 320),
                    "Main Menu",
                    font=assets.fonts["forward"][10],
                    width=100,
                    height=40,
                    command=lambda: setattr(common, "current_state", states.MainMenu()),
                ),
            ]
        )

    def update(self):
        if self.paused:
            self.ui_manager.update()
            return

        self.time_left -= common.dt
        if self.time_left <= 0:
            self.time_left = 0

        self.particle_manager.update()
        self.fast_particle_manager.update()
        for manager in self.info_particle_managers.values():
            manager.update()

        common.collectibles.update()

        self.update_player()

        self.update_camera()

        common.mouse_world_pos = pygame.mouse.get_pos() + common.camera
        common.mouse_direction = (
            (common.mouse_world_pos - self.player.pos) or pygame.Vector2(1, 0)
        ).normalize()

        current_time = pygame.time.get_ticks()
        time_diff = current_time - self.last_shot
        if self.shooting_light and time_diff >= 50:
            self.last_shot = current_time + time_diff - 50
            for _ in range(10):
                self.particle_manager.spawn(
                    self.player.pos.copy(),
                    common.mouse_direction.rotate(random.randint(-30, 30)) * 150,
                )

        for event in common.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

    def render(self):
        self.render_tiles()

        common.collectibles.render()
        self.player.render()

        self.render_light_overlay()  # todo turning this off could be an easter egg
        self.render_hud()

        if self.time_left <= 0:
            pygame.display.flip()
            common.current_state = states.EndScreen(
                "You ran out of time!\nBetter luck next time!",
                common.screen.copy(),
                self.level_name,
            )
        elif all(target.hit for target in common.mission_group):
            pygame.display.flip()
            common.current_state = states.EndScreen(
                "Mission accomplished!\nYou saved children from tears!",
                common.screen.copy(),
                self.level_name,
            )

    def update_camera(self):
        # cam = (
        #     self.player.rect.center
        #     - pygame.Vector2(settings.WIDTH, settings.HEIGHT) / 2
        #     - common.camera
        # ) * 0.05
        # common.camera += round(cam)

        # todo look into this issue with more stuttering camera
        # or nvm because both seem to be similarly stuttering, this sucks
        # maybe the effect is even more so highlighted by the rigid (aliased) circle around the player
        # the above implementation seems to have a milder effect of this stuttering and I have no clue why...
        # maybe the issue is that the position is that the player's position is not rounded?
        # meh, next time gotta implement a proper camera ig, not that it would immediately fix this issue

        # aaa, these comments suck, not that anyone would read them

        # some conclusions: I have no clue what the fudge is going on, going to figure it out in another game I guess
        # will keep this implementation below using vector methods from now on though

        common.camera = common.camera.lerp(
            (
                round(pygame.Vector2(self.player.rect.center), 0)
                - pygame.Vector2(settings.WIDTH, settings.HEIGHT) / 2
            ),
            0.05,
        )
        common.camera = round(common.camera)

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

    def update_player(self):
        if not self.show_map:
            self.player.update()
        self.player.collect(common.collectibles)
        self.player.inventory.update((10, settings.HEIGHT - 27))

        active_item = self.player.inventory.active_item

        if self.player.inventory.just_collided:
            if active_item is not None and active_item.name == "headlamp":
                self.last_shot = pygame.time.get_ticks()
                self.shooting_light = True
                # assets.sfx["humm"].play(loops=-1)
            else:
                self.shooting_light = False

            if active_item is not None and active_item.name == "map":
                self.show_map = True
                assets.sfx["paper"].play()
            else:
                self.show_map = False

            if active_item is not None and active_item.name is None:
                for target in common.mission_group:
                    if self.player.pos_rect.colliderect(target.rect) and not target.hit:
                        target.image = active_item.image
                        target.hit = True
                        self.player.inventory.remove_just_collided()
                        assets.sfx["plop"].play()
                        break
                else:
                    assets.sfx["nope"].play()
                    self.info_particle_managers["invalid location"].spawn(
                        pygame.mouse.get_pos(), pygame.Vector2(0, -40)
                    )
                    self.player.inventory.active_item = None

    def render_tiles(self):
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
        if common.mission_started:
            common.mission_group.render()

    def render_light_overlay(self):
        if self.shooting_light:
            img = pygame.transform.rotate(
                assets.images["headlamp"],
                common.mouse_direction.angle_to(pygame.Vector2(1, 0)),
            )
            renderer.render(img, img.get_rect(center=self.player.rect.center))

        self.night.fill("grey10")

        largest_radius = 45 if common.mission_started else 70

        pygame.draw.circle(
            self.night, (0, 0, 0, 40), self.player.pos - common.camera, largest_radius
        )
        pygame.draw.circle(
            self.night,
            (0, 0, 0, 20),
            self.player.pos - common.camera,
            largest_radius - 20,
        )
        pygame.draw.circle(
            self.night, (0, 0, 0, 0), self.player.pos - common.camera, 15
        )

        for _ in range(5):
            self.fast_particle_manager.spawn(
                self.player.pos.copy(),
                pygame.Vector2(1, 0).rotate(random.randint(0, 359)) * 80,
            )
        self.fast_particle_manager.render(self.night, pygame.BLEND_RGBA_SUB)
        max_radius = 200
        pygame.draw.circle(
            self.night,
            "grey10",
            self.player.pos - common.camera,
            max_radius,
            width=max_radius - largest_radius,
        )

        # add those other particles here, so they're drawn on top of the surface
        self.particle_manager.render(self.night, pygame.BLEND_RGBA_SUB)

        renderer.render(self.darkener, (0, 0), static=True)
        renderer.render(self.night, (0, 0), static=True)
        # renderer.render(self.darkener, (0, 0), static=True)

    def render_hud(self):
        self.hud_surf.fill((0, 0, 0, 0))

        self.timer_bar()

        if settings.DEBUG:
            pos_surf = assets.fonts["forward"][8].render(
                f"player pos: {self.player.pos_rect.center}", True, "white"
            )
            self.hud_surf.blit(pos_surf, (10, 10))

        self.player.inventory.render(target=self.hud_surf)
        if self.player.inventory.rects:
            initial_x = x = self.player.inventory.rects[-1].x
            for rect in self.player.inventory.rects[:-1]:
                x += rect.width + 1
            self.player.inventory.rects[-1].width = x - initial_x + 3
            pygame.draw.rect(
                self.hud_surf, "white", self.player.inventory.rects[-1], width=1
            )

        if self.show_map:
            rect = common.level_map.get_rect(center=self.hud_surf.get_rect().center)
            renderer.render(common.level_map, rect, static=True, target=self.hud_surf)
            pygame.draw.rect(self.hud_surf, "#2E1308", rect.inflate(4, 4), width=2)
            pygame.draw.rect(self.hud_surf, "#A67B5B", rect.inflate(8, 8), width=2)
            pygame.draw.rect(self.hud_surf, "#87553B", rect.inflate(12, 12), width=2)
            text = assets.fonts["forward"][14].render("map", True, "white")
            renderer.render(
                text,
                text.get_rect(
                    midbottom=rect.inflate(12, 12).midtop + pygame.Vector2(0, -5)
                ),
                static=True,
                target=self.hud_surf,
            )

        for name, manager in self.info_particle_managers.items():
            if name in ["basket"]:
                manager.render(self.hud_surf, static=False)
                continue
            manager.render(self.hud_surf, static=True)

        # show objectives
        if self.time_left > 0 and not all(
            target.hit for target in common.mission_group
        ):
            objective = assets.fonts["forward"][12].render("Objective:", True, "white")
            objective_rect = objective.get_rect(topleft=(10, 10))
            if not common.mission_started:
                img = assets.images["decorations"]["goodies"][0]["image"]
            else:
                img = assets.images["decorations"]["target"][0]["image"]
            renderer.render(
                objective, objective_rect, target=self.hud_surf, static=True
            )
            renderer.render(
                img,
                img.get_rect(midleft=objective_rect.midright),
                target=self.hud_surf,
                static=True,
            )

        if self.paused:
            self.ui_manager.render(target=self.hud_surf, static=True)

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
