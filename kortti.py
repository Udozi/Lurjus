import pygame 
from muuttujat import *
from ase import *
from grafiikka import *

maat = ["pata","hertta","risti","ruutu"]

class Kortti():
    onhaamu = False
    maa = "pata"
    arvo = None # Lähtöarvo
    voima = arvo # Voi muuttua pelin aikana; vihollisen tekemä vahinko
    heikennys = 0 # Räjähtävä taikajuoma tekee pysyvää heikennystä kierroksen ajaksi
    lisävoimat = []
    teksti = Teksti()
    indeksi = 0
        
    def vaikutus(self):
        
        if self.maa == "hertta":
            if self.lisävoimaLöytyy("vahvistava"):
                Muuttujat.juomaVoimaBonus += self.arvo
            
            return self.arvo
        
        elif self.maa == "pata" or self.maa == "risti":
            
            return -self.voima
        
        else:
            uusiAse = Ase(self.arvo + Muuttujat.aseenVoimaBonus, self.lisävoimat, self.indeksi)
            Muuttujat.aseenVoimaBonus = 0
            return uusiAse
        
    def __init__(self, määrättyMaa=maa, määrättyArvo=arvo, haamu = False, indeksi = 0):
        super().__init__()
        self.maa = määrättyMaa
        self.arvo = määrättyArvo
        self.voima = self.arvo
        self.onhaamu = haamu
        self.image = pygame.image.load("kuvat/kortit/kortti_selkä.png")
        self.originalImage = self.image
        self.rect = self.image.get_rect()
        self.lisävoimat = []
        self.indeksi = indeksi

        
    def piirrä(self, pohja):
         
        if not self.onhaamu:
            if self.image != pygame.image.load("kuvat/kortit/kortti_selkä.png") and self.arvo != None:
                
                if self.maa == "ruutu" or self.maa == "hertta":
                    self.teksti.päivitä_teksti(str(self.arvo),väri=PUNAINEN,fontti=korttiFontti, sysfont = False)

                else:
                    self.teksti.päivitä_teksti(str(self.voima),väri=MUSTA,fontti=korttiFontti,sysfont = False)

                self.teksti.rect.center = (25, 75)
                self.teksti.piirrä(self.image)
                
                if len(self.lisävoimat) > 0:
                    for l in self.lisävoimat:
                        
                        i = self.lisävoimat.index(l) + 1
                        sijY = 75 + i * 35
                        
                        kuvake = LisävoimaKuvake(l.id) 
                        kuvake.piirrä(self.image, xpos= 25, ypos= sijY)
                        
                
            pohja.blit(self.image, self.rect)    

    def lisävoimaLöytyy(self, lisävoima):
        if len(self.lisävoimat) > 0 and self.lisävoimat[0].id == lisävoima or len(self.lisävoimat) > 1 and self.lisävoimat[1].id == lisävoima:
            return True
        
        else:
            return False
    
mahdollisetLisävoimat = []
            
class Lisävoima():
    
    tyyppi = ""
    id = ""
    nimi = ""
    kuvaus1 = ""
    kuvaus2 = ""
    
    def __init__(self, indeksi = None, tyyppi = "", id = "", nimi = "", kuvaus1 = "", kuvaus2 = "", kohdemaa = ""):
        super().__init__()
        self.indeksi = indeksi
        self.tyyppi = tyyppi
        self.id = id
        self.nimi = nimi
        self.kuvaus1 = kuvaus1
        self.kuvaus2 = kuvaus2
        self.kohdemaa = kohdemaa
        
        mahdollisetLisävoimat.append(self)

# Kirouksia sekä aseiden / potionien lumouksia sekä niiden paikka koodissa

kirous1 = Lisävoima(None,"kirous","vaaniva","Vaaniva","Tämä vihollinen pysyy huoneessa,","vaikka pakenisit.","risti") #pakene_huoneesta
kirous2 = Lisävoima(None,"kirous","johtaja","Johtaja","Vahvistaa muita vihollisia","samassa huoneessa vaikeusasteen verran.","pata") #pelaa_kortti
kirous3 = Lisävoima(None,"kirous","pilkkaava","Pilkkaava","Tämä vihollinen pitää","päihittää ennen muita.","pata") #pelaa_kortti
kirous4 = Lisävoima(None,"kirous","varas","Varas","Jos pakenet tästä huoneesta, nostopinosta","hylätään yksi ruutu ja hertta.","pata") #pakene_huoneesta
kirous5 = Lisävoima(None,"kirous","kuhiseva","Kuhiseva","Tämä vihollinen täyttää huoneen","vihollisilla kuollessaan.","risti") #pelaa_kortti
kirous6 = Lisävoima(None,"kirous","näivettävä","Näivettävä","Tehdessään vahinkoa tämä pienentää","maksimiterveyttä yhdellä.","risti") #pelaa_kortti

lumousa1 = Lisävoima(None,"lumousa","paikkaus","Paikkaus","Aseella voi kaataa useamman","samanarvoisen vihollisen.") #pelaa_kortti
lumousa2 = Lisävoima(None,"lumousa","murtava","Murtava","+3 voimaa PATOJA vastaan.") #pelaa_kortti
lumousa3 = Lisävoima(None,"lumousa","polttava","Polttava","+3 voimaa RISTEJÄ vastaan.") #pelaa_kortti
lumousa4 = Lisävoima(None,"lumousa","kierrätys","Kierrätys","Seuraavaan aseesi voimaan lisätään","tämän aseen voima.") #pelaa_kortti
lumousa5 = Lisävoima(None,"lumousa","henkivaras","Henkivaras","Saat +1 terveyttä, jos","päihität vihollisen ilman vahinkoa.") #pelaa_kortti
lumousa6 = Lisävoima(None,"lumousa","nälkäinen","Nälkäinen","Tämä ase saa +3 voimaa","jokaisesta tällä kaadetusta vihollisesta.") #pelaa_kortti
lumousa7 = Lisävoima(None,"lumousa","uusiutuva","Uusiutuva","Tämä ase saa täyden kestävyyden","tuhotessaan tyrmän pienimmän vihollisen.") #pelaa_kortti

lumousp1 = Lisävoima(None,"lumousp","räjähtävä","Räjähtävä","Parantamisen sijaan tämä vähentää","huoneen vihollisten voimaa.") #pelaa_kortti
lumousp2 = Lisävoima(None,"lumousp","voideltava","Voideltava","Tällä voit parantaa jopa","maksimiterveytesi yli.") #pelaa_kortti
lumousp3 = Lisävoima(None,"lumousp","herkullinen","Herkullinen","Palauttaa terveyttä, vaikka","huoneessa olisi jo pelattu hertta.") #pelaa_kortti
#lumousp4 = Lisävoima(None,"lumousp","saapuva","Saapuva","Tämän voi käyttää nostopinosta.") #peli_loop
lumousp5 = Lisävoima(None,"lumousp","vahvistava","Vahvistava","Kasvattaa voimaasi seuraavaa","vihollista vastaan.") #pelaa_kortti
lumousp6 = Lisävoima(None,"lumousp","korjaava","Korjaava","Tämä lisää myös nykyisen","aseesi kestävyyttä.") #pelaa_kortti