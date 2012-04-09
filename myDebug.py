import myColors
import pygame
from gameStuff import *

from pydoc import help

class cMyDebug():
    """
    Creates a debug window and message handling/storage framework for program control and realtime variable tweaking.
    """
    def __init__(self, init_active = True, init_visible = False, init_pos = (0,0), init_size = (400,300)):
        self.active = init_active        #is window currently updating?
        self.visible = init_visible    #is window rendering/displaying?
        self.version = '0.1'
        
        self.rect = pygame.Rect(init_pos,init_size) # define window render size
        self.window_width = int(WINDOW_WIDTH * 0.5) #
        self.dirty = False
    
        self.colorObj = myColors.colorHelper()
        self.messageQueue = ["myDebug v0.1:"] #initialize a message queue for active display

        self.viewLines = 10 # number of messages to display in the debug window
        self.viewRange = (0,self.viewLines)    # keep track of which messages we are displaying.

        # set some default appearance values
        self.font_dir = "./fonts/"
        self.font_file = "coders_crux.ttf"
        self.font_path = str(self.font_dir + self.font_file)
        self.font_size = 32 
        self.bgColor = self.colorObj.DEBUG_BG_COLOR
        self.fontColor = self.colorObj.DEBUG_FONT_COLOR
        self.maxMessageLimit = 10000 # for debug purposes, don't accept messages
        
        pygame.font.init()
        self.fontObj = pygame.font.Font(self.font_path, self.font_size)
        self.lineheight = self.fontObj.get_height()
        
    def isActive(self):
        return self.active

    def isVisible(self):
        return self.visible
        
    def hideConsole(self):
        self.visible = False
    
    def showConsole(self):
        if self.active == False:
            self.active = True
        self.visible = True     
    
    def addMessage(self, temp_message=[""]):
        """
        adds list of passed messages to debug output message queue    
        """
        for temp in temp_message:
            print ("Adding Message: " + str(temp))
            if len(self.messageQueue) < self.maxMessageLimit:
                self.messageQueue.append(temp)
                if len(self.messageQueue) > self.viewLines:
                    self.scroll(1)
            else:
                print("Couldn't add any more debug messages: queue full")

    def font_load(self, init_fontpath = "./", init_fontSize = 32):
        """
        Load a new local font object and determine font line height by size.
        """
        if init_fontpath != self.fontpath:
            self.fontpath = init_fontpath
            self.fontsize = init_fontsize
            self.fontObj = pygame.font.Font(self.fontPath, self.fontSize)
            self.lineheight = self.fontObj.get_height()           
    
    def font_write(self, message="?"):
        """
        Render text to a PyGame Surface and a rect, then returns them
        """
        surfObj = self.fontObj.render(message, False, self.fontColor, self.bgColor)
        rectObj = surfObj.get_rect()
        
        if isinstance(surfObj, pygame.Surface):
            return [surfObj,rectObj]
        
    def draw(self, surface):
        """
        Traverse message queue over the range and create a render array of surfaces containing rendered message contents.
        """
        #create temp slice list based on view range and append resultant rendered surfaces to renderarray
        self.renderMessages(self.viewRange)
        surface.blit(self.surfaceObj, self.rectObj)
        return True
    
    def erase(self, surface):
        surface.blit(self.bg, self.rect)
        return True
        
        
    def renderMessages(self, view_range=(0,25)):
        #renders list of messages onto a single surface and returns True if successful
        # view_range is a tuple (0,25) that tells the function which messages to pull
        renderarray = []
        temp_n = 0
        for message in self.messageQueue[view_range[0]:view_range[1]]:
            tempMsg = str(temp_n) + ": " + message
            renderarray.append(self.font_write(tempMsg))
            temp_n += 1
            del tempMsg
        self.rect = pygame.Rect((0,0),(self.window_width, len(renderarray) * self.lineheight)) # Define final render window size
        self.surfaceObj = pygame.Surface((self.rect.width, self.rect.height))     # initialize final render surface
        
        #move each rectangle into the proper location by (message index * lineheight), then blit
        for i, surf in enumerate(renderarray): 
            surf[1].move_ip(0, i*self.lineheight)
            self.surfaceObj.blit(surf[0],surf[1])
        
        self.rectObj = self.surfaceObj.get_rect()
        if isinstance(self.surfaceObj, pygame.Surface):
            return True
        else:
            print ("Debug Console surface creation failed in renderMessages()")
            self.hideConsole()
            return False
        
    def updateLastKeyPress(self, keypress):
        self.lastKeyPressed = keypress
        
    def scroll(self, n = 1):
            self.viewRange = (self.viewRange[0]+1,self.viewRange[1]+1)
            tempStr = str(self.viewRange[0]) + ":" +str(self.viewRange[1])
            print("scrolling..." + tempStr)
            return True
            
    def isDirty(self):
        return self.dirty
        
    def getVersion(self):
        return self.version