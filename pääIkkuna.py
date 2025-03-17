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
nopeus = 20

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
opastus_tausta = Taustakuva("opastusTausta")
tekijät_tausta = Taustakuva("tekijätTausta")
#Päävalikon napit
kampanja_nappi = Nappi("kampanja")
pikapeli_nappi = Nappi("pikapeli")
opastus_nappi = Nappi("opastus")
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
opastus_tekstirivi1 = Teksti()
opastus_tekstirivi2 = Teksti()

def piirrä_käden_kortit(pöytä):
    try:
        pöydässäKortteja = len(pöytä)
        if pöytä[-1].onhaamu and pöydässäKortteja > 1:
            SiirtoAnimaatiot.piirrä_pöydättävä_kortti = False
        
        for i in range(0, pöydässäKortteja):
            kortti = pöytä[i]
            
            if not kortti.onhaamu and not (i == 0 and SiirtoAnimaatiot.piirrä_jäänyt_kortti):
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

def piirrä_poistettu_kortti(poistoPakka, nykyinenAse):
    try:
        i = 1

        if SiirtoAnimaatiot.piirrä_pelattava_kortti and Muuttujat.aseestaPoistoon > 0:
            i += Muuttujat.aseestaPoistoon + 1
            if len(nykyinenAse) == 1:
                i -= 1
        
        elif SiirtoAnimaatiot.piirrä_pelattava_kortti and (not SiirtoAnimaatiot.lisää_aseen_päälle and SiirtoAnimaatiot.siirtyvä_kortti.maa != "ruutu"):
            i += 1     
         
        ylinKortti = poistoPakka[-i]
        sijX = 640
        sijY = 355
        
        if ylinKortti.maa == "ruutu":
            ylinKortti.image = KorttiKuvakkeet.valitse_aseen_kuvake(ylinKortti)
        else:
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
            if not Muuttujat.käytäAsetta:
                ase.image.set_alpha(50)            
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
        if not Muuttujat.käytäAsetta:
            vihu.image.set_alpha(50)
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

