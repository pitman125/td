import sys
from math import pi, sin, cos

import pygame
from pygame.locals import *

RESOLUTION = 1024, 700
MIN_HUD_WIDTH = 150
HUD_COLOR = pygame.color.Color(0, 255, 0)
HEXAGON_COLOR  = pygame.color.Color(255, 0, 0)
EXIT_KEYS = K_ESCAPE,
FPS = 60
FPS_COLOR = pygame.color.Color(0, 0, 255)
BACKGROUND_COLOR = pygame.color.Color(255, 255, 255)
DEBUG = True

BLACK = pygame.color.Color(0, 0, 0)

class Game():
    def __init__(self, surface):
        self.surface = surface
        self.running = True
        self.active_section = -1
        self.clock = pygame.time.Clock()
        self.calculate_areas()
        self.init_sections()
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
        if self.active_section == -1:
            self.draw_overview()
        else:
            self.draw_zoomed()
        self.draw_hud()
        if DEBUG:
            self.draw_fps()
    
    def calculate_areas(self):
        screen_width = RESOLUTION[0]
        dynamic = int(screen_width * 0.05)
        width = MIN_HUD_WIDTH if dynamic < MIN_HUD_WIDTH else dynamic
        
        height = RESOLUTION[1]
        self.hud_area = pygame.Rect((0, 0), (width, height))
        self.game_area = pygame.Rect((width, 0),
                                     (RESOLUTION[0] - width, RESOLUTION[1]))
    
    def update_screen(self):
        pygame.display.update()
        
    def draw_fps(self):
        msg = "FPS: %02d" % self.clock.get_fps()
        rendered = self.font.render(msg, False, FPS_COLOR)
        rect = rendered.get_rect()
        self.surface.blit(rendered, rect)
        
    def draw_hud(self):
        pygame.draw.rect(self.surface, HUD_COLOR, self.hud_area)
    
    def draw_overview(self):
        main_radius = RESOLUTION[1]/2 - 20
        coords = self.calculate_hexagon(self.game_area.center, main_radius)
        pygame.draw.polygon(self.surface, HEXAGON_COLOR, coords)
        pygame.draw.circle(self.surface, BLACK, self.game_area.center, main_radius, 1)
        
        for vertex in coords:
            pygame.draw.aaline(self.surface, BLACK, vertex, self.game_area.center)
            
        small_radius = main_radius * 0.1
        coords2 = self.calculate_hexagon(self.game_area.center, small_radius)
        pygame.draw.polygon(self.surface, BLACK, coords2)
        return
    
    def calculate_hexagon(self, center, radius):
        dtheta = pi/3
        theta = pi/2
        coords = []
        r = radius
        for _ in range(6):
            delta = int(r * sin(theta)), int(r * cos(theta))
            coords.append((center[0] + delta[0],
                           center[1] + delta[1]))
            theta += dtheta
        return coords
    
    def draw_zoomed(self):
        zoomed = self.sections[self.active_section]
        # TODO: This
    
    def load_assets(self):
        self.font = pygame.font.Font("./font.ttf", 16)
    
    def init_sections(self):
        self.sections = []
        for _ in range(6):
            self.sections.append(Section(self))

class Section():
    def __init__(self, game):
        self.game = game

def main():
	pygame.init()

	game = Game(pygame.display.set_mode(RESOLUTION))
	game.mainloop()
	return 0

if __name__ == "__main__":
	sys.exit(main())
