import pygame

class Ase():
    voima = 2
    arvo = voima
    kestavyys = 15
    maa = "ruutu"
   
    def poimi(self, arvo):
       self.voima = arvo
       return self
       
    def kayta(self, hyokkays):
        self.kestavyys = hyokkays
        vahinko = self.voima - hyokkays
        return(vahinko)
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("kuvat/kortit/kortti_selkä.png")
        self.originalImage = self.image
        self.rect = self.image.get_rect()

    def piirrä(self, pohja):
        pohja.blit(self.image, self.rect)        