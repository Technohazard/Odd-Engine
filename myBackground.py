import pygame
import myColors
from gameStuff import *

class cMyBG():
    def __init__(self, fname_list = [("./", 0)]):
        self.BGlist = []
        self.img = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.img.convert_alpha()
        self.rect = pygame.Rect((0,0),(WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.colorObj = myColors.colorHelper()
        self.transColor = self.colorObj.getColor("TRANSPARENT")        
        self.img.fill(self.colorObj.BGCOLOR) # fill with background color 
        self.img.set_colorkey(self.transColor)
        
        self.dirty = False
        #set transparent color to global default
        self.transColor = self.colorObj.getColor("TRANSPARENT") 

        for f in fname_list:
            if f[0] != "./":
                self.load(f[0], f[1])
    
    def scroll(self, bg_select, amount = (-1,0)):
        bg_select.scroll(amount[0],amount[1])
        self.dirty = True
    
    def scroll_all(self, amount = (-1,0)):
        for bg in self.BGlist:
            self.scroll(bg[0], amount)
    
    def update(self):
        self.scroll_all()
            
    def load(self, filename="./", init_layer = 0):
            try:
                tempImg = pygame.image.load(filename)
                tempImg.convert_alpha()
                tempImg.set_colorkey(self.transColor)
                print("Loaded BG: " + str(filename))
            except IOError:
                tempMsg = "load_img() image load failed"
                self.errorQueue.append(tempMsg)
                self.isError = True
                del tempMsg
            temp_tup = (tempImg, init_layer)
            self.BGlist.append((tempImg, init_layer))
    
    def draw(self, surface = None):
        """
        collapses all bg layers from BGlist into one background layer
        clears the self.dirty flag!
        if passed a valid surface, also blits to that surface as well as self.img
        """
        for bg in self.BGlist:
            tmpImg = bg[0]
            tmp_rect = bg[0].get_rect()
            self.img.blit(tmpImg, self.rect, tmp_rect)
        
        self.rect = self.img.get_rect()
        if isinstance(surface, pygame.Surface):
            surface.blit(self.img, self.rect)
        self.dirty = False
    
    def get_img(self):
        """
        returns latest collapsed draw image of all bgs
        """
        return self.img
    
    def redraw_rect(self, surface, temp_rect):
        """
        redraws a portion of the background to the target surface, defined by target rect
        """
        surface.blit(self.img, temp_rect)
        
    def isDirty(self):
        return self.dirty