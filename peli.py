import random, os, pääIkkuna
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 
from pygame.locals import *

from grafiikka import *
from kortti import *
from muuttujat import *
from ase import *
from pääIkkuna import *
from äänet import *

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
huoneenKoko = 4

# Yhden kortin siirtäminen nostopakasta pöydälle
def paljasta_kortti():

    if not Muuttujat.opastusTauko: poista_haamukortit()
    
    pöydättyKortti = nostoPakka[-1]
    SiirtoAnimaatiot.viimeisin_siirtyvä = "pöydätty"
    SiirtoAnimaatiot.pöydättävä_kortti = pöydättyKortti
    SiirtoAnimaatiot.pöydättävä_kortti_sijX = 25
    SiirtoAnimaatiot.pöydättävä_kortti_sijY = 380
    i = laske_poytakortit()
    siirrä_pöytään(i)
    
    while SiirtoAnimaatiot.piirrä_pöydättävä_kortti:

        siirrä_pöytään(i)
        piirrä_kaikki()
        
    nostoPakka.pop()
    poyta.append(pöydättyKortti)

    return

def hylkaa_ase():
    
    Muuttujat.aseestaPoistoon = nykyinenAse.__len__()
    poistoPakka.extend(nykyinenAse)
    nykyinenAse.clear()
    
    return

def pelaa_kortti(i):
    
    SiirtoAnimaatiot.piirrä_siirtyvä_kortti = False
    SiirtoAnimaatiot.viimeisin_siirtyvä = "pelattu"
    pelattavaKortti = poyta[i-1]
    Muuttujat.viimeksiPelattu = pelattavaKortti
    vaikutus = pelattavaKortti.vaikutus()
    haamukortti = Kortti()
    haamukortti.luo_kortti("hertta",0,True)
    poyta[i-1] = haamukortti
  
    
    # Jos pelattu kortti on ruutu (=ase)
    if type(vaikutus) is not int:
        
        if nykyinenAse.__len__() > 0: hylkaa_ase()
            
        uusiAse = vaikutus
        nykyinenAse.append(uusiAse)
        Muuttujat.käytäAsetta = True
        toista_sfx("kerää_ase")
    
    else:
        # Vihollinen haastetaan aseen kanssa
        if nykyinenAse.__len__() > 0 and vaikutus < 0 and Muuttujat.käytäAsetta:
            vihollisenVoima = -1 * vaikutus
            
            # Ase kuluu käytössä: Aseella päihitettävän vihollisen
            # on oltava pienempi kuin edellinen sillä aseella
            # päihitetty vihollinen
            if nykyinenAse[0].kestavyys > vihollisenVoima:
                hpMuutos = int(nykyinenAse[0].kayta(vihollisenVoima))
                nykyinenAse.append(pelattavaKortti)
            
                if hpMuutos > 0:
                    hpMuutos = 0

                toista_sfx("hyökkäys")
                    
            else:
                
                hylkaa_ase()
                hpMuutos = int(vaikutus)
                poistoPakka.append(pelattavaKortti)
                toista_sfx("damage")
        
        # Pelattu kortti on parannuskortti tai 
        # ilman asetta kohdattu vihollinen
        else:
            
            # Vain yksi parannus huoneessa
            if Muuttujat.voiParantua or vaikutus < 0: hpMuutos = vaikutus 
            else: hpMuutos = 0  
                 
            poistoPakka.append(pelattavaKortti)
            if hpMuutos > 0:
                Muuttujat.voiParantua = False
                toista_sfx("potion")
            elif hpMuutos < 0:
                toista_sfx("damage")
            else:
                toista_sfx("denied")
            
        Muuttujat.HP = Muuttujat.HP + hpMuutos
        Muuttujat.voiJuosta = False
        
    korttejaPöydässä = laske_poytakortit()
    if korttejaPöydässä < 2 and (Muuttujat.skene != "Opastus" or Muuttujat.huoneNumero > 4 or korttejaPöydässä == 0 or Muuttujat.huoneNumero == 0):
        Muuttujat.voiJuosta = True
    
    if korttejaPöydässä == 0:
        Muuttujat.voiParantua = True
    
    if Muuttujat.HP > 20:
        Muuttujat.HP = 20
    
    korttejaJaljella = nostoPakka.__len__() + korttejaPöydässä
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
    try:
        
        for i in range(len(poyta)):
            if poyta[i].onhaamu:
                uusiPoyta.pop(i) 

    except:
        return 