def piirrä_napit(n = 2):
    
    if n > 1:
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
    hp_tausta.rect.center = (350, 415)
    hp_tausta.päivitä_teksti(str(Muuttujat.HP), 92, MUSTA)
    hp_tausta.piirrä(POHJA)
    hp_teksti.rect.center = (350, 415)
    hp_teksti.päivitä_teksti(str(Muuttujat.HP), 88, VALKOINEN)
    hp_teksti.piirrä(POHJA)
    pakka_tausta.rect.center = (175, 415)
    pakka_tausta.päivitä_teksti(str(len(pakka)), 92, MUSTA)
    pakka_tausta.piirrä(POHJA)
    pakka_teksti.rect.center = (175, 415)
    pakka_teksti.päivitä_teksti(str(len(pakka)), 88, VALKOINEN)
    pakka_teksti.piirrä(POHJA)
    
    if Muuttujat.skene == "Opastus":
        opastus_tekstirivi1.rect.center = (330, 25)
        opastus_tekstirivi2.rect.center = (330, 55)
        opastusFontti = "Dubai"
        opastusFonttiKoko = 20

        match Muuttujat.huoneNumero:
            case 0:
                opastus_tekstirivi1.päivitä_teksti("Tervetuloa opastuskierrokselle! Pelaa kortteja", fonttikoko=opastusFonttiKoko, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("painamalla niitä. Paina 'Etene' jatkaaksesi.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 1: 
                opastus_tekstirivi1.päivitä_teksti("Padat ja ristit (viholliset) tekevät sinuun vahinkoa.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("Hertat (taikajuomat) palauttavat terveyspisteitäsi.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 2:
                opastus_tekstirivi1.päivitä_teksti("Voit paeta täydestä huoneesta, mutta et kahdesti peräkkäin.", fonttikoko=17, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("Kortit sekoitetaan ja siirretään nostopinon pohjalle.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 3: 
                opastus_tekstirivi1.päivitä_teksti("Ruudut (aseet) vähentävät ottamaasi vahinkoa.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("Kun poimit aseen, edellinen siirtyy poistopakkaan.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 4:
                opastus_tekstirivi1.päivitä_teksti("Voit käyttää asetta vain vihollisiin, joiden suuruus", fonttikoko=opastusFonttiKoko, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("on pienempi kuin aseella viimeksi lyöty vihollinen.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 5: 
                opastus_tekstirivi1.päivitä_teksti("Voit edetä, kun huoneessa on alle kaksi korttia.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("Poista käytöstä tai ota käyttöön aseesi painamalla sitä.", fonttikoko=19, fontti=opastusFontti)
            case 6: 
                opastus_tekstirivi1.päivitä_teksti("Voit saada terveyttä vain yhdestä huoneessa pelatusta", fonttikoko=19, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("hertasta. Seuraavassa huoneessa voit parantua lisää.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 7: 
                opastus_tekstirivi1.päivitä_teksti("Peli päättyy, kun sekä nostopino että huone ovat tyhjät...", fonttikoko=18, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("...tai kun terveyspisteesi loppuvat.", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 8: 
                opastus_tekstirivi1.päivitä_teksti("Peli päättyy, kun sekä nostopino että huone ovat tyhjät...", fonttikoko=18, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("...tai kun terveyspisteesi loppuvat..", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 9: 
                opastus_tekstirivi1.päivitä_teksti("Peli päättyy, kun sekä nostopino että huone ovat tyhjät...", fonttikoko=18, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("...tai kun terveyspisteesi loppuvat...", fonttikoko=opastusFonttiKoko, fontti=opastusFontti)
            case 10: 
                opastus_tekstirivi1.päivitä_teksti("Psst! Voit saada tulokseksi jopa 30 pistettä voittamalla pelin", fonttikoko=17, fontti=opastusFontti) 
                opastus_tekstirivi2.päivitä_teksti("täysillä terveyspisteillä ja juomalla lopuksi ison taikajuoman!", fonttikoko=17, fontti=opastusFontti)
        opastus_tekstirivi1.piirrä(POHJA)
        opastus_tekstirivi2.piirrä(POHJA)
    

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
    
    f1_teksti.rect.center = (300, 350)
    f1_teksti.päivitä_teksti("F1 = Aloita uusi peli - ESC = Palaa päävalikkoon", 24)
    f1_teksti.piirrä(POHJA)
    piirrä_napit()

def valitse_viholliskortin_kohde(nykyinenAse, pelattu_kortti):
    if nykyinenAse.__len__() > 0 and nykyinenAse[0].kestavyys > pelattu_kortti.arvo and (pelattu_kortti.maa == "pata" or pelattu_kortti.maa == "risti") and Muuttujat.käytäAsetta:
        SiirtoAnimaatiot.lisää_aseen_päälle = True
    else:
        SiirtoAnimaatiot.lisää_aseen_päälle = False

# Valitse kohdekoordinaatit, johon korttia aletaan siirtämään
# Asekortin koordinaatit: 650, 100
# Potionit ja nyrkillä tapetut viholliset: 100, -100 (piirtoalueen ulkopuolella)
def valitse_kohde(valinta, pelattu_kortti):
    kohdeX = 0
    kohdeY = 0
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

    # Tarkista, mikä siirtymä on käynnissä
    
    match SiirtoAnimaatiot.viimeisin_siirtyvä:
        case "pelattu":
            
            sijX = SiirtoAnimaatiot.siirtyvä_kortti_sijX
            sijY = SiirtoAnimaatiot.siirtyvä_kortti_sijY
            kohdeX = SiirtoAnimaatiot.siirtyvä_kortti_kohdeX
            kohdeY = SiirtoAnimaatiot.siirtyvä_kortti_kohdeY
            muutosX = sijX - kohdeX
            muutosY = sijY - kohdeY
            hypotenuusa = (muutosX**2 + muutosY**2)**(1/2)

            if hypotenuusa != 0:
                sijX -= nopeus * muutosX / hypotenuusa
                sijY -= nopeus * muutosY / hypotenuusa

            if abs(kohdeX - sijX) < nopeus:
                sijX = kohdeX
            if abs(kohdeY - sijY) < nopeus:
                sijY = kohdeY
                
            SiirtoAnimaatiot.siirtyvä_kortti_sijX = sijX
            SiirtoAnimaatiot.siirtyvä_kortti_sijY = sijY
            
            if not (SiirtoAnimaatiot.siirtyvä_kortti_sijX == kohdeX and SiirtoAnimaatiot.siirtyvä_kortti_sijY == kohdeY):
                SiirtoAnimaatiot.piirrä_pelattava_kortti = True
            else:
                SiirtoAnimaatiot.piirrä_pelattava_kortti = False
                
        case "pöydätty":
            
            sijX = SiirtoAnimaatiot.pöydättävä_kortti_sijX
            sijY = SiirtoAnimaatiot.pöydättävä_kortti_sijY
            kohdeX = SiirtoAnimaatiot.pöydättävä_kortti_kohdeX
            kohdeY = SiirtoAnimaatiot.pöydättävä_kortti_kohdeY
            muutosX = sijX - kohdeX
            muutosY = sijY - kohdeY
            hypotenuusa = (muutosX**2 + muutosY**2)**(1/2)

            if hypotenuusa != 0:
                sijX -= nopeus * muutosX / hypotenuusa
                sijY -= nopeus * muutosY / hypotenuusa

            if abs(kohdeX - sijX) < nopeus:
                sijX = kohdeX
            if abs(kohdeY - sijY) < nopeus:
                sijY = kohdeY
                
            SiirtoAnimaatiot.siirtyvä_kortti_sijX = sijX
            SiirtoAnimaatiot.siirtyvä_kortti_sijY = sijY
            
            if not (SiirtoAnimaatiot.siirtyvä_kortti_sijX == kohdeX and SiirtoAnimaatiot.siirtyvä_kortti_sijY == kohdeY):
                SiirtoAnimaatiot.piirrä_pöydättävä_kortti = True
            else:
                SiirtoAnimaatiot.piirrä_pöydättävä_kortti = False

def siirrä_pöytään(n):
    sijX = SiirtoAnimaatiot.pöydättävä_kortti_sijX
    sijY = SiirtoAnimaatiot.pöydättävä_kortti_sijY
    kohdeX = 25 + 154 * n
    kohdeY = 142
    muutosX = sijX - kohdeX
    muutosY = sijY - kohdeY
    hypotenuusa = (muutosX**2 + muutosY**2)**(1/2)

    if hypotenuusa != 0:
        sijX -= nopeus * muutosX / hypotenuusa
        sijY -= nopeus * muutosY / hypotenuusa

    if abs(kohdeX - sijX) < nopeus:
        sijX = kohdeX
    if abs(kohdeY - sijY) < nopeus:
        sijY = kohdeY
        
    SiirtoAnimaatiot.pöydättävä_kortti_sijX = sijX
    SiirtoAnimaatiot.pöydättävä_kortti_sijY = sijY
    
    # Tarkista onko siirtymä käynnissä
    if not (sijX == kohdeX and sijY == kohdeY):
        SiirtoAnimaatiot.piirrä_pöydättävä_kortti = True
    else:
        SiirtoAnimaatiot.piirrä_pöydättävä_kortti = False

def siirrä_nostopakkaan():
    
    sijX = 0
    sijY = 0
    kohdeX = SiirtoAnimaatiot.pako_kohdeX
    kohdeY = SiirtoAnimaatiot.pako_kohdeY
    
    for i in range(4):
        match i:
            case 0: 
                sijX = SiirtoAnimaatiot.pako_kortti1_sijX
                sijY = SiirtoAnimaatiot.pako_kortti1_sijY
            case 1: 
                sijX = SiirtoAnimaatiot.pako_kortti2_sijX
                sijY = SiirtoAnimaatiot.pako_kortti2_sijY
            case 2: 
                sijX = SiirtoAnimaatiot.pako_kortti3_sijX
                sijY = SiirtoAnimaatiot.pako_kortti3_sijY    
            case 3: 
                sijX = SiirtoAnimaatiot.pako_kortti4_sijX
                sijY = SiirtoAnimaatiot.pako_kortti4_sijY
        
        muutosX = sijX - kohdeX
        muutosY = sijY - kohdeY        
        hypotenuusa = (muutosX**2 + muutosY**2)**(1/2)
        
        if hypotenuusa != 0:
            sijX -= nopeus * muutosX / hypotenuusa
            sijY -= nopeus * muutosY / hypotenuusa

        if abs(kohdeX - sijX) < nopeus:
            sijX = kohdeX
        if abs(kohdeY - sijY) < nopeus:
            sijY = kohdeY
            
        match i:
            case 0: 
                SiirtoAnimaatiot.pako_kortti1_sijX = sijX
                SiirtoAnimaatiot.pako_kortti1_sijY = sijY
            case 1: 
                SiirtoAnimaatiot.pako_kortti2_sijX = sijX 
                SiirtoAnimaatiot.pako_kortti2_sijY = sijY 
            case 2: 
                SiirtoAnimaatiot.pako_kortti3_sijX = sijX 
                SiirtoAnimaatiot.pako_kortti3_sijY = sijY   
            case 3: 
                SiirtoAnimaatiot.pako_kortti4_sijX = sijX 
                SiirtoAnimaatiot.pako_kortti4_sijY = sijY
                if sijX == kohdeX and sijY == kohdeY:
                    SiirtoAnimaatiot.piirrä_pakokortit = False 

# Piirretään siirtymän ajan ylimääräinen "haamukortti"
def piirrä_pelattava_kortti():
    if SiirtoAnimaatiot.piirrä_pelattava_kortti:

        try:
            kortti = SiirtoAnimaatiot.siirtyvä_kortti
            SiirtoAnimaatiot.siirtyvä_kortti.image = KorttiKuvakkeet.valitse_kortin_kuvake(kortti)
            SiirtoAnimaatiot.siirtyvä_kortti.rect.x = SiirtoAnimaatiot.siirtyvä_kortti_sijX
            SiirtoAnimaatiot.siirtyvä_kortti.rect.y = SiirtoAnimaatiot.siirtyvä_kortti_sijY
            SiirtoAnimaatiot.siirtyvä_kortti.piirrä(POHJA)
        except:
            return

# Piirretään pöytäyksen ajan ylimääräinen "haamukortti"    
def piirrä_pöydättävä_kortti():
    if SiirtoAnimaatiot.piirrä_pöydättävä_kortti:
        try:
            kortti = SiirtoAnimaatiot.pöydättävä_kortti
            SiirtoAnimaatiot.pöydättävä_kortti.image = KorttiKuvakkeet.valitse_kortin_kuvake(kortti)
            SiirtoAnimaatiot.pöydättävä_kortti.rect.x = SiirtoAnimaatiot.pöydättävä_kortti_sijX
            SiirtoAnimaatiot.pöydättävä_kortti.rect.y = SiirtoAnimaatiot.pöydättävä_kortti_sijY
            SiirtoAnimaatiot.pöydättävä_kortti.piirrä(POHJA)
        except:
            return

def piirrä_vanha_asepino():
    delta_vax = SiirtoAnimaatiot.vanha_ase_kohdeX - SiirtoAnimaatiot.vanha_ase_sijX
    delta_vay = SiirtoAnimaatiot.vanha_ase_kohdeY - SiirtoAnimaatiot.vanha_ase_sijY
    delta_vvx = SiirtoAnimaatiot.vanha_vihu_kohdeX - SiirtoAnimaatiot.vanha_vihu_sijX
    delta_vvy = SiirtoAnimaatiot.vanha_vihu_kohdeY - SiirtoAnimaatiot.vanha_vihu_sijY
    
    vanha_ase_hypotenuusa = ((delta_vax)**2 + (delta_vay)**2)**(1/2)
    if abs(delta_vax) < nopeus:
        SiirtoAnimaatiot.vanha_ase_sijX == SiirtoAnimaatiot.vanha_ase_kohdeX 
    else: SiirtoAnimaatiot.vanha_ase_sijX += nopeus * delta_vax / vanha_ase_hypotenuusa 
    if abs(delta_vay) < nopeus:
        SiirtoAnimaatiot.vanha_ase_sijY == SiirtoAnimaatiot.vanha_ase_kohdeY
    else: SiirtoAnimaatiot.vanha_ase_sijY += nopeus * delta_vay / vanha_ase_hypotenuusa
    
    if SiirtoAnimaatiot.piirrä_vanha_ase: 
        SiirtoAnimaatiot.vanha_ase.image = KorttiKuvakkeet.valitse_aseen_kuvake(SiirtoAnimaatiot.vanha_ase)
        SiirtoAnimaatiot.vanha_ase.rect.x = SiirtoAnimaatiot.vanha_ase_sijX
        SiirtoAnimaatiot.vanha_ase.rect.y = SiirtoAnimaatiot.vanha_ase_sijY
        SiirtoAnimaatiot.vanha_ase.piirrä(POHJA)
        
    if delta_vax == 0 and delta_vay == 0:
        SiirtoAnimaatiot.piirrä_vanha_ase = False
        SiirtoAnimaatiot.vanha_ase_sijX = SiirtoAnimaatiot.vanha_ase_oletusarvot[0]
        SiirtoAnimaatiot.vanha_ase_sijY = SiirtoAnimaatiot.vanha_ase_oletusarvot[1]
    
    vanha_vihu_hypotenuusa = ((delta_vvx)**2 + (delta_vvy)**2)**(1/2)
    if abs(delta_vvx) < nopeus:
        SiirtoAnimaatiot.vanha_vihu_sijX == SiirtoAnimaatiot.vanha_vihu_kohdeX 
    else: SiirtoAnimaatiot.vanha_vihu_sijX += nopeus * delta_vvx / vanha_vihu_hypotenuusa 
    if abs(delta_vvy) < nopeus:
        SiirtoAnimaatiot.vanha_vihu_sijY == SiirtoAnimaatiot.vanha_vihu_kohdeY
    else: SiirtoAnimaatiot.vanha_vihu_sijY += nopeus * delta_vvy / vanha_vihu_hypotenuusa
    
    if SiirtoAnimaatiot.piirrä_vanha_vihu:
        SiirtoAnimaatiot.vanha_vihu.image = KorttiKuvakkeet.valitse_kortin_kuvake(SiirtoAnimaatiot.vanha_vihu)
        SiirtoAnimaatiot.vanha_vihu.rect.x = SiirtoAnimaatiot.vanha_vihu_sijX
        SiirtoAnimaatiot.vanha_vihu.rect.y = SiirtoAnimaatiot.vanha_vihu_sijY
        SiirtoAnimaatiot.vanha_vihu.piirrä(POHJA)
        
    if delta_vvx == 0 and delta_vvy == 0:
        SiirtoAnimaatiot.piirrä_vanha_vihu = False
        SiirtoAnimaatiot.vanha_vihu_sijX = SiirtoAnimaatiot.vanha_vihu_oletusarvot[0]
        SiirtoAnimaatiot.vanha_vihu_sijY = SiirtoAnimaatiot.vanha_vihu_oletusarvot[1]

def piirrä_jäänyt_kortti():

    if abs(SiirtoAnimaatiot.jäänyt_kortti_kohdeX - SiirtoAnimaatiot.jäänyt_kortti_sijX) < nopeus:
        SiirtoAnimaatiot.jäänyt_kortti_sijX = SiirtoAnimaatiot.jäänyt_kortti_kohdeX
    else:
        SiirtoAnimaatiot.jäänyt_kortti_sijX -= nopeus

    if SiirtoAnimaatiot.piirrä_jäänyt_kortti:
        SiirtoAnimaatiot.jäänyt_kortti.image = KorttiKuvakkeet.valitse_kortin_kuvake(SiirtoAnimaatiot.jäänyt_kortti)
        SiirtoAnimaatiot.jäänyt_kortti.rect.x = SiirtoAnimaatiot.jäänyt_kortti_sijX
        SiirtoAnimaatiot.jäänyt_kortti.rect.y = SiirtoAnimaatiot.jäänyt_kortti_sijY
        SiirtoAnimaatiot.jäänyt_kortti.piirrä(POHJA)

    if SiirtoAnimaatiot.jäänyt_kortti_sijX == SiirtoAnimaatiot.jäänyt_kortti_kohdeX:
        SiirtoAnimaatiot.piirrä_jäänyt_kortti = False
    return    

def piirrä_pakokortit():
    if SiirtoAnimaatiot.piirrä_pakokortit:

        SiirtoAnimaatiot.pako_kortti1.rect.x = SiirtoAnimaatiot.pako_kortti1_sijX
        SiirtoAnimaatiot.pako_kortti1.rect.y = SiirtoAnimaatiot.pako_kortti1_sijY
        SiirtoAnimaatiot.pako_kortti1.piirrä(POHJA)
        
        SiirtoAnimaatiot.pako_kortti2.rect.x = SiirtoAnimaatiot.pako_kortti2_sijX
        SiirtoAnimaatiot.pako_kortti2.rect.y = SiirtoAnimaatiot.pako_kortti2_sijY
        SiirtoAnimaatiot.pako_kortti2.piirrä(POHJA)

        SiirtoAnimaatiot.pako_kortti3.rect.x = SiirtoAnimaatiot.pako_kortti3_sijX
        SiirtoAnimaatiot.pako_kortti3.rect.y = SiirtoAnimaatiot.pako_kortti3_sijY
        SiirtoAnimaatiot.pako_kortti3.piirrä(POHJA)

        SiirtoAnimaatiot.pako_kortti4.rect.x = SiirtoAnimaatiot.pako_kortti4_sijX
        SiirtoAnimaatiot.pako_kortti4.rect.y = SiirtoAnimaatiot.pako_kortti4_sijY
        SiirtoAnimaatiot.pako_kortti4.piirrä(POHJA)

def nollaa_korttien_paikat():
    SiirtoAnimaatiot.pöydättävä_kortti_sijX = SiirtoAnimaatiot.pöydättävä_kortti_oletusarvot[0]
    SiirtoAnimaatiot.pöydättävä_kortti_sijY = SiirtoAnimaatiot.pöydättävä_kortti_oletusarvot[1]
    SiirtoAnimaatiot.pöydättävä_kortti_kohdeX = SiirtoAnimaatiot.pöydättävä_kortti_oletusarvot[2]
    SiirtoAnimaatiot.pöydättävä_kortti_kohdeY = SiirtoAnimaatiot.pöydättävä_kortti_oletusarvot[3]

    SiirtoAnimaatiot.siirtyvä_kortti_sijX = SiirtoAnimaatiot.siirtyvä_kortti_oletusarvot[0]
    SiirtoAnimaatiot.siirtyvä_kortti_sijY = SiirtoAnimaatiot.siirtyvä_kortti_oletusarvot[1]
    SiirtoAnimaatiot.siirtyvä_kortti_kohdeX = SiirtoAnimaatiot.siirtyvä_kortti_oletusarvot[2]
    SiirtoAnimaatiot.siirtyvä_kortti_kohdeY = SiirtoAnimaatiot.siirtyvä_kortti_oletusarvot[3]
    
    SiirtoAnimaatiot.vanha_ase_sijX = SiirtoAnimaatiot.vanha_ase_oletusarvot[0]
    SiirtoAnimaatiot.vanha_ase_sijY = SiirtoAnimaatiot.vanha_ase_oletusarvot[1]
    SiirtoAnimaatiot.vanha_ase_kohdeX = SiirtoAnimaatiot.vanha_ase_oletusarvot[2]
    SiirtoAnimaatiot.vanha_ase_kohdeY = SiirtoAnimaatiot.vanha_ase_oletusarvot[3]
    
    SiirtoAnimaatiot.vanha_vihu_sijX = SiirtoAnimaatiot.vanha_vihu_oletusarvot[0]
    SiirtoAnimaatiot.vanha_vihu_sijY = SiirtoAnimaatiot.vanha_vihu_oletusarvot[1]
    SiirtoAnimaatiot.vanha_vihu_kohdeX = SiirtoAnimaatiot.vanha_vihu_oletusarvot[2]
    SiirtoAnimaatiot.vanha_vihu_kohdeY = SiirtoAnimaatiot.vanha_vihu_oletusarvot[3]
    
    SiirtoAnimaatiot.jäänyt_kortti_sijX = SiirtoAnimaatiot.jäänyt_kortti_oletusarvot[0]
    SiirtoAnimaatiot.jäänyt_kortti_sijY = SiirtoAnimaatiot.jäänyt_kortti_oletusarvot[1]
    SiirtoAnimaatiot.jäänyt_kortti_kohdeX = SiirtoAnimaatiot.jäänyt_kortti_oletusarvot[2]
    SiirtoAnimaatiot.jäänyt_kortti_kohdeY = SiirtoAnimaatiot.jäänyt_kortti_oletusarvot[3]
    
    SiirtoAnimaatiot.pako_kortti1_sijX = SiirtoAnimaatiot.pako_oletusarvotX[0]
    SiirtoAnimaatiot.pako_kortti1_sijY = SiirtoAnimaatiot.pako_oletusarvoY
    SiirtoAnimaatiot.pako_kortti2_sijX = SiirtoAnimaatiot.pako_oletusarvotX[1]
    SiirtoAnimaatiot.pako_kortti2_sijY = SiirtoAnimaatiot.pako_oletusarvoY
    SiirtoAnimaatiot.pako_kortti3_sijX = SiirtoAnimaatiot.pako_oletusarvotX[2]
    SiirtoAnimaatiot.pako_kortti3_sijY = SiirtoAnimaatiot.pako_oletusarvoY
    SiirtoAnimaatiot.pako_kortti4_sijX = SiirtoAnimaatiot.pako_oletusarvotX[3]
    SiirtoAnimaatiot.pako_kortti4_sijY = SiirtoAnimaatiot.pako_oletusarvoY
    
    SiirtoAnimaatiot.piirrä_pelattava_kortti = False
    SiirtoAnimaatiot.piirrä_pöydättävä_kortti = False
    SiirtoAnimaatiot.piirrä_vanha_ase = False
    SiirtoAnimaatiot.piirrä_vanha_vihu = False

def piirrä_kortin_kehys(valinta):
    try:
        match valinta:
            case 1:
                sijX = 25
                sijY = 142
            case 2:
                sijX = 179
                sijY = 142
            case 3:
                sijX = 333
                sijY = 142
            case 4:
                sijX = 487
                sijY = 142
            case 5:
                sijX = 640
                sijY = 140
            case 0:
                return
        sijX -= 4; sijY -= 5
        if valinta == 1 or valinta == 2 or valinta == 3 or valinta == 4:
            Efektit.kortti_kehys.piirrä(POHJA, sijX, sijY)
        elif valinta == 5:
            Efektit.huone_kehys.piirrä(POHJA, sijX, sijY)
    except:
        return
    
def piirrä_valikon_kehys(iso, valinta):
    try:
        if iso:
            match valinta:
                case 1:
                    sijX = 140
                    sijY = 480
                case 2:
                    sijX = 400
                    sijY = 480
                case 3:
                    sijX = 660
                    sijY = 480
                case 0:
                    return
            Efektit.valikko_iso_kehys.piirrä(POHJA, sijX, sijY)
        else:
            match valinta:
                case 1:
                    sijX = 140
                    sijY = 565
                case 2:
                    sijX = 400
                    sijY = 565
                case 3:
                    sijX = 660
                    sijY = 565
                case 0:
                    return
            Efektit.valikko_pieni_kehys.piirrä(POHJA, sijX, sijY)
    except:
        return
    
def piirrä_pikavalinnan_kehys(valinta):
    try:
        match valinta:
            case 1:
                sijX = 668
                sijY = 22
            case 2:
                sijX = 734
                sijY = 22
            case 0:
                return
        sijX -= 5; sijY -= 4
        Efektit.pikavalinta_kehys.piirrä(POHJA, sijX, sijY)
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
    pöydättävä_kortti = Kortti()
    vanha_ase = Ase()
    vanha_vihu = Kortti()
    jäänyt_kortti = Kortti()
    pako_kortti1 = Kortti()
    pako_kortti2 = Kortti()
    pako_kortti3 = Kortti()
    pako_kortti4 = Kortti()
    viimeisin_pelattu = 0
    viimeisin_siirtyvä = "pöydätty"
    piirrä_pelattava_kortti = False
    piirrä_pöydättävä_kortti = False
    piirrä_vanha_ase = False
    piirrä_vanha_vihu = False
    piirrä_jäänyt_kortti = False
    piirrä_pakokortit = False
    piirrä_liikettä = piirrä_pelattava_kortti or piirrä_pöydättävä_kortti or piirrä_vanha_ase or piirrä_vanha_vihu
    lisää_aseen_päälle = False
    
    pöydättävä_kortti_oletusarvot = [25, 355, 475, 142]
    pöydättävä_kortti_sijX = pöydättävä_kortti_oletusarvot[0]
    pöydättävä_kortti_sijY = pöydättävä_kortti_oletusarvot[1]
    pöydättävä_kortti_kohdeX = pöydättävä_kortti_oletusarvot[2]
    pöydättävä_kortti_kohdeY = pöydättävä_kortti_oletusarvot[3]
    
    siirtyvä_kortti_oletusarvot = [0, 0, 0, 0]
    siirtyvä_kortti_sijX = siirtyvä_kortti_oletusarvot[0]
    siirtyvä_kortti_sijY = siirtyvä_kortti_oletusarvot[1]
    siirtyvä_kortti_kohdeX = siirtyvä_kortti_oletusarvot[2]
    siirtyvä_kortti_kohdeY = siirtyvä_kortti_oletusarvot[3]
    
    vanha_ase_oletusarvot = [450, 355, 640, 355]
    vanha_ase_sijX = vanha_ase_oletusarvot[0]
    vanha_ase_sijY = vanha_ase_oletusarvot[1]
    vanha_ase_kohdeX = vanha_ase_oletusarvot[2]
    vanha_ase_kohdeY = vanha_ase_oletusarvot[3]
    
    vanha_vihu_oletusarvot = [490, 395, 640, 355]
    vanha_vihu_sijX = vanha_vihu_oletusarvot[0]
    vanha_vihu_sijY = vanha_vihu_oletusarvot[1]
    vanha_vihu_kohdeX = vanha_vihu_oletusarvot[2]
    vanha_vihu_kohdeY = vanha_vihu_oletusarvot[3]
    
    jäänyt_kortti_oletusarvot = [25, 142, 25, 142]
    jäänyt_kortti_sijX = jäänyt_kortti_oletusarvot[0]
    jäänyt_kortti_sijY = jäänyt_kortti_oletusarvot[1]
    jäänyt_kortti_kohdeX = jäänyt_kortti_oletusarvot[2]
    jäänyt_kortti_kohdeY = jäänyt_kortti_oletusarvot[3]
    
    pako_oletusarvotX = [25, 175, 325, 475]
    pako_oletusarvoY = 142
    pako_kohdeX = 25
    pako_kohdeY = 355
    pako_kortti1_sijX = pako_oletusarvotX[0]
    pako_kortti1_sijY = pako_oletusarvoY
    pako_kortti2_sijX = pako_oletusarvotX[1]
    pako_kortti2_sijY = pako_oletusarvoY
    pako_kortti3_sijX = pako_oletusarvotX[2]
    pako_kortti3_sijY = pako_oletusarvoY
    pako_kortti4_sijX = pako_oletusarvotX[3]
    pako_kortti4_sijY = pako_oletusarvoY
    


class Efektit:

    kortti_kehys = Kehys("kortti")
    huone_kehys = Kehys("huone")
    kortti_hover = 0

    pikavalinta_kehys = Kehys("pikavalinta")
    pikavalinta_hover = 0

    valikko_iso_kehys = Kehys("valikko_iso")
    valikko_pieni_kehys = Kehys("valikko_pieni")
    valikko_iso = True
    valikko_hover = 0