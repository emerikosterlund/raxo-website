import pygame
import sys
from scenes.world import WorldScene

SCREEN_W, SCREEN_H = 1024, 768
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Oncology Simulator")
    clock = pygame.time.Clock()

    scene = WorldScene(screen)

    while True:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            result = scene.handle_event(event)
            if result is not None:
                scene = result

        scene.update(dt)
        scene.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
