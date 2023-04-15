import pygame

from . import common, settings, states, assets, renderer

pygame.init()
common.screen = pygame.display.set_mode(
    (settings.WIDTH, settings.HEIGHT), flags=settings.FLAGS
)
pygame.display.set_caption("Eggster")
common.clock = pygame.Clock()

# init
assets.load_assets()

common.current_state = states.MainMenu()

running = True
while running:
    common.dt = pygame.math.clamp(common.clock.tick(settings.FPS) / 1000, 0.008, 0.042)
    # pygame.display.set_caption(f"{common.clock.get_fps():.2f}")
    common.screen.fill("black")

    common.events = pygame.event.get()
    for event in common.events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if event.mod & pygame.KMOD_CTRL:
                    settings.DEBUG = not settings.DEBUG
                    print(f"debug: {settings.DEBUG}")

    if settings.DEBUG:
        renderer.debug_stack = []

    common.current_state.update()
    common.current_state.render()

    if settings.DEBUG:
        for row_num, row in enumerate(common.mask_collision_map):
            for col_num, mask in enumerate(row):
                renderer.render(
                    mask.to_surface(),
                    (col_num * settings.TILE_SIZE, row_num * settings.TILE_SIZE),
                )
        if hasattr(common.current_state, "player"):
            renderer.render(common.current_state.player.mask.to_surface(), common.current_state.player.pos_rect.topleft)

        for rect in renderer.debug_stack:
            surf, color, rect, width = rect
            rect = rect.copy()
            rect.topleft -= common.camera
            pygame.draw.rect(surf, color, rect, width)

    pygame.display.flip()
