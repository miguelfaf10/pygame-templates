import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos

TILE_SIZE = 64
COLS = 20
ROWS = 12
WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE

DELTA = 50

class Editor:
    def __init__(self):
        
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = []
    
        # navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector(0,0)
        
        # support lines
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)
    
        # selection
        self.selection_index = 2
        self.last_selected_cell = None
    
    # support #
    def get_current_cell(self):
        distance_to_origin = vector(mouse_pos()) - self.origin
        col = int(distance_to_origin.x // TILE_SIZE)
        row = int(distance_to_origin.y // TILE_SIZE)
        
        return col,row
    
    # input    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            self.canvas_add() 
                 
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
       
    def canvas_add(self):
        if mouse_buttons()[0]:
            current_cell = self.get_current_cell()
    
            if current_cell not in self.canvas_data:
                self.canvas_data.append(current_cell)
                print(f'Cell {current_cell} added')
            
    # drawing
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE
        
        origin_offset = vector(
            x = self.origin.x % TILE_SIZE, 
            y = self.origin.y % TILE_SIZE)
        
        self.support_line_surf.fill('green')
        
        for col in range(cols):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, 'black', (x,0), (x,WINDOW_HEIGHT))
            
        for row in range(rows):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, 'black', (0,y), (WINDOW_WIDTH,y))
            
        self.display_surface.blit(self.support_line_surf, (0,0))
            
    def draw_level(self):
        for cell_pos in self.canvas_data:
            pos = self.origin + vector(cell_pos) * TILE_SIZE
            
            test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            test_surf.fill('brown')
            self.display_surface.blit(test_surf, pos)
            
    def run(self, dt):
        self.display_surface.fill('gray')
        self.draw_tile_lines()
        self.draw_level( )
        self.event_loop()
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)

