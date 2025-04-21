import pygame
import math
from grafiikka import *

class Ase():
    voima = 2
    arvo = voima
    kestavyys = math.inf
    maa = "ruutu"
    teksti = Teksti()
    lisävoimat = []
       
    def kayta(self, hyokkays, koko, bonus = 0):
        self.kestavyys = koko

        vahinko = self.voima + bonus - hyokkays
        
        return(vahinko)
    
    def __init__(self, arvo = 0, lisävoimat = []):
        super().__init__()
        self.image = pygame.image.load("kuvat/kortit/kortti_selkä.png")
        self.originalImage = self.image
        self.rect = self.image.get_rect()
        self.voima = arvo
        self.arvo = self.voima
        self.lisävoimat = lisävoimat
        

    def piirrä(self, pohja):
        self.teksti.päivitä_teksti(str(self.voima),väri=PUNAINEN,fontti=korttiFontti, sysfont = False)
        self.teksti.rect.center = (25, 75)
        self.teksti.piirrä(self.image)
                
        if len(self.lisävoimat) > 0:
            for l in self.lisävoimat:
                
                i = self.lisävoimat.index(l) + 1
                sijY = 75 + i * 40
                
                kuvake = LisävoimaKuvake(l.id) 
                kuvake.piirrä(self.image, xpos= 25, ypos= sijY)
                
        pohja.blit(self.image, self.rect)        
                
    def lisävoimaLöytyy(self, lisävoima):
        if len(self.lisävoimat) > 0 and self.lisävoimat[0].id == lisävoima or len(self.lisävoimat) > 1 and self.lisävoimat[1].id == lisävoima:
            return True
        
        else:
            return False