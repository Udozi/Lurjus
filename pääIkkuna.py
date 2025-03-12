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
nopeus = 8

IKKUNAN_LEVEYS = 800
IKKUNAN_KORKEUS = 600
POHJA = pygame.display.set_mode((IKKUNAN_LEVEYS, IKKUNAN_KORKEUS))
POHJA.fill((255, 255, 255))
pygame.display.set_caption("Lurjus")
pygame.display.set_icon(pygame.image.load("kuvat/kortit/ruutu2.png"))
korttien_x_sijainnit = [25, 179, 333, 487]
korttien_y_sijainnit = [142, 142, 142, 142]

#Taustoja
paaValikko = Taustakuva("menuTausta")
pikapeli_tausta = Taustakuva("pikapeliTausta")
#Päävalikon napit
kampanja_nappi = Nappi("kampanja")
pikapeli_nappi = Nappi("pikapeli")
tutoriaali_nappi = Nappi("tutoriaali")
asetukset_nappi = Nappi("asetukset")
tekijät_nappi = Nappi("tekijät")
lopeta_nappi = Nappi("lopeta")
päävalikkoon_nappi = Nappi("päävalikkoon")
uusipeli_nappi = Nappi("uusipeli")

viimeisin_lyöty = Kortti()
juokse_nappi = Nappi("taistele")
hp_tausta = Teksti()
hp_teksti = Teksti()
pakka_tausta = Teksti()
pakka_teksti = Teksti()
pisteet_teksti = Pisteet()
f1_teksti = Teksti()

def piirrä_käden_kortit(pöytä):
    try:
        for i in range(0, len(pöytä)):
            kortti = pöytä[i]
            if not kortti.onhaamu:
                kortti.image = KorttiKuvakkeet.valitse_kortin_kuvake(kortti)
                kortti.rect.x = korttien_x_sijainnit[i]
                kortti.rect.y = korttien_y_sijainnit[i]
                kortti.piirrä(POHJA)
    except:
        return


def piirrä_nostopakka():
    try:
        pakkaKuva = Kortti()
        pakkaKuva.rect.x = 25
        pakkaKuva.rect.y = 355
        pakkaKuva.piirrä(POHJA)
    except:
        return

def piirrä_poistettu_kortti(poistoPakka):
    try:
        ylinKortti = poistoPakka[-1]
        sijX = 640
        sijY = 355
        ylinKortti.image = KorttiKuvakkeet.valitse_kortin_kuvake(ylinKortti)
        ylinKortti.rect.x = sijX
        ylinKortti.rect.y = sijY
        ylinKortti.piirrä(POHJA)
    except:
        return

def piirrä_ase(aseet):
    try:
        sijX = 450
        sijY = 355
        for ase in aseet:
            ase.image = KorttiKuvakkeet.valitse_aseen_kuvake(ase)
            ase.rect.x = sijX
            ase.rect.y = sijY
            ase.piirrä(POHJA)

    except:
        return

def piirrä_viimeisin_lyöty(vihu):
    try:
        sijX = 490
        sijY = 395
        vihu.image = KorttiKuvakkeet.valitse_kortin_kuvake(vihu)
        vihu.rect.x = sijX
        vihu.rect.y = sijY
        vihu.piirrä(POHJA)
    except:
        return
    
def piirrä_juoksunappi(toiminto):
    sijX = 640
    sijY = 140
    juokse_nappi.päivitä_kuva(toiminto)
    juokse_nappi.image.set_alpha(255)
    juokse_nappi.rect.x = sijX
    juokse_nappi.rect.y = sijY
    juokse_nappi.piirrä(POHJA)

def piirrä_napit():
    sijX = 668
    sijY = 22
    uusipeli_nappi.rect.x = sijX
    uusipeli_nappi.rect.y = sijY
    uusipeli_nappi.piirrä(POHJA)
    sijX = 734
    sijY = 22
    päävalikkoon_nappi.rect.x = sijX
    päävalikkoon_nappi.rect.y = sijY
    päävalikkoon_nappi.piirrä(POHJA)
    

def piirrä_tekstit(pakka):
    hp_tausta.rect.center = (340, 415)
    hp_tausta.päivitä_teksti(str(Muuttujat.HP), 76, MUSTA)
    hp_tausta.piirrä(POHJA)
    hp_teksti.rect.center = (340, 415)
    hp_teksti.päivitä_teksti(str(Muuttujat.HP), 72, VALKOINEN)
    hp_teksti.piirrä(POHJA)
    pakka_tausta.rect.center = (165, 415)
    pakka_tausta.päivitä_teksti(str(len(pakka)), 76, MUSTA)
    pakka_tausta.piirrä(POHJA)
    pakka_teksti.rect.center = (165, 415)
    pakka_teksti.päivitä_teksti(str(len(pakka)), 72, VALKOINEN)
    pakka_teksti.piirrä(POHJA)
    

def valitse(näppäin):
    if näppäin == K_1: return 1
    elif näppäin == K_2: return 2
    elif näppäin == K_3: return 3
    elif näppäin == K_4: return 4                

def piirrä_pisteet(pisteet):
    POHJA.fill((0, 0, 0))
    pisteet_teksti.rect.center = (450, 300)
    pisteet_teksti.päivitä_teksti("Peli ohi! Pisteesi: " + str(pisteet))
    pisteet_teksti.piirrä(POHJA)
    
    f1_teksti.rect.center = (450, 350)
    f1_teksti.päivitä_teksti("F1 = Aloita uusi peli")
    f1_teksti.piirrä(POHJA)
    piirrä_napit()

