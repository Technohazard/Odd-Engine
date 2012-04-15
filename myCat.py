import sys
import pygame
import myColors
from gameStuff import *

class cMyCat():
    def __init__(self, init_pos = (0, 0), init_speed = [0, 0], init_id = 0):
        self.id = init_id
        
        self.rect = pygame.Rect(init_pos, (10,10))
        self.target = self.rect
        
        self.img = pygame.Surface((10,10))
        self.bg = pygame.Surface(self.img.get_size())             
        
        # convert both to alpha
        self.img.convert_alpha()
        self.bg.convert_alpha()    
            
        # by default the bounding rect is as big as the window
        self.bounding = SCREEN_RECT
        self.speed = init_speed
        self.img_path = "./" 
        self.cursor = None
        
        # Obj color settings
        self.colorObj = myColors.colorHelper()
        
        # Set transparent color to global default
        self.transColor = self.colorObj.getColor("TRANSPARENT") 
        
        # Obj Error queue and reporting
        self.errorQueue=[]
        self.errorQueue.append("Initialized object Id:" + str(self.id) + " @" + str(self.rect))
        self.isError = True # set this if the error queue contains messages. This should pass init msgs

        self.broken = False # If the object does something silly or bad, set the broken flag!
        
        self.imageloaded = False # no image is loaded into an object by default
        self.movespeed = 1 # default movespeed is one for all objects (rounded up from zero)
        self.selected = False # display selection cursor around object
        
    def load_img(self, init_img_path="./"):
        # fill both surfaces with the transparent color
        if init_img_path != self.img_path:  #only reload the image if it's different than original.
            self.img_path = init_img_path
            
            try:
                self.img = pygame.image.load(self.img_path)
            except IOError:
                tempMsg = "load_img(" + str(self.img_path) + ") image load failed"
                self.errorQueue.append(tempMsg)
                self.isError = True
                del tempMsg
            
            # set the color key
            self.img.set_colorkey(self.transColor)
            
            # create rectangle for the image
            self.rect.width = self.img.get_rect().width
            self.rect.height = self.img.get_rect().height
            
            # check that everything is initialized and set flags
            if isinstance(self.img, pygame.Surface):
                if isinstance(self.rect, pygame.Rect):
                    self.imageloaded = True
                else:
                    tempMsg = "Error - load_img() didn't create a valid surf / rect combo for id:" + self.id +" path: " + self.img_path
                    self.errorQueue.append(tempMsg)
                    self.isError = True
                    del tempMsg
                    return False # FAIL!!!
        else:
            tempMsg= "Image same as previous, not reloaded: " + self.img_path
            self.errorQueue.append(tempMsg)
            self.isError = True
            del tempMsg
        if self.imageloaded == True:
            return True
	
    def update(self, surface, background):
            self.erase(surface, background)
            self.move()
            self.draw(surface)
            
    def move(self, bounding_rect = None):
        """
        Moves the cMyCat object according to self.speed
        Takes a pygame.Rect() objects in parameters.
        """
        if bounding_rect != None:
            if not isinstance(bounding_rect, pygame.Rect):
                tempMsg = "id#" +self.id + " move(): Invalid type for bounding_rect parameter!"
                self.addError(tempMsg)
                self.isError = True
                del tempMsg
                self.bounding = self.rect
            elif (bounding_rect != self.bounding):
                self.bounding = bounding_rect
        
        if not isinstance(self.bounding, pygame.Rect):
            self.bounding = pygame.Rect(SCREEN_RECT)
            
        # Once we have done sanity checking, move the Obj
        self.rect.move_ip(self.speed[0], self.speed[1])
        if self.limit_check(self.bounding, True) == True:
            pass
        else:
            tempMsg = "move(): " + str(self.id) + " bounced!"
            self.addError(tempMsg)
            self.isError = True
            del tempMsg
    
    def erase(self, surface, background):
        """
        blit the background onto the surface over the object's rect.
        """
        surface.blit(background, self.rect, self.rect)

    def draw(self, surface):
        """
        blit contents of self image onto surface, adds cursor if image is 'selected'
        """
        surface.blit(self.img, self.rect)
        if self.selected == True:
            self.draw_select(surface)
                
    def get_img():
        """
        Returns the most recent draw image.
        """
        return self.img

    def get_pos():
        return self.rect

    def set_pos(init_pos = (0,0)):
        self_rect.topleft = (init_pos)
        return true

    def set_speed(self, new_speed):
        self.speed = new_speed
    
    def set_target(self, targ_rect, change_speed = True):
        """
        Accepts valid bounding rectangle and returns True if target successfully updates.
        """
        if isinstance(targ_rect, pygame.Rect):
            self.target = targ_rect
            if change_speed == True:
                #get new speed based on a line between self.rect and self.target centers, divided into movespeed increments
                tempctr = self.rect.center
                temptrgctr = self.target.center
                
                newspeed = [0,0]
                self.set_speed(newspeed)
                del newspeed
            return True
        else:
            tempMsg = "failed set_target(): Invalid type for target_rect parameter!\n"
            self.addError(tempMsg)
            self.isError = True
            del tempMsg
            self.target = self.rect
            return False
        
    def getErrors(self):
        temp_queue = self.errorQueue
        self.errorQueue=[]
        return temp_queue
        
    def addError(self, temp_msg=""):
        self.errorQueue.append(str(temp_msg))        
        
    def limit_check(self, bounding_rect, bounce = True):
        if bounding_rect.contains(self.rect):
            return True # Obj is within bounds
        else: # if the Obj is outside of bounding_rect
            if self.rect.top < bounding_rect.top: 
                self.rect.top = bounding_rect.top
                if bounce == True:
                    if (self.rect.top + self.speed[1]) < bounding_rect.top:
                        self.speed[1] *= -1
                return False # bounced out of bounding_rect
            elif self.rect.bottom > bounding_rect.bottom:
                # likewise for bottom side
                self.rect.bottom = bounding_rect.bottom
                if bounce == True:
                    if (self.rect.bottom + self.speed[1]) > bounding_rect.bottom:
                        self.speed[1] *= -1
                return False # bounced out of bounding_rect
            # now, we do the same for the left & right side
            if self.rect.left < bounding_rect.left: 
                self.rect.left = bounding_rect.left
                if bounce == True:
                    if (self.rect.left + self.speed[0]) < bounding_rect.left:
                        self.speed[0] *= -1
                return False # bounced out of bounding_rect
            elif self.rect.right > bounding_rect.right:
                self.rect.right = bounding_rect.right
                if bounce == True:
                    if (self.rect.right + self.speed[0]) > bounding_rect.right:
                        self.speed[0] *= -1
                return False # bounced out of bounding_rect
    
    def calcnewpos(self, rect, vector):
        """
        Takes a vector and returns a rect with the Obj's next projected position
        """
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)
    
    def draw_select(self, surface, line_width = 2, line_color = "CURSOR_COLOR"):
        """
        draws a cursor based on self.rect onto target surface
        """
        if not isinstance(self.cursor, pygame.Surface):
            #Create a cursor surface+rect combo
            self.cursor = pygame.Surface((self.rect.width + line_width, self.rect.height + line_width))
            self.cursor.convert_alpha()
            self.cursor.set_colorkey(self.transColor)
            self.cursor.fill(self.transColor)
            
            temp_rect = self.rect
            
            # Define pointlists containing the corners of the cursor's lines
            top_left = [(temp_rect.left, temp_rect.top + (temp_rect.height * 0.20)),
                        temp_rect.topleft,
                        ((temp_rect.left + (temp_rect.width * 0.20), temp_rect.top))]
            top_right = [(temp_rect.right - (temp_rect.width * 0.20), temp_rect.top),
                        temp_rect.topright,
                        (temp_rect.right, temp_rect.top + (temp_rect.height * 0.20))]
            bottom_left = [(temp_rect.left, temp_rect.bottom - (temp_rect.height * 0.20)),
                        temp_rect.bottomleft,
                        ((temp_rect.left + (temp_rect.width * 0.20), temp_rect.bottom))]
            bottom_right = [(temp_rect.right, temp_rect.bottom - (temp_rect.height * 0.20)),
                        temp_rect.bottomright,
                        ((temp_rect.right - (temp_rect.width * 0.20), temp_rect.bottom))]
                        
            # recreate the line_color parameter into a pygame.color object
            line_color = self.colorObj.getColor(line_color)
            
            # draw cursor lines onto the temp surface
            pygame.draw.lines(self.cursor, line_color, False, top_left, line_width)
            pygame.draw.lines(self.cursor, line_color, False, top_right, line_width)
            pygame.draw.lines(self.cursor, line_color, False, bottom_left, line_width)
            pygame.draw.lines(self.cursor, line_color, False, bottom_right, line_width)
        surface.blit(self.cursor, self.rect, self.rect)
        
    def select(self):
        self.selected = True
    
    def unselect(self):
        self.selected = False
        
    def get_rect(self):
        return self.rect