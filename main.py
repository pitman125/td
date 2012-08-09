import sys

import pygame
from pygame.locals import *

RESOLUTION = 640, 480
EXIT_KEYS = K_ESCAPE,
FPS = 60
FPS_COLOR = pygame.color.Color(0, 0, 255)
BACKGROUND_COLOR = pygame.color.Color(255, 255, 255)
DEBUG = True

class Game():
    def __init__(self, surface):
        self.surface = surface
        self.running = True
        self.clock = pygame.time.Clock()
        self.load_assets()

    def mainloop(self):
        while self.running:
            delta = self.clock.tick(FPS)
            self.handle_input()
            self.update_logic(delta)
            self.draw_game()
            self.update_screen()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key in EXIT_KEYS:
                    self.running = False

    def update_logic(self, delta):
        pass

    def draw_game(self):
        self.surface.fill(BACKGROUND_COLOR)
        if DEBUG:
            self.draw_fps()
        pass
    
    def update_screen(self):
        pygame.display.update()
        
    def draw_fps(self):
        msg = "FPS: %s" % self.clock.get_fps()
        rendered = self.font.render(msg, False, FPS_COLOR)
        rect = rendered.get_rect()
        self.surface.blit(rendered, rect)
    
    def load_assets(self):
        self.font = pygame.font.Font("./font.ttf", 32)


def main():
	pygame.init()

	game = Game(pygame.display.set_mode(RESOLUTION))
	game.mainloop()
	return 0

if __name__ == "__main__":
	sys.exit(main())
