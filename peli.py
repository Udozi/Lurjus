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
    
    poyta = poista_haamukortit()
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
    haamukortti = Kortti()
    haamukortti.luo_kortti("hertta",0,True)
    poyta[i-1] = haamukortti
    
    
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
        
    korttejaPoydassa = laske_poytakortit()
    if korttejaPoydassa < 2:
        Muuttujat.voiJuosta = True
    
    if korttejaPoydassa == 0:
        Muuttujat.voiParantua = True
    
    if Muuttujat.HP > 20:
        Muuttujat.HP = 20
    
    korttejaJaljella = nostoPakka.__len__() + korttejaPoydassa
    if Muuttujat.HP < 1 or korttejaJaljella == 0:
        Muuttujat.peliOhi = True
  
    return

def laske_poytakortit():
    haamuja = 0
    for k in poyta:
        if k.onhaamu: haamuja += 1
    
    kortteja = poyta.__len__() - haamuja
    return(kortteja)

def poista_haamukortit():
    
    uusiPoyta = poyta
    pöydänKoko = len(poyta)
    try:
        for i in range(pöydänKoko):
            if poyta[i].onhaamu:
                uusiPoyta.pop(i) 
    except:
        return uusiPoyta
          
    return uusiPoyta

def pakene_huoneesta():

    random.shuffle(poyta)
    nostoPakka[:0] = poyta
    poyta.clear()
    Muuttujat.voiJuosta = False
    etene()
    return

def etene():  
          
    while laske_poytakortit() < 4 and nostoPakka.__len__() > 0:
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
    while laske_poytakortit() < 4 and nostoPakka.__len__() > 0:
            paljasta_kortti()

    peli_loop("Pikapeli")

def palaa_takaisin():
    skene = Muuttujat.skene
    match skene:
        case "Pikapeli":
            uusiSkene = "PaaValikko"
            Muuttujat.skene = uusiSkene
            return(uusiSkene)

# Uusi looppi (Peliä ohjataan näppäinkomennoilla)
def peli_loop(skene):
    while Muuttujat.kaynnissa:
        
        if skene == "PaaValikko":
            
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
        
        elif skene == "Pikapeli":

            for event in pygame.event.get():
                korttejaPöydässä = laske_poytakortit()
                
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                                        
                    if event.key == K_ESCAPE:
                        skene = palaa_takaisin()
                        
                    elif event.key == K_F1:
                        aloita_peli()
                    elif event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4:
                        valinta = valitse(event.key)
                        if valinta <= poyta.__len__():
                            valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1].arvo)
                            valitse_kohde(valinta, poyta[valinta-1])
                                                    
                    elif event.key == K_5:
                        if korttejaPöydässä == 4 and Muuttujat.voiJuosta:
                            pakene_huoneesta()
                            while korttejaPöydässä < 4 and nostoPakka.__len__() > 0:
                                paljasta_kortti()
                        elif korttejaPöydässä < 2:
                            etene()
                        else:
                            print("Et voi poistua huoneesta nyt.")


                elif event.type == MOUSEBUTTONDOWN:
                    if len(poyta) >= 4 and poyta[3].rect.collidepoint(pygame.mouse.get_pos()):
                        valinta = 4
                        valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1].arvo)
                        valitse_kohde(valinta, poyta[valinta-1])
                    elif len(poyta) >= 3 and poyta[2].rect.collidepoint(pygame.mouse.get_pos()):
                        valinta = 3
                        valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1].arvo)
                        valitse_kohde(valinta, poyta[valinta-1])
                    elif len(poyta) >= 2 and poyta[1].rect.collidepoint(pygame.mouse.get_pos()):
                        valinta = 2
                        valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1].arvo)
                        valitse_kohde(valinta, poyta[valinta-1])
                    elif len(poyta) >= 1 and poyta[0].rect.collidepoint(pygame.mouse.get_pos()):
                        valinta = 1
                        valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1].arvo)
                        valitse_kohde(valinta, poyta[valinta-1])
                    else:
                        valinta = -1

                    if pääIkkuna.juokse_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        if korttejaPöydässä == 4 and Muuttujat.voiJuosta:
                            pakene_huoneesta()
                            while korttejaPöydässä < 4 and nostoPakka.__len__() > 0:
                                paljasta_kortti()
                        elif korttejaPöydässä < 2:
                            etene()

                    if valinta > 0 and valinta <= len(poyta):
                        if not poyta[valinta - 1].onhaamu:
                            pelaa_kortti(valinta)
                            
                    if päävalikkoon_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        skene = palaa_takaisin()
                    elif uusipeli_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        skene = aloita_peli()
                        
        siirrä_kohteeseen()
        piirra_kaikki(skene)

# Täytä pohjavärillä, valitse piirettävät objektit ja päivitä ikkuna

def piirra_kaikki(skene):

    if skene == "PaaValikko":
        POHJA.fill((0,0,0))
        paaValikko.piirrä(POHJA)
        kampanja_nappi.piirrä(POHJA, 660, 480)
        pikapeli_nappi.piirrä(POHJA, 400, 480)
        tutoriaali_nappi.piirrä(POHJA, 140, 480)
        asetukset_nappi.piirrä(POHJA, 400, 565)
        tekijät_nappi.piirrä(POHJA, 140, 565)
        lopeta_nappi.piirrä(POHJA, 660, 565)
        pygame.display.flip()
        
    elif skene == "Pikapeli":

        POHJA.fill((0, 0, 0))
        pikapeli_tausta.piirrä(POHJA)
        
        if not Muuttujat.peliOhi:
            korttejaPöydässä = laske_poytakortit()
            piirrä_käden_kortit(poyta)
            piirrä_ase(nykyinenAse)
            
            if nostoPakka.__len__() > 0:
                piirrä_nostopakka()
            
            if nykyinenAse.__len__() > 1:
                piirrä_viimeisin_lyöty(nykyinenAse[-1])
                
            if poistoPakka.__len__() > 0:
                piirrä_poistettu_kortti(poistoPakka)
            
            if korttejaPöydässä < 2:                
                piirrä_juoksunappi("etene")
            elif korttejaPöydässä == 4 and Muuttujat.voiJuosta:
                piirrä_juoksunappi("pakene")
            else:
                piirrä_juoksunappi("taistele")

            if pääIkkuna.SiirtoAnimaatiot.piirrä_siirtyvä_kortti:
                piirrä_siirtyvä_kortti()
            
            piirrä_napit()
            piirrä_tekstit(nostoPakka)
        else:
            peli_ohi()
        pygame.display.update()
        kello.tick(FPS)   
    
def kaynnista():
    
    while Muuttujat.kaynnissa:
        
        piirra_kaikki(Muuttujat.skene)
        peli_loop("PaaValikko")
     
kaynnista()

pygame.quit()
sys.exit()