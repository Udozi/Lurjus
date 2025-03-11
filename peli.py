import random, os, pääIkkuna
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 
from pygame.locals import *

from grafiikka import *
from kortti import *
from muuttujat import *
from ase import *
from pääIkkuna import *

pygame.init()
FPS = 60
kello = pygame.time.Clock()
 
# Pelin värit
PUNAINEN   = (255, 0, 0)
MUSTA = (0, 0, 0)
LÄHESVALKOINEN = (240, 230, 220)
VALKOINEN = (255, 255, 255)
 
# Luodaan ikkuna
IKKUNAN_LEVEYS = 800
IKKUNAN_KORKEUS = 600
PIIRTOALUSTA = pygame.display.set_mode((IKKUNAN_LEVEYS,IKKUNAN_KORKEUS))
PIIRTOALUSTA.fill(VALKOINEN)
pygame.display.set_caption("Scoundrel")
pygame.display.set_icon(pygame.image.load("kuvat/smorc.png"))

# Scoundrel-pelin maat:
# Ruutu (2-10) - Ase (vähentää vihollisten tekemää vahinkoa)
# Hertta (2-10) - Taikajuoma/ruoka (parantaa sinua)    
# Pata (2-14) - Vihollinen (tekee sinuun vahinkoa)
# Risti (2-14) - Vihollinen (ks. pata)
korttienMaara = {
    "ruutu": 9,
    "hertta": 9,
    "pata": 13,
    "risti": 13
}

nostoPakka = []
poistoPakka = []
poyta = []
nykyinenAse = []

# Yhden kortin siirtäminen nostopakasta pöydälle
def paljasta_kortti():
    
    ylinKortti = nostoPakka[-1]
    poydattyKortti = ylinKortti
    nostoPakka.pop()
    poyta.append(poydattyKortti)
    return

def hylkaa_ase():
    
    poistoPakka.extend(nykyinenAse)
    nykyinenAse.clear()
    return

def pelaa_kortti(i):
    
    pelattavaKortti = poyta[i-1]
    vaikutus = pelattavaKortti.vaikutus()
    poyta.pop(i-1)
    
    # Jos pelattu kortti on ruutu (=ase)
    if type(vaikutus) is not int:
        
        if nykyinenAse.__len__() > 0: hylkaa_ase()
            
        uusiAse = vaikutus
        nykyinenAse.append(uusiAse)
    
    else:
        # Vihollinen haastetaan aseen kanssa
        if nykyinenAse.__len__() > 0 and vaikutus < 0:
            vihollisenVoima = -1 * vaikutus
            
            # Ase kuluu käytössä: Aseella päihitettävän vihollisen
            # on oltava pienempi kuin edellinen sillä aseella
            # päihitetty vihollinen
            if nykyinenAse[0].kestavyys > vihollisenVoima:
                hpMuutos = int(nykyinenAse[0].kayta(vihollisenVoima))
                nykyinenAse.append(pelattavaKortti)
            
                if hpMuutos > 0:
                    hpMuutos = 0
                    
            else:
                
                hylkaa_ase()
                hpMuutos = int(vaikutus)
                poistoPakka.append(pelattavaKortti)
        
        
        # Pelattu kortti on parannuskortti tai 
        # ilman asetta kohdattu vihollinen
        else:
            
            # Vain yksi parannus huoneessa
            if Muuttujat.voiParantua or vaikutus < 0: hpMuutos = vaikutus 
            else: hpMuutos = 0  
                 
            poistoPakka.append(pelattavaKortti)
            if hpMuutos > 0: Muuttujat.voiParantua = False
            
        Muuttujat.HP = Muuttujat.HP + hpMuutos
        Muuttujat.voiJuosta = False
    
    if poyta.__len__() < 2:
        Muuttujat.voiJuosta = True
    
    if poyta.__len__() == 0:
        Muuttujat.voiParantua = True
    
    if Muuttujat.HP > 20:
        Muuttujat.HP = 20
    
    korttejaJaljella = nostoPakka.__len__() + poyta.__len__()
    if Muuttujat.HP < 1 or korttejaJaljella == 0:
        Muuttujat.peliOhi = True
  
    return

def karkaa_huoneesta():

    random.shuffle(poyta)
    nostoPakka[:0] = poyta
    poyta.clear()
    Muuttujat.voiJuosta = False
    return

def etene():  
          
    while poyta.__len__() < 4 and nostoPakka.__len__() > 0:
        paljasta_kortti()
    
    Muuttujat.voiParantua = True    
    return

def peli_ohi():

    pisteet = Muuttujat.HP
    
    # Pisteiden lasku pelin hävittyä
    if Muuttujat.HP < 1:
        nostoPakka.extend(poyta)
        poyta.clear()
        
        for k in nostoPakka:
            if k.maa == "pata" or k.maa == "risti":
                pisteet -= k.arvo
                
        piirrä_pisteet(pisteet)
    
    # Pisteiden lasku pelin voitettua    
    if Muuttujat.HP > 0:

        viimeinenKortti = poistoPakka[-1]
        
        if viimeinenKortti.maa == "hertta" and Muuttujat.HP == 20: 
            pisteet += viimeinenKortti.arvo 
        
        piirrä_pisteet(pisteet)   
        
        
        
def nollaa_peli():
    nostoPakka.clear()
    poyta.clear()
    poistoPakka.clear()
    nykyinenAse.clear()
    Muuttujat.HP = 20
    Muuttujat.peliOhi = False
    Muuttujat.voiJuosta = True
    Muuttujat.voiParantua = True