def pakene_huoneesta():

    random.shuffle(poyta)
    nostoPakka[:0] = poyta
    poyta.clear()
    Muuttujat.voiJuosta = False
    toista_sfx("click")
    uusi_huone()
    return

def peli_ohi():

    SiirtoAnimaatiot.piirrä_siirtyvä_kortti = False
    SiirtoAnimaatiot.piirrä_pöydättävä_kortti = False
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
    nollaa_korttien_paikat()
    Muuttujat.HP = 20
    Muuttujat.peliOhi = False
    Muuttujat.voiParantua = True
    
    if Muuttujat.skene == "Opastus":
        Muuttujat.voiJuosta = False
        Muuttujat.opastusTauko = True
    else:
        Muuttujat.voiJuosta = True
    

# Pelin alussa luodaan ja sekoitetaan korttipakka.
# Pakasta poistetaan punaiset kuvakortit ja ässät.

def aloita_peli():
    nollaa_peli()
    
    if Muuttujat.skene == "Pikapeli":
        for m in maat:
            for a in range(korttienMaara[m]):
                uusiKortti = Kortti()
                uusiKortti.luo_kortti(m,a + 2)
                nostoPakka.append(uusiKortti)
        random.shuffle(nostoPakka)
        
        Muuttujat.huoneNumero = 1
        
    elif Muuttujat.skene == "Opastus":
        # Pelaaja käy läpi käsikirjoitetun opastuskierroksen
        
        huone0 = [Kortti("hertta", 8, True), Kortti("hertta", 7, True), Kortti("hertta", 6, True), Kortti("hertta", 5, True)] # Tyhjä haamuhuone opastuksen alkuun
        huone1 = [Kortti("pata",2),Kortti("risti",3),Kortti("pata",4),Kortti("hertta",9)]       # Vihut ja parantavat juomat
        huone2 = [Kortti("pata",11),Kortti("risti",12),Kortti("pata",13),Kortti("risti",14)]    # Pakeneminen
        huone3 = [Kortti("ruutu",2),Kortti("ruutu",3),Kortti("ruutu",4),Kortti("pata",5),]      # Aseen vaihtaminen
        huone4 = [Kortti("ruutu",5),Kortti("pata",9),Kortti("pata",8),Kortti("pata",7)]         # Aseella lyöminen
        huone5 = [Kortti("pata",10),Kortti("risti",2),Kortti("ruutu",10),Kortti("pata",3)]      # Aseen vaihto (ja käsin taistelu) - Nyt saa edetä
        huone6 = [Kortti("hertta",10),Kortti("hertta",3),Kortti("ruutu",9),Kortti("hertta",2)]  # Vain yksi parantuminen/huone
        opastus_tyrmä = [huone6, huone5, huone4, huone3, huone2, huone1, huone0]
        
        for huone in opastus_tyrmä:
            random.shuffle(huone)
            nostoPakka.extend(huone)        
        
        Muuttujat.huoneNumero = -1 # Opastuksen dialogin tahdittamiseen
        
    uusi_huone()
    peli_loop()


def uusi_huone():
    
    Muuttujat.huoneNumero += 1
    Muuttujat.voiParantua = True
    if not Muuttujat.opastusTauko: poista_haamukortit()
    
    SiirtoAnimaatiot.piirrä_siirtyvä_kortti = False  
    nollaa_korttien_paikat() 

    if not Muuttujat.opastusTauko:
        while laske_poytakortit() < huoneenKoko and nostoPakka.__len__() > 0:
            paljasta_kortti()
            
    else:
        for i in range(4):
            paljasta_kortti()
        Muuttujat.opastusTauko = False
            
    SiirtoAnimaatiot.piirrä_pöydättävä_kortti = False
        

def palaa_takaisin():
    skene = Muuttujat.skene
    match skene:
        case "Pikapeli":
            uusiSkene = "PaaValikko"
            Muuttujat.skene = uusiSkene

        case "Opastus":
            uusiSkene = "PaaValikko"
            Muuttujat.skene = uusiSkene
            
        case "Tekijät":
            uusiSkene = "PaaValikko"
            Muuttujat.skene = uusiSkene


