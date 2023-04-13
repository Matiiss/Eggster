import pygame

from . import assets, animation, entity, inventory


class Collectible(entity.Entity):
    items: list[inventory.Item]

    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = pygame.FRect(image.get_rect(center=pos))
        self.items = []

    def update(self):
        pass


class Basket(Collectible):
    def __init__(self, pos, image):
        super().__init__(pos, image)
        self.rect = pygame.FRect(image.get_rect(topleft=pos))
        images = assets.images
        self.items = [
            inventory.Item(images["headlamp"], name="headlamp"),
            inventory.Item(images["decorations"]["map"][0]["image"], name="map"),
            *[inventory.Item(images["eggs"][""][idx]["image"]) for idx in (1, 3, 4)],
        ]

