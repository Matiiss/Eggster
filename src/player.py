import functools

import pygame

from . import entity, assets, animation, enums, settings, common, position, renderer, collectibles, inventory


class Player(entity.Entity):
    def __init__(self, pos=(50, 50)):
        super().__init__()

        self.pos = pygame.Vector2(pos)
        self.animation = animation.Animation(assets.images["player"])
        self.image = self.animation.update(enums.EntityState.IDLE)

        # responsible for collision detection and stuffs
        self.pos_rect = pygame.FRect(0, 0, 20, 20)

        # for positioning the image during rendering (see entity.Entity.render)
        self.rect = pygame.FRect(self.image.get_rect())

        # ~~dual collision detection for some tiles, hehe~~
        # nope, it's just masks now
        self.mask = pygame.Mask(self.pos_rect.size, fill=True)

        self.velocity = pygame.Vector2(0, 0)
        self.vel = settings.PLAYER_VEL
        self.tiles = []
        self.masks = []

        self.state = enums.EntityState.IDLE
        self.angle = 90

        self.channel = None

        self.collected = entity.Group()
        self.inventory = inventory.InventoryManager()

    def update(self):
        dx, dy = 0, 0
        self.state = enums.EntityState.IDLE

        # for event in common.events:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE:
        #             pass
        #         elif event.key == pygame.K_d:
        #             self.flip_horizontal = False
        #         elif event.key == pygame.K_a:
        #             self.flip_horizontal = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            dx += 1
            self.state = enums.EntityState.WALK
        if keys[pygame.K_a]:
            dx -= 1
            self.state = enums.EntityState.WALK
        if keys[pygame.K_s]:
            dy += 1
            self.state = enums.EntityState.WALK
        if keys[pygame.K_w]:
            dy -= 1
            self.state = enums.EntityState.WALK

        if dx == 0 and dy == 0:
            self.state = enums.EntityState.IDLE

        self.velocity.xy = dx, dy
        if self.velocity:
            self.velocity.normalize_ip()
        self.velocity *= self.vel
        dx, dy = vel = self.velocity * common.dt

        new_pos = position.Position(self.pos_rect.center)
        cx, cy = new_pos.cx, new_pos.cy

        # self.tiles = self.get_surrounding_tiles(cx, cy)
        # horizontal_projection = self.pos_rect.move(vel.x, 0)
        # vertical_projection = self.pos_rect.move(0, vel.y)
        # for tile in self.tiles:
        #     if horizontal_projection.colliderect(tile):
        #         if vel.x > 0:
        #             vel.x = tile.left - self.pos_rect.right
        #         elif vel.x < 0:
        #             vel.x = tile.right - self.pos_rect.left
        #     if vertical_projection.colliderect(tile):
        #         if vel.y > 0:
        #             vel.y = tile.top - self.pos_rect.bottom
        #         elif vel.y < 0:
        #             vel.y = tile.bottom - self.pos_rect.top

        self.masks = self.get_surrounding_masks(cx, cy)
        resolution = 0.05
        safeguard = 100
        for mask, pos in self.masks:
            last = None
            counter = 0
            while (
                self.mask.overlap(
                    mask, pos - pygame.Vector2(self.pos_rect.move(vel.x, 0).topleft)
                )
                is not None
            ):
                if vel.x > 0 and last is None:
                    vel.x -= resolution
                    last = "gt"
                elif vel.x < 0 and last is None:
                    vel.x += resolution
                    last = "lt"

                elif last == "gt":
                    vel.x -= resolution
                elif last == "lt":
                    vel.x += resolution
                counter += 1
                if counter > safeguard:
                    break

            last = None
            counter = 0
            while (
                self.mask.overlap(
                    mask, pos - pygame.Vector2(self.pos_rect.move(0, vel.y).topleft)
                )
                is not None
            ):
                if vel.y > 0 and last is None:
                    vel.y -= resolution
                    last = "gt"
                elif vel.y < 0 and last is None:
                    vel.y += resolution
                    last = "lt"

                elif last == "gt":
                    vel.y -= resolution
                elif last == "lt":
                    vel.y += resolution
                counter += 1
                if counter > safeguard:
                    break

        self.pos += vel

        renderer.append_to_stack(self.pos_rect)
        renderer.append_to_stack(self.rect)

        if self.velocity:
            self.angle = self.velocity.angle_to(pygame.Vector2(1, 0))

        self.image = self.rotate(
            self.animation.update(self.state),
            self.angle,
        )

        self.pos_rect.center = self.pos
        self.rect = self.image.get_rect(center=self.pos_rect.center)

        self.play_sfx()

    def play_sfx(self):
        if self.channel is not None and self.channel.get_busy():
            return
        if self.state == enums.EntityState.WALK:
            self.channel = assets.sfx["crunch"].play()

    @staticmethod
    @functools.lru_cache(maxsize=512)
    def collides(cx: int, cy: int) -> bool:
        map_ = common.collision_map
        if 0 <= cy < len(map_) and 0 <= cx < len(map_[0]):
            return map_[cy][cx]
        return True

    def get_surrounding_tiles(self, cx, cy) -> list[pygame.Rect]:
        tiles = [
            pygame.Rect(
                cx * settings.TILE_SIZE,
                cy * settings.TILE_SIZE,
                settings.TILE_SIZE,
                settings.TILE_SIZE,
            )
            for cx, cy in (
                (cx - 1, cy - 1),
                (cx, cy - 1),
                (cx + 1, cy - 1),
                (cx + 1, cy),
                (cx + 1, cy + 1),
                (cx, cy + 1),
                (cx - 1, cy + 1),
                (cx - 1, cy),
            )
            if self.collides(cx, cy)
        ]
        return tiles

    def get_surrounding_masks(self, cx, cy):
        masks = []
        for cx, cy in (
            (cx - 1, cy - 1),
            (cx, cy - 1),
            (cx + 1, cy - 1),
            (cx + 1, cy),
            (cx + 1, cy + 1),
            (cx, cy + 1),
            (cx - 1, cy + 1),
            (cx - 1, cy),
            (cx, cy),
        ):
            pos = (cx * settings.TILE_SIZE, cy * settings.TILE_SIZE)
            if self.collides(cx, cy):
                if not (cx < 0 or cy < 0):
                    try:
                        masks.append(
                            (
                                common.mask_collision_map[cy][cx],
                                pos,
                            )
                        )
                    except IndexError:
                        masks.append(
                            (
                                pygame.Mask(
                                    (settings.TILE_SIZE, settings.TILE_SIZE), fill=True
                                ),
                                pos,
                            )
                        )

                else:
                    masks.append(
                        (
                            pygame.Mask(
                                (settings.TILE_SIZE, settings.TILE_SIZE), fill=True
                            ),
                            pos,
                        )
                    )

        return masks

    def collect(self, collectible_group: entity.Group):
        lst = []
        for collectible in collectible_group:
            if self.pos_rect.colliderect(collectible.rect):
                assets.sfx["sloop"].play()
                lst.append(collectible)
                self.collected.add(collectible)

                if isinstance(collectible, collectibles.Basket):
                    self.inventory.update(collectible.items)

        for collectible in lst:
            collectible_group.remove(collectible)
