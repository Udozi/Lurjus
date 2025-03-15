import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, time 
from pygame.locals import *

VALKOINEN = (255, 255, 255)
PUNAINEN = (255, 0, 0)
MUSTA = (0, 0, 0)

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

    def __init__(self, toiminto):
        super().__init__()
        self.toiminto = toiminto
        latausnimi = "kuvat/napit/" + toiminto + "_nappi.png"
        self.image = pygame.image.load(latausnimi)
        self.rect = self.image.get_rect()
        
    def päivitä_kuva(self, nimi):
        latausnimi = "kuvat/napit/" + str(nimi) + "_nappi.png"
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
        self.text = pygame.font.Font("freesansbold.ttf", 16).render("Tehtävänäsi on päihittää ilkeä", True, (0, 0, 0), (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = (120, 60)

    def päivitä_teksti(self, teksti, fonttikoko = 16, väri = VALKOINEN, fontti = "freesansbold.ttf"):
        self.text = pygame.font.SysFont(fontti, fonttikoko).render(teksti, False, väri)

    def piirrä(self, surface):
        surface.blit(self.text, self.rect)
        
class Pisteet(pygame.sprite.Sprite):
    teksti = ""
    def __init__(self):
        super().__init__()
        self.text = pygame.font.Font("freesansbold.ttf", 40).render("Tehtävänäsi on päihittää ilkeä", True, (0, 0, 0), (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = (120, 60)

    def päivitä_teksti(self, teksti):
        self.text = pygame.font.Font("freesansbold.ttf", 40).render(teksti, True, (255, 255, 255), (0, 0, 0))

    def piirrä(self, surface):
        surface.blit(self.text, self.rect)            
