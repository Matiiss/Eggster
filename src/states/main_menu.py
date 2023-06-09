import random
import sys

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
                ui.Label(
                    (settings.WIDTH / 2, 100),
                    "by Matiiss",
                    font=assets.fonts["forward"][14],
                    bg=(0, 0, 0, 0),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 170),
                    "Play",
                    width=100,
                    height=40,
                    command=lambda: setattr(common, "current_state", LevelSelector()),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 220),
                    "Settings",
                    font=assets.fonts["forward"][12],
                    width=100,
                    height=40,
                    command=lambda: setattr(common, "current_state", SettingsMenu()),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 270),
                    "Lore",
                    width=100,
                    height=40,
                    command=lambda: setattr(common, "current_state", LoreMenu()),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 320),
                    "Exit",
                    width=100,
                    height=40,
                    command=lambda: sys.exit()
                )
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

        slider_rect = pygame.Rect(0, 0, 100, 20)
        slider_rect.center = (settings.WIDTH / 2, 130)
        self.ui_manager.add(
            [
                ui.Label(
                    (settings.WIDTH / 2, 60),
                    "Settings",
                    font=assets.fonts["forward"][20],
                    bg=(0, 0, 0, 0),
                ),
                ui.Label(
                    (settings.WIDTH / 2, 110),
                    "Music volume",
                    font=assets.fonts["forward"][14],
                    bg=(0, 0, 0, 0),
                ),
                ui.HorizontalSlider(
                    slider_rect.copy(),
                    initial_value=int(common.music_volume * 100),
                    callback=lambda value: setattr(common, "music_volume", value / 100),
                ),
                ui.Label(
                    (settings.WIDTH / 2, 180),
                    "SFX volume",
                    font=assets.fonts["forward"][14],
                    bg=(0, 0, 0, 0),
                ),
                ui.HorizontalSlider(
                    slider_rect.move(0, 70),
                    initial_value=int(common.sfx_volume * 100),
                    callback=lambda value: setattr(common, "sfx_volume", value / 100),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 250),
                    "Fullscreen toggle",
                    width=170,
                    height=30,
                    font=assets.fonts["forward"][12],
                    command=self.toggle_fullscreen,
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
        for widget in self.ui_manager.widgets:
            if isinstance(widget, ui.HorizontalSlider):
                widget.draw(common.screen)

    @staticmethod
    def toggle_fullscreen():
        if settings.FULLSCREEN:
            pygame.display.set_mode(
                (settings.WIDTH, settings.HEIGHT), flags=settings.FLAGS
            )
            settings.FULLSCREEN = False
        else:
            pygame.display.set_mode(
                (settings.WIDTH, settings.HEIGHT),
                flags=settings.FLAGS | pygame.FULLSCREEN,
            )
            settings.FULLSCREEN = True


class LoreMenu(states.State):
    def __init__(self):
        super().__init__()
        self.ui_manager = ui.UIManagerLite()
        self.ui_manager.add(
            [
                ui.Label(
                    (settings.WIDTH / 2, 60),
                    "Lore",
                    font=assets.fonts["forward"][20],
                    bg=(0, 0, 0, 0),
                ),
                ui.Label(
                    (settings.WIDTH / 2, settings.HEIGHT / 2),
                    "uhh...",
                    font=assets.fonts["forward"][12],
                    bg=(0, 0, 0, 0),
                ),
                ui.Label(
                    (settings.WIDTH / 2, settings.HEIGHT / 2 + 20),
                    "in the README.md",
                    font=assets.fonts["forward"][4],
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


class EndScreen(states.State):
    def __init__(self, msg, bg, level):
        super().__init__()
        self.bg = bg

        self.ui_manager = ui.UIManagerLite()
        self.ui_manager.add(
            [
                ui.Label(
                    (settings.WIDTH / 2, 70),
                    msg,
                    font=assets.fonts["forward"][20],
                    bg=(0, 0, 0, 0),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 220),
                    "Play Again",
                    font=assets.fonts["forward"][10],
                    width=100,
                    height=40,
                    command=lambda: setattr(
                        common, "current_state", states.Game(level)
                    ),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 270),
                    "Levels",
                    font=assets.fonts["forward"][10],
                    width=100,
                    height=40,
                    command=lambda: setattr(common, "current_state", LevelSelector()),
                ),
                ui.Button(
                    (settings.WIDTH / 2, 320),
                    "Main Menu",
                    font=assets.fonts["forward"][10],
                    width=100,
                    height=40,
                    command=lambda: setattr(common, "current_state", MainMenu()),
                ),
            ]
        )

    def update(self):
        self.ui_manager.update()

    def render(self):
        renderer.render(self.bg, (0, 0), static=True)
        self.ui_manager.render()
