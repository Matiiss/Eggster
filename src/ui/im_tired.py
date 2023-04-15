# srsly, I'm basically falling asleep :pg_tired:

import abc
import typing as t

import pygame

from src import renderer, common, assets, settings


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
        flags = []
        for widget in self.widgets:
            flag = widget.update(*args, **kwargs)
            flags.append(flag)

        if any(
            widget.collides for widget in self.widgets if isinstance(widget, Button)
        ) and not any(flags):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def render(self, target=None, static=True):
        for widget in self.widgets:
            if isinstance(widget, HorizontalSlider):
                continue
            renderer.render(widget.image, widget.rect, target=target, static=static)


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

        prev_alignment = self.font.align
        self.font.align = pygame.FONT_CENTER
        text_surf = self.font.render(text, True, self.fg)
        self.font.align = prev_alignment

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

    def update(self) -> bool:
        ret = False
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
                    ret = True
                self.clicked = False
        return ret


class HorizontalSlider(Widget):
    def __init__(
        self,
        rect: pygame.Rect,
        min_value: int = 0,
        max_value: int = 100,
        step: int = 1,
        callback: callable = lambda _: None,
        initial_value: int = 50
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.range = max_value - min_value
        self.step = min(self.range, max(step, self.range // rect.width))
        self.callback = callback
        self.rail = rect.inflate(0, -0.8 * rect.height)
        self.x, self.y = rect.center
        self.radius = int(rect.width * 0.05)
        self.clicked = False
        self.prev_value = 0

        self.value = initial_value

    def update(self) -> None:
        for event in common.events:
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.collision(event.pos)
            ):
                self.clicked = True
            elif (
                event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                and self.clicked
            ):
                self.clicked = False
                value = self.value
                if self.prev_value != value:
                    self.prev_value = value

            elif event.type == pygame.MOUSEMOTION and self.clicked:
                self.x, self.y = self.clamp_rail(event.pos)
                self.value = round(self.value / self.step) * self.step

    def collision(self, pos: t.Tuple[int, int]) -> bool:
        mx, my = pos
        dx, dy = abs(self.x - mx), abs(self.y - my)
        if dx**2 + dy**2 <= self.radius**2:
            return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "#cc6063", self.rail)
        pygame.draw.circle(surface, "#ffece3", (self.x, self.y), self.radius)

    def clamp_rail(self, pos: t.Tuple[int, int]) -> t.Tuple[int, int]:
        x, y = pos
        new_x = max(self.rail.left + self.radius, min(x, self.rail.right - self.radius))
        return new_x, self.rail.centery

    @property
    def value(self) -> int:
        distance = self.x - (self.rail.left + self.radius)
        rel_val = distance / (self.rail.width - 2 * self.radius)
        value = self.min_value + round((self.range * rel_val) / self.step) * self.step
        return value

    @value.setter
    def value(self, value: int) -> None:
        value = value and round(value / self.step) * self.step - self.min_value
        rel_val = value / self.range
        new_rel_pos = round(rel_val * (self.rail.width - 2 * self.radius))
        self.x = new_rel_pos + self.rail.left + self.radius
        value += self.min_value
        self.prev_value = value
        self.callback(value)
