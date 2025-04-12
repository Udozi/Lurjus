import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, time 
from pygame.locals import *
pygame.font.init()

VALKOINEN = (255, 255, 255)
PUNAINEN = (255, 0, 0)
MUSTA = (0, 0, 0)

korttiFontti = pygame.font.SysFont("Dubai", 36, bold=True)

class Taustakuva(pygame.sprite.Sprite):
    def __init__(self, nimi = "placeholder"):
        super().__init__()
        latausnimi = "kuvat/" + nimi + ".png"
        self.image = pygame.image.load(latausnimi)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        
    def piirrä(self, tausta):
        tausta.blit(self.image, self.rect)
        
class Nappi(pygame.sprite.Sprite):
    toiminto = ""

    def __init__(self, toiminto, näkyvä = True):
        super().__init__()
        self.toiminto = toiminto
        
        if näkyvä:           
            latausnimi = "kuvat/napit/" + toiminto + "_nappi.png"
            self.image = pygame.image.load(latausnimi).convert_alpha()
            self.rect = self.image.get_rect()
        
    def päivitä_kuva(self, nimi):
        latausnimi = "kuvat/napit/" + str(nimi) + "_nappi.png"
        self.image = pygame.image.load(latausnimi)
        self.rect = self.image.get_rect()

    def piirrä(self, pohja, xpos = None, ypos = None):
        
        if xpos != None and ypos != None:
            self.rect.center = (xpos, ypos)
        
        pohja.blit(self.image, self.rect)

class Kuva(pygame.sprite.Sprite):
    def __init__(self, nimi):
        super().__init__()
        latausnimi = "kuvat/" + nimi + ".png"
        self.image = pygame.image.load(latausnimi)
        self.rect = self.image.get_rect()
        
    def piirrä(self, pohja, xpos = None, ypos = None):
        
        if xpos != None and ypos != None:
            self.rect.center = (xpos, ypos)
        
        pohja.blit(self.image, self.rect)

class Teksti(pygame.sprite.Sprite):
    teksti = ""
    def __init__(self):
        super().__init__()
        self.text = pygame.font.SysFont("FreeSans", 16).render("Tehtävänäsi on päihittää ilkeä", True, (0, 0, 0), (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = (120, 60)

    def päivitä_teksti(self, teksti, fonttikoko = 16, väri = VALKOINEN, fontti = "freesansbold.ttf", sysfont = True):
        
        if sysfont:
            self.text = pygame.font.SysFont(fontti, fonttikoko).render(teksti, False, väri)
        else:
            self.text = fontti.render(teksti, False, väri)
        self.rect = self.text.get_rect()

    def piirrä(self, surface):
        surface.blit(self.text, self.rect)

class LisävoimaKuvake():
    
    def __init__(self, nimi):
        super().__init__()
        latausnimi = "kuvat/lisävoimat/" + nimi + ".png"
        self.image = pygame.image.load(latausnimi)
        self.rect = self.image.get_rect()
        
    def piirrä(self, pohja, xpos = None, ypos = None):
        
        if xpos != None and ypos != None:
            self.rect.center = (xpos, ypos)
        
        pohja.blit(self.image, self.rect)

class Kehys(pygame.sprite.Sprite):
    def __init__(self, nimi = "kortti"):
        super().__init__()
        self.image = pygame.image.load("kuvat/efektit/hover_" + nimi + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = (120, 60)
        self.nimi = nimi

    def piirrä(self, pohja, xpos, ypos):
        if xpos != None and ypos != None:
            if self.nimi.startswith("valikko"):
                self.rect.center = (xpos, ypos)
            else:
                self.rect.x = xpos
                self.rect.y = ypos
        
        pohja.blit(self.image, self.rect)