# Uusi looppi (Peliä ohjataan näppäinkomennoilla)
def peli_loop():
    while Muuttujat.käynnissä:
        
        if Muuttujat.skene == "PaaValikko":
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    Muuttujat.käynnissä = False

                elif event.type == MOUSEBUTTONDOWN:    

                    if kampanja_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        Muuttujat.skene = "Kampanja"
                        print(Muuttujat.skene)
                        Muuttujat.skene = "PaaValikko"
                                        
                    elif pikapeli_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        Muuttujat.skene = "Pikapeli"
                        toista_sfx("click")
                        aloita_peli()
                                        
                    elif opastus_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        Muuttujat.skene = "Opastus"
                        toista_sfx("click")
                        aloita_peli()
                                        
                    elif tekijät_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        Muuttujat.skene = "Tekijät"
                        toista_sfx("click")
                        while Muuttujat.skene == "Tekijät":
                            peli_loop()
                        
                    elif asetukset_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        Muuttujat.skene = "Asetukset"
                        print(Muuttujat.skene)
                        Muuttujat.skene = "PaaValikko"
                                        
                    elif lopeta_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        toista_sfx("click")
                        print("Kiitos käynnistä!")
                        Muuttujat.käynnissä = False

                elif event.type == MOUSEMOTION:

                    if kampanja_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.valikko_iso = True
                        pääIkkuna.Efektit.valikko_hover = 0 #3 Ei käytössä
                                        
                    elif pikapeli_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.valikko_iso = True
                        pääIkkuna.Efektit.valikko_hover = 2
                                        
                    elif opastus_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.valikko_iso = True
                        pääIkkuna.Efektit.valikko_hover = 1
                                        
                    elif tekijät_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.valikko_iso = False
                        pääIkkuna.Efektit.valikko_hover = 1
                        
                    elif asetukset_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.valikko_iso = False
                        pääIkkuna.Efektit.valikko_hover = 0 #2 Ei käytössä
                                        
                    elif lopeta_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.valikko_iso = False
                        pääIkkuna.Efektit.valikko_hover = 3
                    else:
                        pääIkkuna.Efektit.valikko_hover = 0
        
        elif Muuttujat.skene == "Pikapeli" or Muuttujat.skene == "Opastus":

            for event in pygame.event.get():
                korttejaPöydässä = laske_poytakortit()
                
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    valinta = 0
                                        
                    if event.key == K_ESCAPE:
                        palaa_takaisin()
                        
                    elif event.key == K_F1:
                        aloita_peli()
                    elif (event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4) and not Muuttujat.peliOhi:
                        valinta = valitse(event.key)

                        if valinta <= poyta.__len__() and not poyta[valinta - 1].onhaamu:
                            valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1])
                            valitse_kohde(valinta, poyta[valinta-1])
                                                    
                    elif event.key == K_5 and not Muuttujat.peliOhi:
                        valinta = 5
                        if korttejaPöydässä == huoneenKoko and Muuttujat.voiJuosta and (Muuttujat.skene != "Opastus" or Muuttujat.huoneNumero > 1):
                            pakene_huoneesta()
                            
                        elif korttejaPöydässä < 2:
                            uusi_huone()
                        else:
                            print("Et voi poistua huoneesta nyt.")
                            
                    elif len(nykyinenAse) > 0 and event.key == K_6 and not Muuttujat.peliOhi:
                        toista_sfx("click")
                        if Muuttujat.käytäAsetta:
                            Muuttujat.käytäAsetta = False
                        else:
                            Muuttujat.käytäAsetta = True
                                

                    if valinta > 0 and valinta <= len(poyta):
                        if not poyta[valinta - 1].onhaamu:
                            pelaa_kortti(valinta)

                elif event.type == MOUSEBUTTONDOWN:
                    if len(poyta) >= 4 and poyta[3].rect.collidepoint(pygame.mouse.get_pos()):
                        valinta = 4
                        valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1])
                        valitse_kohde(valinta, poyta[valinta-1])
                        pääIkkuna.Efektit.kortti_hover = 0
                    elif len(poyta) >= 3 and poyta[2].rect.collidepoint(pygame.mouse.get_pos()):
                        valinta = 3
                        valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1])
                        valitse_kohde(valinta, poyta[valinta-1])
                        pääIkkuna.Efektit.kortti_hover = 0
                    elif len(poyta) >= 2 and poyta[1].rect.collidepoint(pygame.mouse.get_pos()):
                        valinta = 2
                        valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1])
                        valitse_kohde(valinta, poyta[valinta-1])
                        pääIkkuna.Efektit.kortti_hover = 0
                    elif len(poyta) >= 1 and poyta[0].rect.collidepoint(pygame.mouse.get_pos()):
                        valinta = 1
                        valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1])
                        valitse_kohde(valinta, poyta[valinta-1])
                        pääIkkuna.Efektit.kortti_hover = 0
                    else:
                        valinta = -1

                    if pääIkkuna.juokse_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        if korttejaPöydässä == huoneenKoko and Muuttujat.voiJuosta and (Muuttujat.skene != "Opastus" or Muuttujat.huoneNumero > 1):
                            pakene_huoneesta()
                            
                        elif korttejaPöydässä < 2 and (Muuttujat.skene != "Opastus" or Muuttujat.huoneNumero > 4 or korttejaPöydässä == 0 or Muuttujat.huoneNumero == 0):
                            Muuttujat.voiJuosta = True
                            toista_sfx("click")
                            uusi_huone()
                      
                    if len(nykyinenAse) > 0 and not Muuttujat.peliOhi and (nykyinenAse[0].rect.collidepoint(pygame.mouse.get_pos()) or nykyinenAse[-1].rect.collidepoint(pygame.mouse.get_pos())):
                        toista_sfx("click")
                        if Muuttujat.käytäAsetta:
                            Muuttujat.käytäAsetta = False
                        else:
                            Muuttujat.käytäAsetta = True

                    if valinta > 0 and valinta <= len(poyta):
                        if not poyta[valinta - 1].onhaamu:
                            pelaa_kortti(valinta)
                            
                    if päävalikkoon_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        palaa_takaisin()
                        toista_sfx("click")
                    elif uusipeli_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        aloita_peli()
                        toista_sfx("click")

                elif event.type == MOUSEMOTION:
                    if len(poyta) >= 4 and poyta[3].rect.collidepoint(pygame.mouse.get_pos()) and not poyta[3].onhaamu:
                        pääIkkuna.Efektit.kortti_hover = 4
                    elif len(poyta) >= 3 and poyta[2].rect.collidepoint(pygame.mouse.get_pos()) and not poyta[2].onhaamu:
                        pääIkkuna.Efektit.kortti_hover = 3
                    elif len(poyta) >= 2 and poyta[1].rect.collidepoint(pygame.mouse.get_pos()) and not poyta[1].onhaamu:
                        pääIkkuna.Efektit.kortti_hover = 2
                    elif len(poyta) >= 1 and poyta[0].rect.collidepoint(pygame.mouse.get_pos()) and not poyta[0].onhaamu:
                        pääIkkuna.Efektit.kortti_hover = 1
                    elif pääIkkuna.juokse_nappi.rect.collidepoint(pygame.mouse.get_pos()) and (Muuttujat.voiJuosta):
                        pääIkkuna.Efektit.kortti_hover = 5
                    else:
                        pääIkkuna.Efektit.kortti_hover = 0

                    if pääIkkuna.päävalikkoon_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.pikavalinta_hover = 2
                    elif pääIkkuna.uusipeli_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.pikavalinta_hover = 1
                    else:
                        pääIkkuna.Efektit.pikavalinta_hover = 0
                        
            siirrä_kohteeseen()

        elif Muuttujat.skene == "Tekijät":

            for event in pygame.event.get():
                
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        palaa_takaisin()
                        
                elif event.type == MOUSEBUTTONDOWN:
                    if päävalikkoon_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        palaa_takaisin()
                        toista_sfx("click")

                elif event.type == MOUSEMOTION:
                    if pääIkkuna.päävalikkoon_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.pikavalinta_hover = 2
                    else:
                        pääIkkuna.Efektit.pikavalinta_hover = 0

        piirrä_kaikki()

