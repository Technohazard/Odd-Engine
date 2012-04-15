import sys
import pygame
from pygame.locals import *

pygame.init()

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

# Game music tracklist, mixer
import myMusic

# Loading and playing background music:
musicObj = myMusic.gameMusicHelper()
musicObj.loadTrack('./music/07 - F6 Gs (Lost Area).mp3')

#start playing music
musicObj.play()

# Game SFX mixer
import mySound

soundObj = mySound.gameSoundHelper()
soundObj.load('./sfx/cat_meow_01.ogg')
soundObj.load("./sfx/cat_meow_02.wav")
soundObj.load("./sfx/cat_meow_03.wav")

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

## Game metadata class + object
game = gameData()

#Setup Game Clock
FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

## Setup Display surface, background, and convert to alpha
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0,32)
screen.convert_alpha()
screen.fill(colorObj.BGCOLOR) # fill with background color
pygame.display.set_caption(game.getDisplayCaption()) # Title Window

import myBackground

backgroundObj = myBackground.cMyBG([('./img/cat_paradise_800x600.png', 0),
                                    ('./img/cloud_scroll_bg_800x600.png', 1)])
backgroundObj.draw()
background = backgroundObj.get_img()
displayBG = False

# Font Drawing test object
fontObj_diehld = pygame.font.Font('./fonts/DIEHLD__.ttf', 32)
textSurfaceObj_2 = fontObj_diehld.render('New Font!', True, colorObj.RED, colorObj.BLACK)
textRectObj_2 = textSurfaceObj_2.get_rect()
textRectObj_2.center = (150, 100)

# Setup game objects
   
# Make a list of game objects
cats = []
cats.append(cMyCat((200, 200), [1, 0], 0))
cats.append(cMyCat((500, 200), [0, 1], 1))
cats.append(cMyCat((500, 400), [-1, 0], 2))
cats.append(cMyCat((200, 400), [0, -1], 3))
selected_cat = 0 

# Make a list of Targets
targetlist = [pygame.Rect(100, 100, 10, 10),
              pygame.Rect(700, 100, 10, 10),
              pygame.Rect(700, 700, 10, 10),
              pygame.Rect(100, 700, 10, 10)]

# Load cat images - all the same for now.
for cat in cats:
        if cat.load_img('./img/cat_01.png'):
                pass
        else:
                debug_console.addMessage(cat.getErrors())

# cats[0].set_target(targetlist[1])
# cats[1].set_target(targetlist[2])
# cats[2].set_target(targetlist[3])
# cats[3].set_target(targetlist[0])
		  
# Core game loop
while game.isRunning(): 

    # update backgrounds
    # Each background is independently updated, which animates / draws / it as necessary
    # draw() renders all backgrounds onto a single Surface
    if displayBG == True:
            backgroundObj.update()
            if backgroundObj.isDirty():
                    backgroundObj.draw(background)
                    screen.blit(background, SCREEN_RECT, SCREEN_RECT)
            
    # Update all cats
    for cat in cats:
        cat.erase(screen, background)
        cat.move()

    for cat in cats:
        cat.draw(screen)

        # Collect errors from cat moves
        if cat.isError == True:
                debug_console.addMessage(cat.getErrors())

    # Display debug console main try loop
    if debug_console.isActive():
            # Collect messages from appropriate objects and dump to debug queue
                    if debug_console.isVisible():
                            if debug_console.draw(screen):
                                    pass
                            else:
                                    print ("Debug Draw failed, autohiding ")
                                    debug_console.hideConsole()
                                    debug_console.erase(screen, background)
                            
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
                            musicObj.fadeOut(3)
                            del tempMsg
                        else:
                            tempMsg="Music Restarted!"
                            debug_console.addMessage([tempMsg])
                            musicObj.play()
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
                            tempMsg="Mouse: " + str(mouseMgr.get_pos())
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
                            cats[selected_cat].unselect()
                            if selected_cat < (len(cats)-1):
                                    selected_cat += 1
                            else:
                                    selected_cat = 0
                            tempMsg = "Cat #" + str(selected_cat) + " selected"
                            cats[selected_cat].select()
                            debug_console.addMessage([tempMsg])
                            del tempMsg
                    if event.key == K_b:
                        if displayBG == True:
                            tempMsg = "Background Off"
                            debug_console.addMessage([tempMsg])
                            displayBG = False
                            del tempMsg
                        else:
                            tempMsg = "Background On"
                            debug_console.addMessage([tempMsg])
                            displayBG = True
                            del tempMsg
                    if event.key == K_c:
                        tempMsg = "Cat#" + str(selected_cat) + ": " + str(cats[selected_cat].get_rect())
                        screen.blit(cats[selected_cat].img, mouseMgr.get_pos())
                        debug_console.addMessage([tempMsg])

            elif (event.type == MOUSEMOTION):
                    mouseMgr.set_pos(event.pos)
            elif (event.type == MOUSEBUTTONUP):
                    mouseMgr.set_pos(event.pos)
                    mouseMgr.set_clicked(True)
              
    pygame.display.update()
    fpsClock.tick(FPS)
#End main while loop

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
