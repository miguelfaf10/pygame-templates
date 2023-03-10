import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *

DELTA = 50

class Editor:
    def __init__(self):
        
        # main setup
        self.display_surface = pygame.display.get_surface()
    
        # navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector(0,0)
    
    # input    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
                 
    def pan_input(self, event):
        
        # middle mouse button pressed / released
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin    
            
        if not mouse_buttons()[1]:
            self.pan_active = False
        
        # mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y += (event.y)*DELTA
            else:
                self.origin.x -= (event.y)*DELTA
        
        # panning update
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset
       
    # drawing
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE
        
        origin_offset = vector(
            x = self.origin.x % TILE_SIZE, 
            y = self.origin.y % TILE_SIZE)
        
        for col in range(cols):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self. display_surface, LINE_COLOR, (x,0), (x,WINDOW_HEIGHT))
            
        for row in range(rows):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self. display_surface, LINE_COLOR, (0,y), (WINDOW_WIDTH,y))
            
    def run(self, dt):
        self.display_surface.fill('white')
        self.draw_tile_lines()
        self.event_loop()
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)