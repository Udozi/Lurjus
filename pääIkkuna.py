import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys
from pygame.locals import *

from muuttujat import Muuttujat
from kortti import *
from grafiikka import *

pygame.init()
FPS = 60
kello = pygame.time.Clock()

IKKUNAN_LEVEYS = 800
IKKUNAN_KORKEUS = 600
POHJA = pygame.display.set_mode((IKKUNAN_LEVEYS, IKKUNAN_KORKEUS))
POHJA.fill((255, 255, 255))
pygame.display.set_caption("Lurjus")
pygame.display.set_icon(pygame.image.load("kuvat/kortit/ruutu2.png"))
korttien_x_sijainnit = {
    1 : 60,
    2 : 120,
    3 : 180,
    4 : 240,
}
korttien_y_sijainnit = {
    1 : 200,
    2 : 200,
    3 : 200,
    4 : 200,
}

paaValikko = PaaValikko()
#Päävalikon napit
kampanja_nappi = Nappi("kampanja")
pikapeli_nappi = Nappi("pikapeli")
tutoriaali_nappi = Nappi("tutoriaali")
asetukset_nappi = Nappi("asetukset")
tekijät_nappi = Nappi("tekijät")
lopeta_nappi = Nappi("lopeta")

viimeisin_lyöty = Kortti()
etene_nappi = Nappi("etene")
pakene_nappi = Nappi("pakene")
hp_teksti = Teksti()
pakka_teksti = Teksti()
voi_edetä = False
voi_paeta = True
pisteet_teksti = Pisteet()
f1_teksti = Teksti()

def piirrä_käden_kortit(pöytä):
    try:
        sijX = 50
        sijY = 400
        for i in range(0, len(pöytä)):
            kortti = pöytä[i]
            if not kortti.onhaamu:
                kortti.image = KorttiKuvakkeet.valitse_kortin_kuvake(kortti)
                kortti.rect.x = sijX
                kortti.rect.y = sijY
            sijX += 100
            kortti.piirrä(POHJA)
    except:
        return

def piirrä_ase(aseet):
    try:
        sijX = 650
        sijY = 100
        for ase in aseet:
            ase.image = KorttiKuvakkeet.valitse_aseen_kuvake(ase)
            ase.rect.x = sijX
            ase.rect.y = sijY
            ase.piirrä(POHJA)

    except:
        return

def piirrä_viimeisin_lyöty(vihu):
    try:
        sijX = 650
        sijY = 150
        vihu.image = KorttiKuvakkeet.valitse_lyödyn_kuvake(vihu)
        vihu.rect.x = sijX
        vihu.rect.y = sijY
        vihu.piirrä(POHJA)
    except:
        return
    
def piirrä_napit():
    sijX = 480
    sijY = 400
    if voi_edetä: etene_nappi.image.set_alpha(255)
    else: etene_nappi.image.set_alpha(127)
    etene_nappi.rect.x = sijX
    etene_nappi.rect.y = sijY
    etene_nappi.piirrä(POHJA)
    sijX = 480
    sijY = 460
    if voi_paeta: pakene_nappi.image.set_alpha(255)
    else: pakene_nappi.image.set_alpha(127)
    pakene_nappi.rect.x = sijX
    pakene_nappi.rect.y = sijY
    pakene_nappi.piirrä(POHJA)

def piirrä_tekstit(pakka):
    hp_teksti.rect.center = (120, 60)
    hp_teksti.päivitä_teksti("HP: " + str(Muuttujat.HP))
    hp_teksti.piirrä(POHJA)
    pakka_teksti.rect.center = (600, 60)
    if pakka.__len__() == 1:
        pakka_teksti.päivitä_teksti("Nostopakassa jäljellä " + str(len(pakka)) + " kortti")
    else:
        pakka_teksti.päivitä_teksti("Nostopakassa jäljellä " + str(len(pakka)) + " korttia")
    pakka_teksti.piirrä(POHJA)
    

def valitse(näppäin):
    if näppäin == K_1: return 1
    elif näppäin == K_2: return 2
    elif näppäin == K_3: return 3
    elif näppäin == K_4: return 4                

def piirrä_pisteet(pisteet):
    pisteet_teksti.rect.center = (450, 300)
    pisteet_teksti.päivitä_teksti("Peli ohi! Pisteesi: " + str(pisteet))
    pisteet_teksti.piirrä(POHJA)
    
    f1_teksti.rect.center = (450, 350)
    f1_teksti.päivitä_teksti("F1 = Aloita uusi peli")
    f1_teksti.piirrä(POHJA)

class KorttiKuvakkeet:

    def valitse_kortin_kuvake(kortti):
        kuvake = None
        tiedoston_nimi = "kuvat/kortit/" + kortti.maa + str(kortti.arvo) + ".png"
        kuvake = pygame.image.load(tiedoston_nimi)
        return kuvake
    
    def valitse_aseen_kuvake(ase):
        try:
            kuvake = None
            tiedoston_nimi = "kuvat/kortit/ruutu" + str(ase.voima) + ".png"
            kuvake = pygame.image.load(tiedoston_nimi)
            return kuvake
        except:
            return
    
    def valitse_lyödyn_kuvake(vihu):
        try:
            kuvake = None
            tiedoston_nimi = "kuvat/kortit/" + vihu.maa + str(vihu.arvo) + ".png"
            kuvake = pygame.image.load(tiedoston_nimi)
            return kuvake
        except:
            return