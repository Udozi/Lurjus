import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, time 
from pygame.locals import *

class PaaValikko(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kuvat/menuTausta.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        
    def piirra(self, tausta):
        tausta.blit(self.image, self.rect)

class NappiKampanja(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kuvat/menuKampanja.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 225)
        
    def piirra(self, tausta):
        tausta.blit(self.image, self.rect)
        
class NappiPikapeli(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kuvat/menuPikapeli.png")
        self.rect = self.image.get_rect()
        self.rect.center = (600, 225)
        
    def piirra(self, tausta):
        tausta.blit(self.image, self.rect)

class NappiTutoriaali(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kuvat/menuTutoriaali.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 375)
        
    def piirra(self, tausta):
        tausta.blit(self.image, self.rect)
        
class NappiTekijat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kuvat/menuTekijat.png")
        self.rect = self.image.get_rect()
        self.rect.center = (600, 375)
        
    def piirra(self, tausta):
        tausta.blit(self.image, self.rect)
        
class NappiLopeta(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kuvat/menuLopeta.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 525)
        
    def piirra(self, tausta):
        tausta.blit(self.image, self.rect)
        
class Nappi(pygame.sprite.Sprite):
    toiminto = ""

    def __init__(self, toiminto):
        super().__init__()
        self.toiminto = toiminto
        match toiminto:
            case "etene": self.image = pygame.image.load("kuvat/etene_nappi.png")
            case "pakene": self.image = pygame.image.load("kuvat/pakene_nappi.png")
        self.rect = self.image.get_rect()

    def piirrä(self, pohja):
        pohja.blit(self.image, self.rect)

class Teksti(pygame.sprite.Sprite):
    teksti = ""
    def __init__(self):
        super().__init__()
        self.text = pygame.font.Font("freesansbold.ttf", 16).render("Tehtävänäsi on päihittää ilkeä", True, (0, 0, 0), (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = (120, 60)

    def päivitä_teksti(self, teksti):
        self.text = pygame.font.Font("freesansbold.ttf", 16).render(teksti, True, (255, 255, 255), (0, 0, 0))

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
