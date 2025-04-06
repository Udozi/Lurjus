import pygame 
from ase import *
from grafiikka import *

maat = ["pata","hertta","risti","ruutu"]

class Kortti():
    onhaamu = False
    maa = "pata"
    arvo = 2
    lisävoimat = []

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

mahdollisetLisävoimat = []
            
class Lisävoima():
    
    tyyppi = ""
    id = ""
    nimi = ""
    kuvaus1 = ""
    kuvaus2 = ""
    
    def __init__(self, tyyppi = "", id = "", nimi = "", kuvaus1 = "", kuvaus2 = ""):
        super().__init__()
        self.tyyppi = tyyppi
        self.id = id
        self.nimi = nimi
        self.kuvaus1 = kuvaus1
        self.kuvaus2 = kuvaus2
        
        mahdollisetLisävoimat.append(self)

# Kirouksia sekä aseiden / potionien lumouksia sekä niiden paikka koodissa

kirous1 = Lisävoima("kirous","vaaniva","Vaaniva","Tämä vihollinen pysyy huoneessa,","vaikka pakenisit.") #pakene_huoneesta
kirous2 = Lisävoima("kirous","johtaja","Johtaja","Vahvistaa muita vihollisia","samassa huoneessa kirousten verran.") #pelaa_kortti ?
kirous3 = Lisävoima("kirous","pilkkaava","Pilkkaava","Tämä vihollinen pitää","päihittää ennen muita.") #peli_loop
kirous4 = Lisävoima("kirous","varas","Varas","Jos pakenet tästä huoneesta, nostopinosta","hylätään yksi ruutu ja hertta.") #pakene_huoneesta
kirous5 = Lisävoima("kirous","kuhiseva","Kuhiseva","Tämä vihollinen täyttää huoneen","vihollisilla kuollessaan.") #pelaa_kortti
kirous6 = Lisävoima("kirous","näivettävä","Näivettävä","Tehdessään vahinkoa tämä pienentää","maksimiterveyttä yhdellä.") #pelaa_kortti

lumousa1 = Lisävoima("lumousa","paikkaus","Paikkaus","Asetta käytettäessä sen","kestävyys kasvaa yhdellä.") #pelaa_kortti
lumousa2 = Lisävoima("lumousa","murtava","Murtava","+3 voimaa PATOJA vastaan.") #pelaa_kortti
lumousa3 = Lisävoima("lumousa","polttava","Polttava","+3 voimaa RISTEJÄ vastaan.") #pelaa_kortti
lumousa4 = Lisävoima("lumousa","kierrätys","Kierrätys","Seuraavaan aseesi voimaan lisätään","tämän aseen voima.") #pelaa_kortti
lumousa5 = Lisävoima("lumousa","henkivaras","Henkivaras","Saat +1 terveyttä, jos","päihität vihollisen ilman vahinkoa.") #pelaa_kortti
lumousa6 = Lisävoima("lumousa","nälkäinen","Nälkäinen","Tämä ase saa +3 voimaa","jokaisesta tällä kaadetusta vihollisesta.") #pelaa_kortti
lumousa7 = Lisävoima("lumousa","uusiutuva","Uusiutuva","Tämä ase saa täyden kestävyyden","tuhotessaan tyrmän pienimmän vihollisen.") #pelaa_kortti

lumousp1 = Lisävoima("lumousp","räjähtävä","Räjähtävä","Parantamisen sijaan tämä vähentää","huoneen vihollisten voimaa.") #pelaa_kortti
lumousp2 = Lisävoima("lumousp","voideltava","Voideltava","Tällä voit parantaa jopa","maksimiterveytesi yli.") #pelaa_kortti
lumousp3 = Lisävoima("lumousp","herkullinen","Herkullinen","Palauttaa terveyttä, vaikka","huoneessa olisi jo pelattu hertta.") #pelaa_kortti
lumousp4 = Lisävoima("lumousp","saapuva","Saapuva","Tämän voi käyttää nostopinosta.") #peli_loop
lumousp5 = Lisävoima("lumousp","vahvistava","Vahvistava","Kasvattaa voimaasi seuraavaa","vihollista vastaan.") #pelaa_kortti
lumousp6 = Lisävoima("lumousp","korjaava","Korjaava","Tämä lisää myös nykyisen","aseesi kestävyyttä.") #pelaa_kortti