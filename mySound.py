import pygame
from gameStuff import *

class gameSoundHelper():
    def __init__(self):
        self.sfx_list = []
        pass
        
    def load(self, init_path = "./sfx/beeps.wav", init_ref="DEFAULT_BEEP"):
        tempSnd = pygame.mixer.Sound(init_path)
        self.sfx_list.append((init_ref, tempSnd))
        tempStr = "Sound Loaded: " + init_ref + " path: " + init_path
        print(tempStr)
        del tempStr
        del tempSnd
        
    def play(self, init_ref="DEFAULT_BEEP"):
        
        pass
    
    def list_all(self):
        for sfx in self.sfx_list:
            tempStr = sfx[1] + sfx[0]
            print(tempStr)
        del tempStr
    
