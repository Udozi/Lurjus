from muuttujat import Muuttujat
import pygame

class Kauppias():
    sija = 1
    tila = "odottaa"
    hinta = 0
    toiminto = ""
    
    def __init__(self, sija):
        super().__init__()
        self.sija = sija
        self.image = pygame.image.load("kuvat/kauppiaat/kauppias" + str(self.sija) + self.tila + ".png")
        self.rect = self.image.get_rect()
        
        if sija == 1:    
            self.hinta = 2
            self.toiminto = "kasvataPunaisia"
            self.rect.center = (110, 200)
            
        elif sija == 2:            
            self.hinta = 1
            
            if True or Muuttujat.HP <= Muuttujat.maxHP / 2: # Poista True kun lumouksia lisätään
                self.toiminto = "kasvataHP"
                
            else: self.toiminto = "lumoaPunaisia"
            
            self.rect.center = (300, 257)
            
        elif sija == 3:
            self.hinta = 0
            
            if Muuttujat.haasteOtettu: self.toiminto = "tarjoaKirous"
            else: self.toiminto = "tarjoaHaaste"
            
            self.rect.center = (500, 185)
            
        else: 
            if (len(Muuttujat.esineet) == 1 and Muuttujat.helmiä == 0) or len(Muuttujat.esineet) == 2:
                self.hinta = 0
                self.toiminto = "vaihdaEsine"
                
            else:
                self.hinta = 1
                self.toiminto = "myyEsine"
                
            self.rect.center = (700, 201)
                
    def muuta_kuva(self):
        self.image = pygame.image.load("kuvat/kauppiaat" + self.sija + self.tila)
        self.rect = self.image.get_rect()
    
    def asioi(self):
        
        if Muuttujat.helmiä < self.hinta:
            return False        
        
        Muuttujat.helmiä -= self.hinta
        
        match self.toiminto:
            
            case "kasvataPunaisia":
                
                Muuttujat.punaistenTaso += 1
                
            case "kasvataHP":

                Muuttujat.maxHP += 3
                Muuttujat.HP = Muuttujat.maxHP
                
        return True

    
    def piirrä(self, pohja):        
        pohja.blit(self.image, self.rect) 