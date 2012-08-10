import sys
from math import pi, sin, cos, sqrt

import pygame
from pygame.locals import *

RESOLUTION = 1024, 700
MIN_HUD_WIDTH = 150
HUD_COLOR = pygame.color.Color(0, 255, 0)
HEXAGON_COLOR  = pygame.color.Color(255, 0, 0)
EXIT_KEYS = K_ESCAPE,
CENTER_HEXAGON = 0.15
FIRST_ROW_COUNT = 5
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
        self.calculate_grid()
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
        self.outer_radius = RESOLUTION[1]/2 - 20 # TODO: Make relative
        self.inner_radius = int(self.outer_radius * CENTER_HEXAGON)

    def calculate_grid(self):
        self.cell_size = int(self.inner_radius * 2 * sqrt(3) / FIRST_ROW_COUNT)
        self.row_count = (self.outer_radius - self.inner_radius) / self.cell_size

    def cells_on_row(self, n):
        return int((self.inner_radius + n * self.cell_size) * 2 * sqrt(3)) / self.cell_size

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
        coords = self.calculate_hexagon(self.game_area.center,
                                        self.outer_radius)
        pygame.draw.polygon(self.surface, HEXAGON_COLOR, coords)

        for section in self.sections:
            section.draw_overview()

        coords2 = self.calculate_hexagon(self.game_area.center,
                                         self.inner_radius)
        pygame.draw.polygon(self.surface, BLACK, coords2)

        for g_radius in range(self.inner_radius, self.outer_radius,
                              self.cell_size):
            grid_coords = self.calculate_hexagon(self.game_area.center,
                                                 g_radius)
            pygame.draw.polygon(self.surface, BLACK, grid_coords, 1)

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
        for i in range(6):
            self.sections.append(Section(self, i * pi/3 + pi/2))

class Section():
    def __init__(self, game, angle):
        self.game = game
        self.angle = angle
        self.create_cells()
        for t in self.cells:
            for _ in t:
                print ".",
            print ""

    def create_cells(self):
        self.cells = []
        for x in range(self.game.row_count):
            row = [Cell(self, x, y) for y in range(self.game.cells_on_row(x))]
            self.cells.append(row)

    def draw_overview(self):
        cx, cy = self.game.game_area.center
        vx = cx + self.game.outer_radius * sin(self.angle)
        vy = cy + self.game.outer_radius * cos(self.angle)
        pygame.draw.aaline(self.game.surface,
                           BLACK, (vx, vy), (cx, cy))

class Cell():
    def __init__(self, section, x, y):
        self.section = section
        self.x = x
        self.y = y

    def draw_overview(self):
        return

def main():
        pygame.init()

        game = Game(pygame.display.set_mode(RESOLUTION))
        game.mainloop()
        return 0

if __name__ == "__main__":
    main()
