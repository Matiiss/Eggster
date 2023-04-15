import random

import pygame

from src import common, states, player, assets, renderer, settings, particles, ui


class MainMenu(states.State):
    def __init__(self):
        super().__init__()
        self.ui_manager = ui.UIManagerLite()
        self.ui_manager.add(
            [
                ui.Label(
                    (settings.WIDTH / 2, 60),
                    "Eggster",
                    font=assets.fonts["forward"][28],
                    bg=(0, 0, 0, 0),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 150),
                    "Play",
                    width=100,
                    height=40,
                    command=lambda: setattr(common, "current_state", LevelSelector()),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 200),
                    "Settings",
                    font=assets.fonts["forward"][12],
                    width=100,
                    height=40,
                    command=lambda: setattr(common, "current_state", SettingsMenu())
                ),
                ui.Button((settings.WIDTH / 2, 250), "Lore", width=100, height=40),
            ]
        )

        self.particle_manager = particles.ParticleManager(assets.images["particles"])

    def update(self):
        self.ui_manager.update()
        self.particle_manager.update()

    def render(self):
        for pos in [
            (0, 0),
            (settings.WIDTH, 0),
            (settings.WIDTH, settings.HEIGHT),
            (0, settings.HEIGHT),
        ]:
            for _ in range(1):
                self.particle_manager.spawn(
                    pos,
                    pygame.Vector2(1, 0).rotate(random.randint(0, 359)) * 80,
                )
        self.particle_manager.render(static=True)
        self.ui_manager.render()


class LevelSelector(states.State):
    def __init__(self):
        super().__init__()
        self.ui_manager = ui.UIManagerLite()
        self.ui_manager.add(
            [
                ui.Label(
                    (settings.WIDTH / 2, 60),
                    "Levels",
                    font=assets.fonts["forward"][20],
                    bg=(0, 0, 0, 0),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 320),
                    "Back",
                    width=80,
                    height=30,
                    font=assets.fonts["forward"][12],
                    command=lambda: setattr(common, "current_state", MainMenu()),
                ),
                ui.Button(
                    (160, settings.HEIGHT / 2),
                    "Level E",
                    width=95,
                    height=40,
                    command=lambda: setattr(
                        common, "current_state", states.Game("level_1")
                    ),
                ),
                ui.Button(
                    (160 * 2, settings.HEIGHT / 2),
                    "Level B",
                    width=95,
                    height=40,
                    command=lambda: setattr(
                        common, "current_state", states.Game("level_2")
                    ),
                ),
                ui.Button(
                    (160 * 3, settings.HEIGHT / 2),
                    "Level T",
                    width=95,
                    height=40,
                    command=lambda: setattr(
                        common, "current_state", states.Game("level_3")
                    ),
                ),
            ]
        )

        self.particle_manager = particles.ParticleManager(assets.images["particles"])

    def update(self):
        self.ui_manager.update()
        self.particle_manager.update()

    def render(self):
        for pos in [
            (0, 0),
            (settings.WIDTH, 0),
            (settings.WIDTH, settings.HEIGHT),
            (0, settings.HEIGHT),
        ]:
            for _ in range(1):
                self.particle_manager.spawn(
                    pos,
                    pygame.Vector2(1, 0).rotate(random.randint(0, 359)) * 80,
                )
        self.particle_manager.render(static=True)
        self.ui_manager.render()


class SettingsMenu(states.State):
    def __init__(self):
        super().__init__()
        self.ui_manager = ui.UIManagerLite()
        self.ui_manager.add(
            [
                ui.Label(
                    (settings.WIDTH / 2, 60),
                    "Settings",
                    font=assets.fonts["forward"][20],
                    bg=(0, 0, 0, 0),
                ),
                ui.Label(
                    (settings.WIDTH / 2, settings.HEIGHT / 2),
                    "uhh...",
                    font=assets.fonts["forward"][12],
                    bg=(0, 0, 0, 0),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 320),
                    "Back",
                    width=80,
                    height=30,
                    font=assets.fonts["forward"][12],
                    command=lambda: setattr(common, "current_state", MainMenu()),
                ),
            ]
        )

        self.particle_manager = particles.ParticleManager(assets.images["particles"])

    def update(self):
        self.ui_manager.update()
        self.particle_manager.update()

    def render(self):
        for pos in [
            # (0, 0),
            # (settings.WIDTH, settings.HEIGHT),
            (0, settings.HEIGHT),
        ]:
            for _ in range(1):
                self.particle_manager.spawn(
                    pos,
                    pygame.Vector2(1, 0).rotate(random.randint(0, 359)) * 80,
                )
        self.particle_manager.render(static=True)

        self.ui_manager.render()
        renderer.render(assets.images["cobweb"], (settings.WIDTH - 64, 0))
