# srsly, I'm basically falling asleep :pg_tired:

import abc
import typing as t

import pygame

from src import renderer, common, assets


Color: t.TypeAlias = (
    str | tuple[int, int, int] | tuple[int, int, int, int] | pygame.Color
)


# whyyy is this so much like an entity????
class Widget(abc.ABC):
    image: pygame.Surface
    rect: pygame.Rect | pygame.FRect

    fg: Color
    bg: Color
    hover_fg: Color
    hover_bg: Color

    width: int | None
    height: int | None
    wraplength: int | None

    font: pygame.Font

    padx: int
    pady: int
    border_width: int
    border_radius: int

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        pass


class UIManagerLite:
    def __init__(self):
        # who cares about the dang z order...
        self.widgets: list[Widget] = []

    def add(self, widgets: Widget | list[Widget]):
        if isinstance(widgets, list):
            # almost used a for loop...
            self.widgets.extend(widgets)
        else:
            self.widgets.append(widgets)

    def update(self, *args, **kwargs):
        for widget in self.widgets:
            widget.update(*args, **kwargs)

        if any(
                widget.collides for widget in self.widgets if isinstance(widget, Button)
        ):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def render(self, target=None):
        for widget in self.widgets:
            renderer.render(widget.image, widget.rect, target=target)


class Label(Widget):
    config = {
        "fg": "#ffece3",
        "bg": "#cc6063",
        "hover_fg": "",
        "hover_bg": "",
        "click_fg": "",
        "click_bg": "",
        "width": None,
        "height": None,
        "wraplength": None,
        "font": None,  # welp
        "padx": 0,
        "pady": 0,
        "border_width": 2,
        "border_radius": 0,
    }

    def __init__(self, pos, text, config: dict | None = None, **kwargs):
        config = (
            type(self).config | kwargs
            if config is None
            else type(self).config | config | kwargs
        )
        for key, value in config.items():
            setattr(self, key, value)

        self.font = self.font or assets.fonts["forward"][16]

        text_surf = self.font.render(text, True, self.fg)
        self.width = self.width or text_surf.get_width() + self.padx * 2
        self.height = self.height or text_surf.get_height() + self.pady * 2

        self.image = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        self.size_rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=pos)

        pygame.draw.rect(
            self.image, self.bg, self.size_rect, border_radius=self.border_radius
        )
        self.image.blit(text_surf, text_surf.get_rect(center=self.size_rect.center))

    def update(self):
        pass


# ~~some button implementation from somewhere~~
# nope, just implementing one from scratch (for who knows which time)
class Button(Widget):
    command: t.Callable = staticmethod(lambda: None)
    click_fg: Color
    click_bg: Color

    config = {
        "fg": "#ffece3",
        "bg": "#cc6063",
        "hover_fg": "",
        "hover_bg": "#b34f52",
        "click_fg": "",
        "click_bg": "#b34f52",
        "width": None,
        "height": None,
        "wraplength": None,
        "font": None,  # welp
        "padx": 4,
        "pady": 4,
        "border_width": 4,
        "border_radius": 20,
    }

    def __init__(self, pos, text, config: dict | None = None, **kwargs):
        config = (
            type(self).config | kwargs
            if config is None
            else type(self).config | config | kwargs
        )
        for key, value in config.items():
            setattr(self, key, value)

        self.font = self.font or assets.fonts["forward"][16]

        self.text_surf = self.font.render(text, True, self.fg)
        self.width = self.width or self.text_surf.get_width() + self.padx * 2
        self.height = self.height or self.text_surf.get_height() + self.pady * 2

        self.image = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        self.size_rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=pos)

        pygame.draw.rect(
            self.image, self.bg, self.size_rect, border_radius=self.border_radius
        )
        self.image.blit(
            self.text_surf, self.text_surf.get_rect(center=self.size_rect.center)
        )

        # self.idle_image = pygame.transform.scale_by(pygame.transform.smoothscale_by(self.image.copy(), 4), 0.25)
        self.idle_image = self.image.copy()

        self.sound_channel: pygame.mixer.Sound | None = None
        self.clicked = False
        self.collides = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        # left, mid, right = pygame.mouse.get_pressed(num_buttons=3)
        self.collides = self.rect.collidepoint(mouse_pos)
        self.image = self.idle_image.copy()

        if not self.clicked and self.collides:  # hovering
            pygame.draw.rect(
                self.image,
                self.hover_bg,
                self.size_rect,
                width=self.border_width,
                border_radius=self.border_radius,
            )
        elif self.clicked:  # pressing down
            pygame.draw.rect(
                self.image,
                self.click_bg,
                self.size_rect,
                border_radius=self.border_radius,
            )
            self.image.blit(
                self.text_surf,
                self.text_surf.get_rect(center=self.size_rect.center),
            )

        for event in common.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.collides:
                    self.sound_channel = assets.sfx["wood_2"].play()
                    self.clicked = True
                else:
                    self.clicked = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.collides and self.clicked:
                    self.sound_channel.play(assets.sfx["wood_2"])
                    # assets.sfx["wood_2"].play()
                    self.command()
                self.clicked = False
