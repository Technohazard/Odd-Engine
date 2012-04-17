import pygame
from pygame.locals import *

class cMyMouse():
    def __init__(self):
        self.pos = (0,0)
        self.rel = (0,0)
        self.rect = pygame.Rect(self.pos, (64,64))
        self.dirty = False
        self.click_log = [((0,0), 1, "UP")] # initialize the click log with
        self.cursor = pygame.Surface((self.rect.w, self.rect.h))
        self.LB = "UP"
        self.RB = "UP"
        self.MB = "UP"
        self.wheelup = "UP"
        self.wheeldown = "UP"
    
    def eventHandler(self, myEvent):
        if myEvent.type == MOUSEMOTION:
            self.set_pos(myEvent.pos)
            self.set_rel(myEvent.rel)
            
        if myEvent.type == MOUSEBUTTONUP:
            self.set_pos(myEvent.pos)
            self.set_button(myEvent.button, "UP")
            self.click(self.pos, myEvent.button, "UP")
            
        if myEvent.type == MOUSEBUTTONDOWN:
            self.set_pos(myEvent.pos)
            self.set_button(myEvent.button, "DOWN")
            self.click(self.pos, myEvent.button, "DOWN")
            
    def set_pos(self, pass_pos = (0,0)):
        if pass_pos != self.pos :
            self.pos = pass_pos
            self.dirty = True
            
    def set_rel(self, pass_rel = (0,0)):
        if pass_rel != self.rel:
            self.rel = pass_rel
            self.dirty = True
            
    def set_button(self, pass_button, click_status):
        if pass_button == 1 :
            self.LB = click_status
        elif pass_button == 2 :
            self.MB = click_status
        elif pass_button == 3 :
            self.RB = click_status
        elif pass_button == 4 :
            self.wheelup = click_status
        elif pass_button == 5 :
            self.wheeldown = click_status
        else:
            #unknown mouse button.
            pass

    def click(self, click_pos, click_btn = "LEFT", click_type = "DOWN"):
        """
        Takes a tuple as a position, and stores it in the clicks log.
        """
        self.click_log.append((click_pos, click_btn, click_type))

    def release(self, click_pos, click_btn = "LEFT", click_type = "UP"):
        """
        Takes a tuple as a position, and stores it in the clicks log.
        """
        self.click_log.append((click_pos, click_btn, click_type))
        
    def get_pos(self):
        return self.pos
        
    def get_rect():
        self.rect.topleft = self.pos
        return self.rect

    """
    MOUSEMOTION	     pos, rel, buttons
    MOUSEBUTTONUP    pos, button
    MOUSEBUTTONDOWN  pos, button
    """
    