# Pelin alussa luodaan ja sekoitetaan korttipakka.
# Pakasta poistetaan punaiset kuvakortit ja ässät.

def aloita_peli():
    nollaa_peli()
    for m in maat:
        for a in range(korttienMaara[m]):
            uusiKortti = Kortti()
            uusiKortti.luo_kortti(m,a + 2)
            nostoPakka.append(uusiKortti)
    random.shuffle(nostoPakka)
    while poyta.__len__() < 4 and nostoPakka.__len__() > 0:
            paljasta_kortti()

    peli_loop("Pikapeli")

def prosessoi_tapahtumat():
    for event in pygame.event.get():
        if event.type == QUIT:
            Muuttujat.kaynnissa = False

        elif event.type == MOUSEBUTTONDOWN:    
            if Muuttujat.skene == "PaaValikko":
                if kampanja_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                    Muuttujat.skene = "Kampanja"
                    print(Muuttujat.skene)
                    Muuttujat.skene = "PaaValikko"
                                    
                elif pikapeli_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                    Muuttujat.skene = "Pikapeli"
                    aloita_peli()
                    print(Muuttujat.skene)
                                    
                elif tutoriaali_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                    Muuttujat.skene = "Tutoriaali"
                    print(Muuttujat.skene)
                    Muuttujat.skene = "PaaValikko"
                                    
                elif tekijät_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                    Muuttujat.skene = "Tekijat"
                    print(Muuttujat.skene)
                    Muuttujat.skene = "PaaValikko"
                    
                elif asetukset_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                    Muuttujat.skene = "Asetukset"
                    print(Muuttujat.skene)
                    Muuttujat.skene = "PaaValikko"
                                    
                elif lopeta_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                    print("Kiitos käynnistä!")
                    Muuttujat.kaynnissa = False

# Uusi looppi (Peliä ohjataan näppäinkomennoilla)
def peli_loop(skene):
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Muuttujat.skene = "PaaValikko"
                    
                elif event.key == K_F1:
                    aloita_peli()
                elif event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4:
                    print()
                    valinta = valitse(event.key)
                    if valinta <= poyta.__len__():
                        pelaa_kortti(valinta)
                                                
                elif event.key == K_5:
                    if poyta.__len__() == 4 and Muuttujat.voiJuosta:
                        karkaa_huoneesta()
                        while poyta.__len__() < 4 and nostoPakka.__len__() > 0:
                            paljasta_kortti()
                    elif poyta.__len__() == 1:
                        etene()
                    else:
                        print("Et voi poistua huoneesta nyt.")


            elif event.type == MOUSEBUTTONDOWN:
                if len(poyta) >= 4 and poyta[3].rect.collidepoint(pygame.mouse.get_pos()):
                    valinta = 4
                elif len(poyta) >= 3 and poyta[2].rect.collidepoint(pygame.mouse.get_pos()):
                    valinta = 3
                elif len(poyta) >= 2 and poyta[1].rect.collidepoint(pygame.mouse.get_pos()):
                    valinta = 2
                elif len(poyta) >= 1 and poyta[0].rect.collidepoint(pygame.mouse.get_pos()):
                    valinta = 1
                else:
                    valinta = -1

                if pääIkkuna.pakene_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                    if poyta.__len__() == 4 and Muuttujat.voiJuosta:
                        karkaa_huoneesta()
                        while poyta.__len__() < 4 and nostoPakka.__len__() > 0:
                            paljasta_kortti()
                elif pääIkkuna.etene_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                    if poyta.__len__() < 2:
                        etene()

                if valinta > 0 and valinta <= poyta.__len__():
                    pelaa_kortti(valinta)

        if poyta.__len__() == 4 and Muuttujat.voiJuosta:
            pääIkkuna.voi_paeta = True
        else:
            pääIkkuna.voi_paeta = False
        if poyta.__len__() < 2:
            pääIkkuna.voi_edetä = True
        else:
            pääIkkuna.voi_edetä = False

        piirra_kaikki(skene)

# Täytä pohjavärillä, valitse piirettävät objektit ja päivitä ikkuna

def piirra_kaikki(skene):

    if skene == "PaaValikko":
        paaValikko.piirrä(PIIRTOALUSTA)
        kampanja_nappi.piirrä(PIIRTOALUSTA, 200, 225)
        pikapeli_nappi.piirrä(PIIRTOALUSTA, 600, 225)
        tutoriaali_nappi.piirrä(PIIRTOALUSTA, 200, 375)
        asetukset_nappi.piirrä(PIIRTOALUSTA, 600, 375)
        tekijät_nappi.piirrä(PIIRTOALUSTA, 200, 525)
        lopeta_nappi.piirrä(PIIRTOALUSTA, 600, 525)
        pygame.display.flip()
        
    elif skene == "Pikapeli":

        POHJA.fill((0, 0, 0))
        if not Muuttujat.peliOhi:
            piirrä_käden_kortit(poyta)
            piirrä_ase(nykyinenAse)
            
            if nykyinenAse.__len__() > 1:
                piirrä_viimeisin_lyöty(nykyinenAse[-1])
                
            piirrä_napit()
            piirrä_tekstit(nostoPakka)
        else:
            peli_ohi()
        pygame.display.update()
        kello.tick(FPS)   
    
def kaynnista():
    
    while Muuttujat.kaynnissa:
        
        piirra_kaikki(Muuttujat.skene)
        prosessoi_tapahtumat()
     
kaynnista()

pygame.quit()
quit()