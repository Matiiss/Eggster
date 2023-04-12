import pygame

from . import common, settings, state, assets, renderer

pygame.init()
common.screen = pygame.display.set_mode(
    (settings.WIDTH, settings.HEIGHT), flags=settings.FLAGS
)
common.clock = pygame.Clock()

# init
assets.load_assets()

common.current_state = state.Game()

running = True
while running:
    common.dt = common.clock.tick(settings.FPS) / 1000
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
        for rect in renderer.debug_stack:
            surf, color, rect, width = rect
            rect = rect.copy()
            rect.topleft -= common.camera
            pygame.draw.rect(surf, color, rect, width)

    pygame.display.flip()
