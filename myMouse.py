import pygame


class cMyMouse():
    def __init__(self):
        self.pos = (0,0)
        self.dirty = False
        self.clicked = False
        pass
    
    def set_pos(self,pass_pos=(0,0)):
        if self.pos != pass_pos:
            self.pos = pass_pos
            self.dirty = True

    def set_clicked(self, status):
        if status == True:
            self.clicked = status

    def get_pos(self):
        return self.pos