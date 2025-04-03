from muuttujat import Muuttujat
from haasteet import haasteet
from esineet import mahdollisetEsineet
import pygame, random, math

class Kauppias():
    sija = 1
    tila = "odottaa"
    hinta = 0
    toiminto = ""
    haaste = None
    esine = None
    
    info_otsikko = ""
    info_rivi1 = ""
    info_rivi2 = ""
    
    def __init__(self, sija):
        super().__init__()
        self.sija = sija
        self.image = pygame.image.load("kuvat/kauppiaat/kauppias" + str(self.sija) + self.tila + ".png")
        self.rect = self.image.get_rect()
        
        if sija == 1:    
            self.hinta = 2
            self.toiminto = "kasvataPunaisia"
            self.rect.center = (110, 200)
            self.info_otsikko = "Kasvata punaisia kortteja"
            self.info_rivi1 = "Kasvata kaikkia herttoja ja ruutuja yhdellä."
            
        elif sija == 2:            
            self.hinta = 1
            
            if True or Muuttujat.HP <= Muuttujat.maxHP / 2: # Poista True kun lumouksia lisätään
                self.toiminto = "kasvataHP"
                self.info_otsikko = "Kasvata maksimiterveyttä ja parannu"
                self.info_rivi1 = "Kasvata maksimiterveyttäsi kolmella terveyspisteellä"
                self.info_rivi2 = "ja parannu täysiin terveyspisteisiin."
                
            else: self.toiminto = "lumoaPunaisia"
            
            self.rect.center = (300, 257)
            
        elif sija == 3:
            self.hinta = 0
            
            if False and Muuttujat.haasteOtettu: self.toiminto = "tarjoaKirous" # Poista False kun kirouksia lisätään
            
            else: 
                self.toiminto = "tarjoaHaaste"
                
                # Kauppias arpoo haasteen listalta
                self.haaste = haasteet[random.randrange(len(haasteet))]
                
                if self.haaste.id == "palkkiometsästäjä":
                    self.haaste.kuvaus2 = str(min(20, 15 + math.floor(Muuttujat.vaikeusaste))) + " suuruinen vihollinen."
                
                Muuttujat.tarjottuHaaste = self.haaste
                self.info_otsikko = self.haaste.nimi + ": Seuraavassa pelissä"
                self.info_rivi1 = self.haaste.kuvaus1 + " " + self.haaste.kuvaus2
            
            self.rect.center = (500, 246)
            
        else: 
            self.esine = mahdollisetEsineet[random.randrange(len(mahdollisetEsineet))]
            self.info_rivi1 = self.esine.kuvaus1 + " " + self.esine.kuvaus2
            
            if (len(Muuttujat.esineet) == 1 and Muuttujat.helmiä == 0) or len(Muuttujat.esineet) == 2:
                self.hinta = 0
                self.toiminto = "vaihdaEsine"
                self.info_otsikko = "Vaihda esine: " + self.esine.nimi 
                self.info_rivi2 = "Vaihdossa annat esineen: " + Muuttujat.esineet[0].nimi
                
            else:
                self.hinta = 1
                self.toiminto = "myyEsine"
                self.info_otsikko = "Osta esine: " + self.esine.nimi
                               
            self.rect.center = (700, 245)
                
    def vaihda_tila(self, tila = "odottaa"):
        
        if self.tila != "myyty":
            self.tila = tila
            self.image = pygame.image.load("kuvat/kauppiaat/kauppias" + str(self.sija) + self.tila + ".png")
            self.rect = self.image.get_rect()
            
            if self.sija == 1:
                if self.tila == "odottaa": self.rect.center = (110, 200)
                elif self.tila == "huomio": self.rect.center = (108, 232)
                else: self.rect.center = (108, 198)
                
            if self.sija == 2:
                if self.tila == "odottaa": self.rect.center = (300, 257)
                elif self.tila == "huomio": self.rect.center = (300, 250)
                else: self.rect.center = (300, 342)
                
            if self.sija == 3:
                if self.tila == "odottaa": self.rect.center = (500, 246)
                elif self.tila == "huomio": self.rect.center = (500, 236)
                else: self.rect.center = (500, 256)
                
            if self.sija == 4:
                if self.tila == "odottaa": self.rect.center = (700, 245)
                elif self.tila == "huomio": self.rect.center = (700, 239)
                else: self.rect.center = (700, 241)

    
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
                
            case "tarjoaHaaste":
                
                Muuttujat.valittuHaaste = self.haaste
                Muuttujat.amuletinVoima += 1
                
            case "myyEsine":                
                Muuttujat.esineet.append(self.esine)
                
            case "vaihdaEsine":
                Muuttujat.esineet.pop(0)
                Muuttujat.esineet.append(self.esine)
                
        return True

    
    def piirrä(self, pohja):        
        pohja.blit(self.image, self.rect) 