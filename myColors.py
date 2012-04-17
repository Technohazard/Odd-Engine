import pygame

class colorHelper():
    """
    Defines Color values as a dictionary of Pygame Color objects and provides methods for various
    fun color stuff.
    """
    colorDict = {'WHITE': pygame.Color(255, 255, 255, 255),
                    'BLACK': pygame.Color(0, 0, 0, 255),
                    'LIME': pygame.Color(0, 255, 0, 255),
                    'GREEN': pygame.Color(0, 128, 0, 255),
                    'DARK_GREEN': pygame.Color(0, 64, 0, 255),
                    'RED': pygame.Color(255, 0, 0, 255),
                    'MAROON': pygame.Color(128, 0, 0, 255),
                    'BLUE': pygame.Color(0, 0, 255, 255),
                    'NAVYBLUE': pygame.Color(0, 0, 128, 255),
                    'GRAY': pygame.Color(128, 128, 128, 255),
                    'SILVER': pygame.Color(192, 192, 192, 255),
                    'FUCHSIA': pygame.Color(255, 0, 255, 255),
                    'OLIVE': pygame.Color(128, 128, 0, 255),
                    'PURPLE': pygame.Color(128, 0, 128, 255),
                    'TEAL': pygame.Color(0, 128, 128, 255),
                    'YELLOW': pygame.Color(255, 255, 0, 255),
                    'TRANSPARENT': pygame.Color(255, 0, 255, 255),
                    'CURSOR_COLOR': pygame.Color(255, 255, 0, 128),
                    'DEBUG_FONT_COLOR': pygame.Color(0, 255, 0, 255),
                    'DEBUG_BG_COLOR': pygame.Color(0, 64, 0, 64),
                    'BGCOLOR': pygame.Color(0, 0, 0, 255),
                    'BUTTON_BG_COLOR': pygame.Color("#8F2471"),
                    'BUTTON_FONT_COLOR': pygame.Color("#DF64BD"),
                    'BUTTON_BORDER_COLOR': pygame.Color("#DF38B1"),
                    'BUTTON_CLICK_COLOR': pygame.Color("#BE008A"),
                    'BUTTON_SHADOW_COLOR': pygame.Color("#7C005A")
                    }
                    
    WHITE = colorDict['WHITE']
    BLACK = colorDict['BLACK']
    LIME = colorDict['LIME']
    GREEN = colorDict['GREEN']
    RED = colorDict['RED']
    MAROON = colorDict['MAROON']
    BLUE = colorDict['BLUE']
    NAVYBLUE = colorDict['NAVYBLUE']    
    GRAY = colorDict['GRAY']
    SILVER = colorDict['SILVER']    
    FUCHSIA = colorDict['FUCHSIA']
    OLIVE = colorDict['OLIVE']
    PURPLE = colorDict['PURPLE']
    TEAL = colorDict['TEAL']
    YELLOW = colorDict['YELLOW']
    
    DEBUG_FONT_COLOR = colorDict['DEBUG_FONT_COLOR'] # Lime @ 100% alpha
    DEBUG_BG_COLOR = colorDict['DEBUG_BG_COLOR'] # Dark Green @ 25% alpha
    
    CURSOR_COLOR = colorDict['CURSOR_COLOR'] # Yellow @ 50% alpha
    
    BGCOLOR = colorDict['BLACK'] # Black Background
    
    # Define Fuschia as the default transparent color
    TRANSPARENT = FUCHSIA

    # Button colors
    BUTTON_BG_COLOR = colorDict['BUTTON_BG_COLOR']
    BUTTON_FONT_COLOR = colorDict['BUTTON_FONT_COLOR']
    BUTTON_BORDER_COLOR = colorDict['BUTTON_BORDER_COLOR']
    BUTTON_CLICK_COLOR = colorDict['BUTTON_CLICK_COLOR']
    BUTTON_SHADOW_COLOR = colorDict['BUTTON_SHADOW_COLOR']
    
    def getColor(self, cname="BLACK"):
        """
        Lookup color name in internal dictionary and return appropreate pygame color object
        """
        return self.colorDict[cname]