def valitse_viholliskortin_kohde(nykyinenAse, pelatun_kortin_arvo):
    if nykyinenAse.__len__() > 0 and nykyinenAse[0].kestavyys > pelatun_kortin_arvo:
        SiirtoAnimaatiot.lisää_aseen_päälle = True
    else:
        SiirtoAnimaatiot.lisää_aseen_päälle = False

# Valitse kohdekoordinaatit, johon korttia aletaan siirtämään
# Asekortin koordinaatit: 650, 100
# Potionit ja nyrkillä tapetut viholliset: 100, -100 (piirtoalueen ulkopuolella)
def valitse_kohde(valinta, pelattu_kortti):
    kohdeX = 0
    kohdeY = 0
    print(pelattu_kortti.maa)
    match pelattu_kortti.maa:
        case "ruutu":
            kohdeX = 450
            kohdeY = 355
        case "pata":
            if SiirtoAnimaatiot.lisää_aseen_päälle:
                kohdeX = 490
                kohdeY = 395
            else:
                kohdeX = 640
                kohdeY = 355
        case "risti":
            if SiirtoAnimaatiot.lisää_aseen_päälle:
                kohdeX = 490
                kohdeY = 395
            else:
                kohdeX = 640
                kohdeY = 355
        case "hertta":
            kohdeX = 200
            kohdeY = 415
    
    SiirtoAnimaatiot.siirtyvä_kortti = pelattu_kortti
    SiirtoAnimaatiot.viimeisin_pelattu = valinta
    SiirtoAnimaatiot.siirtyvä_kortti_sijX = korttien_x_sijainnit[valinta-1]
    SiirtoAnimaatiot.siirtyvä_kortti_sijY = korttien_y_sijainnit[valinta-1]
    SiirtoAnimaatiot.siirtyvä_kortti_kohdeX = kohdeX
    SiirtoAnimaatiot.siirtyvä_kortti_kohdeY = kohdeY

# Siirrä kortin sijaintia joka framessa n pikseliä kohti kohdekoordinatteja
def siirrä_kohteeseen():
    if SiirtoAnimaatiot.siirtyvä_kortti_sijX < SiirtoAnimaatiot.siirtyvä_kortti_kohdeX:
        SiirtoAnimaatiot.siirtyvä_kortti_sijX += nopeus
    elif SiirtoAnimaatiot.siirtyvä_kortti_sijX > SiirtoAnimaatiot.siirtyvä_kortti_kohdeX:
        SiirtoAnimaatiot.siirtyvä_kortti_sijX -= nopeus
    if SiirtoAnimaatiot.siirtyvä_kortti_sijY < SiirtoAnimaatiot.siirtyvä_kortti_kohdeY:
        SiirtoAnimaatiot.siirtyvä_kortti_sijY += nopeus
    elif SiirtoAnimaatiot.siirtyvä_kortti_sijY > SiirtoAnimaatiot.siirtyvä_kortti_kohdeY:
        SiirtoAnimaatiot.siirtyvä_kortti_sijY -= nopeus
    
    if abs(SiirtoAnimaatiot.siirtyvä_kortti_kohdeX - SiirtoAnimaatiot.siirtyvä_kortti_sijX) < nopeus:
        SiirtoAnimaatiot.siirtyvä_kortti_sijX = SiirtoAnimaatiot.siirtyvä_kortti_kohdeX
    if abs(SiirtoAnimaatiot.siirtyvä_kortti_kohdeY - SiirtoAnimaatiot.siirtyvä_kortti_sijY) < nopeus:
        SiirtoAnimaatiot.siirtyvä_kortti_sijY = SiirtoAnimaatiot.siirtyvä_kortti_kohdeY
    
    # Tarkista onko siirtymä käynnissä
    if not (SiirtoAnimaatiot.siirtyvä_kortti_sijX == SiirtoAnimaatiot.siirtyvä_kortti_kohdeX and SiirtoAnimaatiot.siirtyvä_kortti_sijY == SiirtoAnimaatiot.siirtyvä_kortti_kohdeY):
        SiirtoAnimaatiot.piirrä_siirtyvä_kortti = True
    else:
        SiirtoAnimaatiot.piirrä_siirtyvä_kortti = False

# Piirretään siirtymän ajan ylimääräinen "haamukortti"
def piirrä_siirtyvä_kortti():
    if SiirtoAnimaatiot.piirrä_siirtyvä_kortti:
        try:
            kortti = SiirtoAnimaatiot.siirtyvä_kortti
            SiirtoAnimaatiot.siirtyvä_kortti.image = KorttiKuvakkeet.valitse_kortin_kuvake(kortti)
            SiirtoAnimaatiot.siirtyvä_kortti.rect.x = SiirtoAnimaatiot.siirtyvä_kortti_sijX
            SiirtoAnimaatiot.siirtyvä_kortti.rect.y = SiirtoAnimaatiot.siirtyvä_kortti_sijY
            SiirtoAnimaatiot.siirtyvä_kortti.piirrä(POHJA)
        except:
            return
    

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

class SiirtoAnimaatiot:

    siirtyvä_kortti = Kortti()
    viimeisin_pelattu = 0
    piirrä_siirtyvä_kortti = False
    lisää_aseen_päälle = False

    siirtyvä_kortti_sijX = 0
    siirtyvä_kortti_sijY = 0
    siirtyvä_kortti_kohdeX = 0
    siirtyvä_kortti_kohdeY = 0