# Täytä pohjavärillä, valitse piirettävät objektit ja päivitä ikkuna

def piirrä_kaikki():
    skene = Muuttujat.skene
    POHJA.fill((0,0,0))

    if skene == "PaaValikko":
        paaValikko.piirrä(POHJA)
        kampanja_nappi.piirrä(POHJA, 660, 480)
        pikapeli_nappi.piirrä(POHJA, 400, 480)
        opastus_nappi.piirrä(POHJA, 140, 480)
        asetukset_nappi.piirrä(POHJA, 400, 565)
        tekijät_nappi.piirrä(POHJA, 140, 565)
        lopeta_nappi.piirrä(POHJA, 660, 565)
        piirrä_valikon_kehys(pääIkkuna.Efektit.valikko_iso, pääIkkuna.Efektit.valikko_hover)
        
    elif skene == "Pikapeli" or skene == "Opastus":

        if skene == "Pikapeli": pikapeli_tausta.piirrä(POHJA)
        elif skene == "Opastus": opastus_tausta.piirrä(POHJA)
        
        if not Muuttujat.peliOhi:
            
            korttejaPöydässä = laske_poytakortit()
            piirrä_käden_kortit(poyta)
            
            herttaViimeisin = False
            if len(poistoPakka) > 0:
                if Muuttujat.viimeksiPelattu.maa == "hertta":
                    herttaViimeisin = True
            
            if len(nykyinenAse) > 0 and (not SiirtoAnimaatiot.piirrä_siirtyvä_kortti or herttaViimeisin) or nykyinenAse.__len__() > 1:
                piirrä_ase(nykyinenAse)
            
            if len(poistoPakka) > 0 and not (Muuttujat.käytäAsetta and len(nostoPakka) == 1):
                piirrä_nostopakka()
            
            if nykyinenAse.__len__() > 1:
                i = -1
                if nykyinenAse.__len__() > 2:
   
                    if SiirtoAnimaatiot.piirrä_siirtyvä_kortti and not herttaViimeisin and Muuttujat.käytäAsetta:
                        i -= 1
                        
                elif SiirtoAnimaatiot.piirrä_siirtyvä_kortti and not herttaViimeisin and Muuttujat.käytäAsetta:
                    i += 1

                if i < 0: 
                    # -2 = piirrä edellinen vihu
                    # -1 = piirrä päällimmäinen
                    # 0 = älä piirrä   
                    piirrä_viimeisin_lyöty(nykyinenAse[i])

            piirrä_poistettu_kortti(poistoPakka, nykyinenAse)
            
            if korttejaPöydässä < 2 and (skene != "Opastus" or Muuttujat.huoneNumero > 4 or korttejaPöydässä == 0 or Muuttujat.huoneNumero == 0):                
                piirrä_juoksunappi("etene")
            elif korttejaPöydässä == huoneenKoko and Muuttujat.voiJuosta and (skene != "Opastus" or Muuttujat.huoneNumero > 1):
                piirrä_juoksunappi("pakene")
            else:
                piirrä_juoksunappi("taistele")

            piirrä_napit()
            piirrä_tekstit(nostoPakka)
            piirrä_kortin_kehys(pääIkkuna.Efektit.kortti_hover)
            piirrä_pöydättävä_kortti()
            piirrä_pikavalinnan_kehys(pääIkkuna.Efektit.pikavalinta_hover)
            
            if pääIkkuna.SiirtoAnimaatiot.piirrä_siirtyvä_kortti:
                piirrä_siirtyvä_kortti()
            else:
                Muuttujat.aseestaPoistoon = 0
    
        else:
            peli_ohi()  
        
    elif skene == "Tekijät":
        tekijät_tausta.piirrä(POHJA)
        piirrä_napit(1)
        piirrä_pikavalinnan_kehys(pääIkkuna.Efektit.pikavalinta_hover)
    
    pygame.display.update()
    kello.tick(FPS) 
    
def käynnistä():
    
    while Muuttujat.käynnissä:
        
        piirrä_kaikki()
        peli_loop()
     
käynnistä()

pygame.quit()
sys.exit()