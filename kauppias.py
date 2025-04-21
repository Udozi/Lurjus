from muuttujat import Muuttujat
from haasteet import haasteet
from esineet import mahdollisetEsineet
from kortti import *
import pygame, random, math

mahdollisetAselumoukset = []
mahdollisetJuomalumoukset = []
mahdollisetKiroukset = []

for lv in mahdollisetLisävoimat:
    match lv.tyyppi:
        case "lumousa":
            mahdollisetAselumoukset.append(lv)
        case "lumousp":
            mahdollisetJuomalumoukset.append(lv)            

class Kauppias():
    sija = 1
    tila = "odottaa"
    hinta = 0
    toiminto = ""
    haaste = None
    esine = None
    lumoukset = []
    kiroukset = []
    pakotaLisävoimaton = False
    
    info_otsikko = ""
    info_rivi1 = ""
    info_rivi2 = ""
    
    def __init__(self, sija, pakotaLisävoimaton = False):
        super().__init__()
        self.sija = sija
        self.image = pygame.image.load("kuvat/kauppiaat/kauppias" + str(self.sija) + self.tila + ".png")
        self.rect = self.image.get_rect()
        self.pakotaLisävoimaton = pakotaLisävoimaton
        
        if sija == 1:    
            self.hinta = 2
            self.toiminto = "kasvataPunaisia"
            self.rect.center = (110, 200)
            self.info_otsikko = "Kasvata punaisia kortteja"
            self.info_rivi1 = "Kasvata kaikkia herttoja ja ruutuja yhdellä."
            
        elif sija == 2:            
            self.hinta = 1
            self.lumoukset.clear()
            
            if Muuttujat.HP <= Muuttujat.maxHP / 2 or self.pakotaLisävoimaton: 
                self.toiminto = "kasvataHP"
                self.info_otsikko = "Kasvata maksimiterveyttä ja parannu"
                self.info_rivi1 = "Kasvata maksimiterveyttäsi kolmella terveyspisteellä"
                self.info_rivi2 = "ja parannu täysiin terveyspisteisiin."
                
            else: 
                self.toiminto = "lumoaPunaisia"
                lumottaviaAseita = [0,1,2,3,4,5,6,7,8]
                lumottaviaJuomia = [0,1,2,3,4,5,6,7,8]
                lumotut = []
                
                for lumous in Muuttujat.aselumoukset:
                    lumotut.append(lumous.indeksi)
                    if lumotut.count(lumous.indeksi) > 1 and lumous.indeksi in lumottaviaAseita:
                        lumottaviaAseita.remove(lumous.indeksi)
                    
                lumotut.clear()
                
                for lumous in Muuttujat.juomalumoukset:
                    lumotut.append(lumous.indeksi)
                    if lumotut.count(lumous.indeksi) > 1 and lumous.indeksi in lumottaviaJuomia:
                        lumottaviaJuomia.remove(lumous.indeksi)
                
                lumousa = None
                lumousa = random.choice(mahdollisetAselumoukset)
                if len(lumottaviaAseita) == 0:
                    self.tila = "virhe"
                    return 
                lumousa.indeksi = random.choice(lumottaviaAseita)
                self.lumoukset.append(lumousa)
                
                lumousp = None
                lumousp = random.choice(mahdollisetJuomalumoukset)
                if len(lumottaviaJuomia) == 0:
                    self.tila = "virhe"
                    return
                lumousp.indeksi = random.choice(lumottaviaJuomia)
                self.lumoukset.append(lumousp)
                
                self.info_otsikko = "Lumoa yksi ase ja taikajuoma"
                self.info_rivi1 = "Aselumous: " + lumousa.nimi
                self.info_rivi2 = "Juomalumous: " + lumousp.nimi
            
            self.rect.center = (300, 257)
            
        elif sija == 3:
            self.hinta = 0
            
            if Muuttujat.haasteOtettu and not self.pakotaLisävoimaton: 
            
                self.toiminto = "tarjoaKirouksia"
                self.kiroukset.clear()
                self.hinta = -1
                kirottaviaVihollisia = [0,1,2,3,4,5,6,7,8,9,10,11,12]
                kirotut = []
                nimilista = []
                
                while len(self.kiroukset) < 3 and len(kirottaviaVihollisia) > 0: 
                    
                    mahdollisetKiroukset.clear()
                    
                    for lv in mahdollisetLisävoimat:
                        if lv.tyyppi == "kirous": mahdollisetKiroukset.append(lv)
                    
                    for kirous in Muuttujat.kiroukset:
                        kirotut.append(kirous.indeksi)
                        
                        if kirotut.count(kirous.indeksi) > 1 and kirous.indeksi in kirottaviaVihollisia:
                                kirottaviaVihollisia.remove(kirous.indeksi)
                  
                    if len(kirottaviaVihollisia) == 0:
                        self.tila = "virhe"
                        return
                        
                    elif len(kirottaviaVihollisia) < 3: 
                        break
                        
                    valittuKirous = random.choice(mahdollisetKiroukset)
                    valittuKirous.indeksi = random.choice(kirottaviaVihollisia)
                    uusiKirous = Lisävoima(valittuKirous.indeksi, "kirous", valittuKirous.id, valittuKirous.nimi, valittuKirous.kuvaus1, valittuKirous.kuvaus2, valittuKirous.kohdemaa)
                    
                    # Kauppias tekee joka kerta kolme eri kirousta
                    if not uusiKirous.nimi in nimilista:
                        nimilista.append(uusiKirous.nimi)
                        self.kiroukset.append(uusiKirous)
               
                self.info_otsikko = "Ota vastaan kolme kirousta"
                self.info_rivi1 = "Saat heti yhden helmen, mutta"
                self.info_rivi2 = "jotkut viholliset vahvistuvat pysyvästi."
            
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
            
            esinelista = []
            for e in mahdollisetEsineet:                
                if not e in Muuttujat.esineet:
                    esinelista.append(e)
            
            self.esine = random.choice(esinelista)
            if self.esine.id == "amuletti": 
                self.esine.kuvaus2 = "ottamaasi haastetta kohden. (" + str(Muuttujat.amuletinVoima) + ")"
            
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
                if Muuttujat.HP < Muuttujat.maxHP:
                    Muuttujat.HP = Muuttujat.maxHP
            
            case "lumoaPunaisia":
                
                Muuttujat.aselumoukset.append(self.lumoukset[0])
                Muuttujat.juomalumoukset.append(self.lumoukset[1])
                
            case "tarjoaHaaste":
                
                Muuttujat.valittuHaaste = self.haaste
                Muuttujat.amuletinVoima += 1
                
            case "tarjoaKirouksia":
                
                Muuttujat.kiroukset.extend(self.kiroukset)
            
            case "myyEsine":                
                Muuttujat.esineet.append(self.esine)
                
            case "vaihdaEsine":
                Muuttujat.esineet.pop(0)
                Muuttujat.esineet.append(self.esine)
                
        return True

    
    def piirrä(self, pohja):        
        pohja.blit(self.image, self.rect) 