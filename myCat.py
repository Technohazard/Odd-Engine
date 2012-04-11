import pygame
import myColors
from gameStuff import *

class cMyCat():
    def __init__(self, init_pos=(0, 0), init_speed=[0, 0], init_id = 0):
        self.id = init_id
        
        self.rect = pygame.Rect(init_pos,(10,10))
        self.target = self.rect
        
        # by default the bounding rect is as big as the window
        self.bounding = pygame.Rect((0,0),(WINDOW_WIDTH, WINDOW_HEIGHT)) 
        self.speed = init_speed
        self.img_path = "./" 
        
        # Obj color settings
        self.colorObj = myColors.colorHelper()
        self.transColor = self.colorObj.getColor("TRANSPARENT") #set transparent color to global default
        
        # Obj Error queue and reporting
        self.errorQueue=[]
        self.errorQueue.append("Initialized object Id:" + str(self.id))
        self.broken = False # If the object does something silly, like throw an exception, set the broken flag!
        self.brokenmessage = "Working!" # store error responses when broken
        self.imageloaded = False # no image is loaded into an object by default
        self.movespeed = 1 # default movespeed is one for all objects (rounded up from zero)
        self.selected = False # display selection cursor around object
        
    def load_img(self, init_img_path="./"):
        # fill both surfaces with the transparent color
        if init_img_path != self.img_path:  #only reload the image if it's different than original.
            self.img_path = init_img_path
            self.img = pygame.image.load(self.img_path)
            self.bg = pygame.Surface(self.img.get_size()) #create a Bg surface with the same dimensions as the loaded image
            self.bg.fill(self.transColor) # fill the background with object's transparent color (inherited from global)
            # set the color key for both surfaces
            self.img.set_colorkey(self.transColor)
            self.bg.set_colorkey(self.transColor)
            # convert both to alpha
            self.img.convert_alpha()
            self.bg.convert_alpha()            
            # create rectangle for the image
            self.rect = self.img.get_rect() # resize rect to match image size
            if isinstance(self.img, pygame.Surface):
                if isinstance(self.rect, pygame.Rect):
                    self.imageloaded = True
                else:
                    tempMsg= "Error - load_img() didn't create a valid surf / rect combo for id:" + self.id +" path: " + self.img_path
                    self.errorQueue.append(tempMsg)
                    del tempMsg
                    return False
        else:
            tempMsg= "Image same as previous, not reloaded: " + self.img_path
            self.errorQueue.append(tempMsg)
            del tempMsg
            return False
        if self.imageloaded == True:
            return True
	
    def update(self, surface):
        if self.broken == False:
            #First, erase the old sprite
            if self.erase(surface):
                pass
            else:
                self.broken = True
                self.brokenmessage = "Erase Failed for id:" + str(self.id)
                self.addError(self.brokenmessage)
                return False # update failed
            if self.move(self.target, surface.get_rect()) == True:
                pass
            else:
                self.brokenmessage = "Move failed for id:" + str(self.id)
                self.addError(self.brokenmessage)
                return False # update failed
            if self.draw(surface):
                pass
                return True # successfully updated
            else:
                self.broken = True
                self.brokenmessage = "Draw failed for id:" + str(self.id)
                self.addError(self.brokenmessage)
                return False # update failed
        else:
            return True # made it out alive! :)
            
    def move(self, target_rect, bounding_rect):
        # Moves the cMyCat object according to self.speed
        # Takes a pygame.Rect() objects in parameters.
        
        #If you don't pass a valid target bounding rect, crash the object.
        if not isinstance(target_rect, pygame.Rect):
            self.brokenmessage = "failed move(): Invalid type for target_rect parameter!\n"
            self.target = self.rect
            return False    # Move function failed! This will flag broken!
            
        if not isinstance(bounding_rect, pygame.Rect):
            self.brokenmessage = "failed move(): Invalid type for bounding_rect parameter!\n"
            self.bounding = self.rect
            return False    # Move function failed! This will flag broken!
        elif (bounding_rect != self.bounding):
            self.bounding = bounding_rect
            
        # once we have done sanity checking, continue with moving the Obj
        self.rect.move_ip(self.speed[0], self.speed[1])
        if self.limit_check(bounding_rect, True) == True:
            pass
        else:
            self.brokenmessage = "failed move(): Invalid type for bounding_rect parameter!\n"
            self.target = self.rect
            return False    # Move function failed! This will flag broken!
        return True # if nothing went wrong!
    
    def erase(self, surface):
        # erase the Ball object from its current location
        surface.blit(self.bg, self.rect)
        return True

    def draw(self, surface):
        surface.blit(self.img, self.rect)
        return True
                
    def get_img():
        return img

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
        #Create a temporary draw surface+rect combo
        temp_surf = pygame.Surface((self.rect.width + line_width, self.rect.height + line_width))
        temp_surf.set_colorkey(self.transColor)
        temp_surf.fill(self.transColor)
        temp_surf.convert_alpha()
        
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
        pygame.draw.lines(temp_surf, line_color, False, top_left, line_width)
        pygame.draw.lines(temp_surf, line_color, False, top_right, line_width)
        pygame.draw.lines(temp_surf, line_color, False, bottom_left, line_width)
        pygame.draw.lines(temp_surf, line_color, False, bottom_right, line_width)
        
        surface.blit(temp_surf, temp_rect)