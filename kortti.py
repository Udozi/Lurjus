import random, pygame 
from ase import *
from grafiikka import *

maat = ["pata","hertta","risti","ruutu"]
arvot = [range(2,14)]

class Kortti():
    onhaamu = False
    maa = "pata"
    arvo = 2

    def luo_kortti(self, maa, arvo, haamu = False):
        self.maa = maa
        self.arvo = arvo
        self.onhaamu = haamu
        return
        
    def nayta(self):
        isomaa = str(self.maa).capitalize()
        korttiInfo = isomaa + " " + str(self.arvo)
        return korttiInfo
        
    def vaikutus(self):
        
        if self.maa == "hertta":
            return self.arvo
        
        elif self.maa == "pata":
            return -self.arvo
        
        elif self.maa == "risti":
            return -self.arvo
        
        else:
            uusiAse = Ase()
            return(uusiAse.poimi(self.arvo))
        
    def __init__(self, määrättyMaa=maa, määrättyArvo=arvo, haamu = False):
        super().__init__()
        self.maa = määrättyMaa
        self.arvo = määrättyArvo
        self.onhaamu = haamu
        self.image = pygame.image.load("kuvat/kortit/kortti_selkä.png")
        self.originalImage = self.image
        self.rect = self.image.get_rect()

    def piirrä(self, pohja):
         
        if not self.onhaamu:
            pohja.blit(self.image, self.rect)    