import os
import json
import pathlib

import pygame

from .spritesheet import AsepriteSpriteSheet
from .level import Level

images = {}
sfx = {}
maps = {}


def image_path(path, extension="png"):
    return os.path.join("assets/images", f"{path}.{extension}")


def load_image(path):
    return pygame.image.load(image_path(path)).convert_alpha()


def load_sound(path, extension="mp3"):
    return pygame.mixer.Sound(os.path.join("assets/sfx", f"{path}.{extension}"))


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
        }
    )
    sfx.update({"crunch": load_sound("crunch")})
    maps.update({"level_1": Level(level_path("level_1"), load_tiles())})
