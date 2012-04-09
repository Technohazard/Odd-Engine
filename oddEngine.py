import sys
import pygame
from pygame.locals import *

# Game Clock + timing
import time

# Sprite / game object container
from myCat import cMyCat

# Mouse cursor and interface layer
from myMouse import cMyMouse

# Debug console module
from myDebug import cMyDebug

# Game data and constants
from gameStuff import *

# Color definitions and helper class
import myColors

#Setup debug console object 
debug_console = cMyDebug()  #creates a new instance of the class and
                #assigns this object to the local variable x.
tempMsg = "OddDebug Console "+ debug_console.getVersion() +" Active!"
debug_console.addMessage([tempMsg])
del tempMsg

# sets up a mouse manager object
mouseMgr = cMyMouse() 
colorObj = myColors.colorHelper()

## Feminist Trail
## Version 0.1
## Author: Justin Smith
## Email: odd_dimensions@gmail.com

from gameConstants import *

# define game colors, menu colors, etc.
BGCOLOR = colorObj.BLACK

pygame.init()

## Game metadata class + object
game = gameData()

#Setup Game Clock
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

## Setup Display surface and convert to alpha
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,32)
#MAINSURF = MAINSURF.convert_alpha()

pygame.display.set_caption(game.getDisplayCaption())

#setup game fonts

fontObj_diehld = pygame.font.Font('./fonts/DIEHLD__.ttf', 32)
textSurfaceObj_2 = fontObj_diehld.render('New Font!', True, colorObj.RED, colorObj.BLACK)
textRectObj_2 = textSurfaceObj_2.get_rect()
textRectObj_2.center = (150, 100)

#Load Sound Objects
soundObj = pygame.mixer.Sound('./sfx/beeps.wav')

# Loading and playing background music:
pygame.mixer.music.load('./music/07 - F6 Gs (Lost Area).mp3')
                        
#Fill window with background color
screen.fill(BGCOLOR)

#start playing music
pygame.mixer.music.play(-1, 0.0)

#setup game objects
   
#make a list of cats
cats = []
cats.append(cMyCat(init_pos=(100, 100), init_speed=[1, 0], init_id = 0))
cats.append(cMyCat(init_pos=(200, 100), init_speed=[0, 1], init_id = 1))
cats.append(cMyCat(init_pos=(200, 200), init_speed=[-1, 0], init_id = 2))
cats.append(cMyCat(init_pos=(100, 200), init_speed=[0, -1], init_id = 3))
selected_cat = 0 

targetlist = [pygame.Rect(100, 100, 10, 10),
              pygame.Rect(200, 100, 10, 10),
              pygame.Rect(200, 200, 10, 10),
              pygame.Rect(100, 200, 10, 10)]

for cat in cats:
        if cat.load_img('./img/cat.png'):
                pass
        else:
                tempMsg=cat.getErrors()
                debug_console.addMessage(tempMsg)
                del tempMsg

cats[0].set_target(targetlist[1])
cats[1].set_target(targetlist[2])
cats[2].set_target(targetlist[3])
cats[3].set_target(targetlist[0])
		  
