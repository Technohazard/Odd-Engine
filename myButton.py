import pygame
from gameStuff import *
import myColors

class cMyButton(pygame.sprite.Sprite):
    """
    Class used to create a button. 
    """
    def __init__(self, init_text = "OK", init_pos = (0,0), init_size = (100,50), init_id = 0):
        self.id = init_id
        self.text = init_text
        self.rect = pygame.Rect(init_pos, init_size)
        self.dirty = False
        self.state = "UP"
        
        self.img = pygame.Surface((self.rect.w, self.rect.h))
        self.img.convert_alpha()
        
        self.label = pygame.Surface((self.rect.w, self.rect.h))
        self.label.convert_alpha()
        
        self.colorObj = myColors.colorHelper()
        self.transColor = self.colorObj.getColor("TRANSPARENT")
        
        self.img.set_colorkey(self.transColor)
        self.label.set_colorkey(self.transColor)
        
        self.buttonType = "CLICK"
        self.visible = True

        self.errorQueue=[]
        self.errorQueue.append("Initialized button ID#:" + str(self.id) + " @" + str(self.rect))
        self.isError = True # set this if the error queue contains messages. This should pass init msgs
       
        # set some default appearance values
        self.font_dir = "./fonts/"
        self.font_file = "DIEHLD__.ttf"
        self.font_path = str(self.font_dir + self.font_file)
        self.font_size = 18 
        self.borderWidth = 4
        
        self.bgColor = self.colorObj.BUTTON_BG_COLOR
        self.fontColor = self.colorObj.BUTTON_FONT_COLOR
        self.borderColor = self.colorObj.BUTTON_BORDER_COLOR
        self.clickColor = self.colorObj.BUTTON_CLICK_COLOR
        self.shadowColor = self.colorObj.BUTTON_SHADOW_COLOR
        
        # create font object from font file
        self.fontObj = pygame.font.Font(self.font_path, self.font_size)
        self.lineheight = self.fontObj.get_height()
        self.render()
        
    def update(self):
        pass
    
    def set_pos(self, init_pos = (0,0)):
        self.rect.topleft = init_pos

    def set_label(self, init_label = "OK"):
        self.label = init_label
            
    def load_font(self, init_fontpath = "./", init_fontSize = 32):
        """
        Load a new local font object and determine font line height by size.
        """
        if init_fontpath != self.fontpath:
            self.fontpath = init_fontpath
            self.fontsize = init_fontsize
            self.fontObj = pygame.font.Font(self.fontPath, self.fontSize)
            self.lineheight = self.fontObj.get_height()           
    
    def label_write(self, message = 'OK'):
        """
        Render text to the label surface
        """
        self.label_img = self.fontObj.render(message, False, self.fontColor, self.bgColor)
            
    def rollover(self, mouse_pos):
        """
        Takes a rect of mouse object and returns true if within self.rect
        """
        tmpRect = pygame.Rect(mouse_pos,(1,1))
        if self.rect.contains(tmpRect):
            if self.state != "HOVER":
                self.state = "HOVER"
                self.addError("Hover!")
                self.render()
                return True
            else:
                # already hovering no need to update
                pass
        else:
            if self.state == "HOVER":
                self.state = "UP"
                self.addError("UP!")
                self.render()    
                return False
            else:
                self.state = "UP"
    
    def click(self, pass_button):
        """
        Default method to call if mouse is clicked and over the button.
        """
        if self.buttonType == "CLICK":
            if pass_button == 1:
                self.state = "DOWN"
                self.addError("DOWN!")
                self.render()
    
    def release(self, pass_button):
        """ 
        Default method to call if mouse is clicked and over the button.
        """
        if self.buttonType == "CLICK":
            if pass_button == 1:
                if self.state == "DOWN":
                    self.state = "UP"
                    self.addError("RELEASE!")
                    self.render()
                
    def draw(self, surface):
        """
        blit contents of self image onto surface, adds cursor if image is 'selected'
        """
        if self.visible == True:
            surface.blit(self.img, self.rect)
            
    def erase(self, surface, background):
        """
        blit the background onto the surface over the object's rect.
        """
        surface.blit(background, self.rect, self.rect)
        
    def hide(self):
        self.visible = FALSE
        
    def render(self):
        """
        procedurally generate a basic button and renders it to self.img
        only call this if the button changes state (including rollover)
        """
        # Background
        if self.state == "DOWN":
            self.img.fill(self.clickColor)
        elif self.state == "HOVER":
            self.img.fill(self.bgColor)
        else:
            self.img.fill(self.bgColor)
        # render text label, calculate center, and blit to coords on img rect
        text_loc = (self.rect.center[0] - (self.rect.width/2), self.rect.center[1] - (self.lineheight / 2))
        
        self.label_write(self.text)
        self.img.blit(self.label, text_loc)
        
        # add border line
        # Define pointlists containing the corners of the cursor's lines
        button_border = [self.rect.topleft,
                    self.rect.topright,
                    self.rect.bottomright,
                    self.rect.bottomleft]
        pygame.draw.lines(self.img, self.borderColor, True, button_border, self.borderWidth)
        tempMsg = "Button #" + str(self.id) + "rendered!"
        self.addError(tempMsg)
        del tempMsg
        self.dirty = True
        
    def isDirty(self):
        return self.dirty
        
    def getErrors(self):
        temp_queue = self.errorQueue
        self.errorQueue=[]
        self.isError = False
        return temp_queue
        
    def addError(self, temp_msg=""):
        self.errorQueue.append(str(temp_msg))
        self.isError = True