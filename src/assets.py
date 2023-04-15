import functools
import os
import json
import pathlib

import pygame

from .spritesheet import AsepriteSpriteSheet
from .level import Level

images = {}
sfx: dict[str, pygame.mixer.Sound] = {}
maps = {}
fonts: dict[str, dict[int, pygame.Font]] = {}


def image_path(path, extension="png"):
    return os.path.join("assets/images", f"{path}.{extension}")


def load_image(path):
    return pygame.image.load(image_path(path)).convert_alpha()


def load_sound(path, extension="mp3"):
    return pygame.mixer.Sound(os.path.join("assets/sfx", f"{path}.{extension}"))


def load_fonts(path, sizes):
    return {size: pygame.Font(os.path.join("assets/fonts", path), size) for size in sizes}


@functools.cache
def load_tiles():
    dct = {}
    with open("assets/maps/tile_map.json") as file:
        data = json.load(file)

    for tile in data["tiles"]:
        path = pathlib.Path(tile["image"])
        dct[tile["id"]] = load_image(f"tiles/{path.stem}")

    return dct


def level_path(path, extension="json"):
    return os.path.join("assets/maps", f"{path}.{extension}")


def set_sound_volume(value):
    for sound in sfx.values():
        sound.set_volume(value)


def load_assets():
    images.update(
        {
            "player": AsepriteSpriteSheet(image_path("player/player")),
            "tiles": load_tiles(),
            "particles": AsepriteSpriteSheet(image_path("particles/particles")),
            "particles_fast": AsepriteSpriteSheet(
                image_path("particles/particles_fast")
            ),
            "eggs": AsepriteSpriteSheet(image_path("eggs/eggs")),
            "decorations": AsepriteSpriteSheet(image_path("decorations/decorations")),
            "headlamp": load_image("player/headlamp"),
            "cobweb": load_image("decorations/cobweb"),
        }
    )
    sfx.update(
        {
            "crunch": load_sound("crunch"),
            "sloop": load_sound("sloop"),
            "nope": load_sound("nope"),
            "paper": load_sound("paper"),
            "humm": load_sound("humm"),
            "plop": load_sound("plop"),
            "wood": load_sound("wood"),
            "wood_1": load_sound("wood_1"),
            "wood_2": load_sound("wood_2")
        }
    )
    # maps.update({"level_1": Level(level_path("level_1"), load_tiles())})
    fonts.update(
        {
            "default": {16: pygame.Font(None, 16)},
            "forward": {**load_fonts("FFFFORWA.TTF", [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 28, 32])},
            "forward_regular": {**load_fonts("fff-forward.regular.ttf", [6, 8, 10, 12, 14, 16, 18])}
        }
    )
