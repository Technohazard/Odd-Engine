import pygame

# Constant definitions
WINDOW_WIDTH = 800 # size of window's width in pixels
WINDOW_HEIGHT = 600 # size of windows' height in pixels

SCREEN_RECT = pygame.Rect((0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))

class gameData():
    def __init__(self, init_version="v0.1",
                 init_title="Odd Engine",
                 init_author="Justin Smith",
                 init_email="odd_dimensions@gmail.com",
                 init_website="http://odddimensions.com",
                 init_running=True):
        """
        Handles miscellaneous game options, parameters, info, status, and flow control.
        """
        self.version = init_version
        self.title = init_title
        self.author = init_author
        self.email = init_email
        self.website = init_website
        self.running = init_running    #Game always starts running
        self.paused = False    # Game always starts unpaused
        self.displaycaption = self.title + self.version    # used for window title
        
    def isRunning(self):
        return self.running
    
    def start(self):
        self.running = True
        
    def pause(self):
        if self.paused == False:
            self.paused = True
            return True
        else:
            self.paused = False
            return False
            
    def halt(self):
        self.running = False
        
    def getDisplayCaption(self):
        self.displaycaption = self.title + self.version
        return self.displaycaption