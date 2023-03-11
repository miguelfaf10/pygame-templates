import pygame, os
from  pygame.image import load
from editor import Editor, WINDOW_WIDTH, WINDOW_HEIGHT


os.environ["SDL_VIDEODRIVER"] = "x11"

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.editor = Editor()
        
        # cursor

#        cursor = pygame.cursors.Cursor((21,21))
#        pygame.mouse.set_cursor(cursor)
        
    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            self.editor.run(dt)    
            pygame.display.update()
             
if __name__ == '__main__':
    main = Main()
    main.run()