#main game loop
while game.isRunning(): 
    # Update all cats
    for i, cat in enumerate(cats):
        if cat.update(screen):
                if i == selected_cat:
                    cat.draw_select(screen)
        else:
                #collect errors from cat moves
                tempMsg = cat.getErrors()
                debug_console.addMessage(tempMsg)
                del tempMsg                        

    #display debug console main try loop
    if debug_console.isActive():
            #collect messages from appropriate objects and dump to debug queue
                    if debug_console.isVisible():
                            if debug_console.draw(screen):
                                    pass
                            else:
                                    print ("Debug Draw failed, autohiding ")
                                    debug_console.hideConsole()
                            
    #except (RuntimeError, TypeError, NameError):
    #        debug_console.addMessage(["Debug Console Couldn't Display!"])
     #       pygame.quit()
      #      game.halt()
               
    # main event handler loop
    for event in pygame.event.get():
            if (event.type == QUIT):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    game.halt()
            elif (event.type == KEYDOWN):
                    _ = pygame.key.name(event.key)
                    #render keypressed to text
            elif (event.type == KEYUP): 
                    if (event.key == K_m): #Fade out / restart music toggle
                        if pygame.mixer.music.get_busy() == True:
                            tempMsg="Music Paused!"
                            debug_console.addMessage([tempMsg])
                            pygame.mixer.music.fadeout(3)
                            del tempMsg
                        else:
                            tempMsg="Music Restarted!"
                            debug_console.addMessage([tempMsg])
                            pygame.mixer.music.play(-1, 0.0)
                            del tempMsg
                    if (event.key == K_d): # Debug Toggle
                        if debug_console.isVisible():
                            tempMsg="Console Hidden."
                            debug_console.addMessage([tempMsg])
                            debug_console.hideConsole()
                            del tempMsg
                        else:
                            tempMsg="Console Shown."
                            debug_console.addMessage([tempMsg])
                            debug_console.showConsole()
                            del tempMsg
                    if (event.key == K_a): # Add debug Msg.
                            tempMsg="Test!"
                            debug_console.addMessage([tempMsg])
                            del tempMsg
                    if (event.key == K_p): # Pause
                            if game.pause():
                                    tempMsg="Game Paused..."
                                    debug_console.addMessage([tempMsg])
                                    del tempMsg
                            else:
                                    tempMsg="Game Resumed."
                                    debug_console.addMessage([tempMsg])
                                    del tempMsg
                    if (event.key == K_1): # Cat Target 1
                            for cat in cats:
                                    if cat.set_target(targetlist[0]):
                                            pass
                            debug_console.addMessage(["Cats Targeted: 1"])
                    if (event.key == K_2): # Cat Target 2
                            for cat in cats:
                                    if cat.set_target(targetlist[1]):
                                            pass
                            debug_console.addMessage(["Cats Targeted: 2"])
                    if (event.key == K_3): # Cat Target 3
                            for cat in cats:
                                    if cat.set_target(targetlist[2]):
                                            pass
                            debug_console.addMessage(["Cats Targeted: 3"])
                    if (event.key == K_4): # Cat Target 4
                            for cat in cats:
                                    if cat.set_target(targetlist[3]):
                                            pass
                            debug_console.addMessage(["Cats Targeted: 4"])
                    # quit the game
                    if (event.key == K_ESCAPE):
                            debug_console.addMessage(["Game Halting..."])
                            game.halt()
                    if event.key == K_LEFT:
                            cats[selected_cat].set_speed([cats[selected_cat].speed[0] - 1, cats[selected_cat].speed[1]])
                    if event.key == K_RIGHT:
                            cats[selected_cat].set_speed([cats[selected_cat].speed[0] + 1, cats[selected_cat].speed[1]])
                    if event.key == K_UP:
                            cats[selected_cat].set_speed([cats[selected_cat].speed[0], cats[selected_cat].speed[1] - 1])
                    if event.key == K_DOWN:
                            cats[selected_cat].set_speed([cats[selected_cat].speed[0], cats[selected_cat].speed[1] + 1])
                    if event.key == K_t:
                            if selected_cat < len(cats):
                                    selected_cat += 1
                                    tempMsg = "Cat #" + str(selected_cat) + " selected"
                                    debug_console.addMessage([tempMsg])
                                    del tempMsg
                            else:
                                    selected_cat = 0
            elif (event.type == MOUSEMOTION):
                    mouseMgr.set_pos(event.pos)
            elif (event.type == MOUSEBUTTONUP):
                    mouseMgr.set_pos(event.pos)
                    mouseMgr.set_clicked(True)
              
    pygame.display.flip()
    fpsClock.tick(FPS)
#End main while loop

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
