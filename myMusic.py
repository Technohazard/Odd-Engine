import pygame
from gameStuff import *

class musicTrack():
    def __init__(self, init_path = "./"):
        self.path = init_path
        if pygame.mixer.get_init() != None:
            pygame.mixer.init()
        
class gameMusicHelper():
    def __init__(self):
        pygame.mixer.init()
        self.tracklist=[]
        self.errorlist=[]
   
    def loadTrack(self, load_path):
        try:
            open(load_path)
        except IOError as e:
            print("whoops! track load failed")
            return False
        
        self.tracklist.append(musicTrack(load_path))
        try:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.load(load_path)
        except IOError:
            print("whoops! track load failed")
            
    def play(self, loops = 0, start_time = 0):
        """
        play the next track.
        """
        pygame.mixer.music.play(loops, start_time)
        
    def stop(self):
        """
        stops current track
        """
        pygame.mixer.stop()
        
    def pause(self):
        pygame.mixer.pause
    
    def fadeInto(self, next_track, fade_secs = 3):
        """
        fade out current track and fade in the next track
        """
        pygame.mixer.music.fadeout(fade_secs * 1000)
        self.play(fade_secs)
        
    def fadeOut(self, fade_secs = 3):
        """
        fades out currently playing track
        """
        pygame.mixer.music.fadeout(fade_secs * 1000)
        
    def volume(self, init_vol = 100):
        pygame.mixer.music.set_volume(init_vol)
