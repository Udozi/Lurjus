import random, os, pääIkkuna, math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 
from pygame.locals import *

from grafiikka import *
from kortti import *
from muuttujat import *
from ase import *
from pääIkkuna import *
from äänet import *
from kauppias import *
from haasteet import *
from esineet import *

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

"""
Scoundrel-pelin haasteita ja niiden sijainti koodissa:
Palkkiometsästäjä - pakkaan sekoitetaan ylimääräinen iso vihollinen (aloita_peli)
Muuttuva labyrintti - huone vaihtuu, kun jäljellä on 2 korttia (pelaa_kortti)
Hermomyrkky - paljain käsin otettu vahinko x2 (pelaa_kortti)
Tulviva lattia - paon jälkeen pitää selvittää 2 huonetta ennen seuraavaa pakoa (peli_loop)
Pelkokerroin - asetta on pakko käyttää (peli_loop)
Taikamuuri - aseen alkukestävyys on 2 x aseen voima (ase.py)
Ahtaat huoneet - huoneen koko 3 (aloita_peli)
(skaalautuvan ui:n jälkeen: Tilavat huoneet - huoneen koko 5 (aloita_peli))
Mustasukkaisuus - käyttämätön ase vahingoittaa pelaajaa voima x2 verran (pelaa_kortti)
"""

nostoPakka = []
poistoPakka = []
poyta = []
nykyinenAse = []

kauppiaat = []

def esinelöytyy(id):
    
    if Muuttujat.skene == "Seikkailu":
    
        if len(Muuttujat.esineet) > 0:
            
            if Muuttujat.esineet[0].id == id:
                return True
            
            if len(Muuttujat.esineet) > 1:
                if Muuttujat.esineet[1].id == id: return True
            
    return False

# Yhden kortin siirtäminen nostopakasta pöydälle
def paljasta_kortti():

    if not Muuttujat.opastustauko: poista_haamukortit()
    
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
    
    Muuttujat.nostoPinoKortit = len(nostoPakka)

    return

def hylkaa_ase():
    
    Muuttujat.aseestaPoistoon = nykyinenAse.__len__()
    SiirtoAnimaatiot.vanha_ase = nykyinenAse[0]
    SiirtoAnimaatiot.vanha_vihu = nykyinenAse[-1]
    SiirtoAnimaatiot.piirrä_vanha_ase = True
    SiirtoAnimaatiot.piirrä_vanha_vihu = True
    poistoPakka.extend(nykyinenAse)
    nykyinenAse.clear()
    
    return

def pelaa_kortti(i):
    
    SiirtoAnimaatiot.piirrä_pelattava_kortti = False
    SiirtoAnimaatiot.viimeisin_siirtyvä = "pelattu"
    pelattavaKortti = poyta[i-1]
    Muuttujat.viimeksiPelattu = pelattavaKortti
    vaikutus = pelattavaKortti.vaikutus()
    haamukortti = Kortti()
    haamukortti.luo_kortti("hertta",0,True)
    poyta[i-1] = haamukortti
  
    # Jos pelattu kortti on ruutu (=ase)
    if type(vaikutus) is not int:
        
        if len(nykyinenAse) > 0: 
            
            if Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "mustasukkaisuus" and len(nykyinenAse) == 1:
                hpMuutos = - nykyinenAse[0].voima * 2
                toista_sfx("damage")
                Muuttujat.HP += hpMuutos 

            hylkaa_ase()
                                     
        uusiAse = vaikutus
        nykyinenAse.append(uusiAse)
        
        if Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "taikamuuri":
            nykyinenAse[0].kestavyys = nykyinenAse[0].voima * 2
        
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
                if Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "hermomyrkky": hpMuutos *= 2
                toista_sfx("damage")
            else:
                toista_sfx("denied")
            
        Muuttujat.HP = Muuttujat.HP + hpMuutos
        Muuttujat.voiJuosta = False
        
    korttejaPöydässä = laske_poytakortit()
    
    if ((esinelöytyy("savukaapu") and (Muuttujat.huoneitaViimePaosta > 0 or Muuttujat.huonenro < 3)) or korttejaPöydässä < 2 and (Muuttujat.skene != "Opastus" or Muuttujat.huonenro > 4 or korttejaPöydässä == 0 or Muuttujat.huonenro == 0)) or (korttejaPöydässä < 3 and Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "muuttuvaLabyrintti"):
        Muuttujat.voiJuosta = True
    
    if korttejaPöydässä == 0:
        Muuttujat.voiParantua = True
    
    if Muuttujat.HP > Muuttujat.maxHP:
        Muuttujat.HP = Muuttujat.maxHP
    
    korttejaJaljella = nostoPakka.__len__() + korttejaPöydässä
    if Muuttujat.HP < 1 or korttejaJaljella == 0:
        Muuttujat.peliOhi = True
     
    # Voittolaskuri ja voittoputkilaskuri. Häviö nollaa putken, finaali ei
        if Muuttujat.HP < 1: 
            if len(nostoPakka) == 0: 
                Muuttujat.finaalit += 1
                Muuttujat.palkinto -= 1

            else: 
                Muuttujat.häviöt += 1
                Muuttujat.voittoputki = 0
        
        elif Muuttujat.HP == Muuttujat.maxHP: 
            Muuttujat.superVoitot += 1
            Muuttujat.voittoputki += 1
            Muuttujat.palkinto += 1
        
        else: 
            Muuttujat.voitot += 1
            Muuttujat.voittoputki += 1
            
        Muuttujat.helmiä += Muuttujat.palkinto

    if Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "muuttuvaLabyrintti" and korttejaPöydässä < 3 and len(nostoPakka) > 0:
        pakene_huoneesta()
  
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

    SiirtoAnimaatiot.piirrä_pakokortit = True
    SiirtoAnimaatiot.piirrä_pakokortti1 = not poyta[0].onhaamu
    SiirtoAnimaatiot.piirrä_pakokortti2 = not poyta[1].onhaamu
    SiirtoAnimaatiot.piirrä_pakokortti3 = not poyta[2].onhaamu
    if len(poyta) > 3:
        SiirtoAnimaatiot.piirrä_pakokortti4 = not poyta[3].onhaamu
    
    if Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "muuttuvaLabyrintti" and laske_poytakortit() == 2:
        Muuttujat.voiJuosta = True
        Muuttujat.huoneitaViimePaosta += 1
    
    else: 
        Muuttujat.voiJuosta = False
        Muuttujat.huoneitaViimePaosta = 0 
        Muuttujat.pakojaPeräkkäin += 1
    
    random.shuffle(poyta)
    poista_haamukortit()
    poista_haamukortit()
    
    nostoPakka[:0] = poyta    
    poyta.clear()
    
    toista_sfx("click")
    while SiirtoAnimaatiot.piirrä_pakokortit:
        siirrä_nostopakkaan()
        piirrä_kaikki()
    
    if esinelöytyy("teleportti"):
        random.shuffle(nostoPakka)
    
    uusi_huone()
    return

def peli_ohi():

    SiirtoAnimaatiot.piirrä_pelattava_kortti = False
    SiirtoAnimaatiot.piirrä_pöydättävä_kortti = False
    pisteet = Muuttujat.HP    
    
    # Pisteiden lasku pelin hävittyä
    if Muuttujat.HP < 1:
        nostoPakka.extend(poyta)
        poyta.clear()
        
        for k in nostoPakka:
            if k.maa == "pata" or k.maa == "risti":
                pisteet -= k.arvo
    
    # Pisteiden lasku pelin voitettua    
    if Muuttujat.HP > 0:

        viimeinenKortti = poistoPakka[-1]
        
        if viimeinenKortti.maa == "hertta" and Muuttujat.HP == Muuttujat.maxHP: 
            pisteet += viimeinenKortti.arvo 
        
    piirrä_pisteet(pisteet)   

def nollaa_seikkailu():
    
    Muuttujat.skene = "Kauppa"
    Muuttujat.maxHP = 20
    Muuttujat.HP = Muuttujat.maxHP
    Muuttujat.vaikeusaste = 0
    Muuttujat.helmiä = 1
    Muuttujat.punaistenTaso = 0
    Muuttujat.amuletinVoima = 0
    Muuttujat.esineet.clear()
    Muuttujat.valittuHaaste = None       
            
def nollaa_peli():

    if not (Muuttujat.skene == "Seikkailu" or Muuttujat.skene == "ValitseTyrmä") or Muuttujat.tyrmävalinta == "Helppo": 
        Muuttujat.HP = Muuttujat.maxHP
        
    nostoPakka.clear()
    poyta.clear()
    poistoPakka.clear()
    nykyinenAse.clear()
    nollaa_korttien_paikat()

    Muuttujat.peliOhi = False
    Muuttujat.voiParantua = True
    
    if Muuttujat.skene == "Opastus":
        Muuttujat.voiJuosta = False
        Muuttujat.opastustauko = True
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
        
        Muuttujat.huonenro = 1
    
    elif Muuttujat.skene == "Seikkailu":
        
        if Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "ahtaatHuoneet": Muuttujat.huoneenKoko = 3
        else: Muuttujat.huoneenKoko = 4
        
        if Muuttujat.tyrmävalinta == "Helppo": 
            Muuttujat.vaikeusaste += 0.5
            Muuttujat.haasteOtettu == False
            Muuttujat.palkinto = 1
            
            if not esinelöytyy("kartta"): Muuttujat.valittuHaaste = None
                    
        else:
            Muuttujat.vaikeusaste += 1 
            Muuttujat.palkinto = 2
            
        if Muuttujat.valittuHaaste != None:
            Muuttujat.palkinto += 1
        
        for m in maat:
            for a in range(korttienMaara[m]):
                
                uusiKortti = Kortti()
                if m == "risti" or m == "pata":
                    kortinSuuruus = min(a + 1 + math.floor(Muuttujat.vaikeusaste), 20)
                    uusiKortti.luo_kortti(m, kortinSuuruus)
                else: 
                    kortinSuuruus = min(a + 2 + Muuttujat.punaistenTaso, 20)
                    
                    if m == "ruutu" and esinelöytyy("amuletti"):
                        kortinSuuruus = min(kortinSuuruus + Muuttujat.amuletinVoima, 20)
                    
                    uusiKortti.luo_kortti(m, kortinSuuruus)
                nostoPakka.append(uusiKortti)
        
        if Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "palkkiometsästäjä":
            kortinSuuruus = min(14 + math.floor(Muuttujat.vaikeusaste), 20)
            haasteKortti = Kortti()
            haasteKortti.luo_kortti("pata", kortinSuuruus)
            nostoPakka.append(haasteKortti)
                
        random.shuffle(nostoPakka)
        Muuttujat.huonenro = 1
        
        if esinelöytyy("magneetti"):
            i = -1
            while len(nykyinenAse) == 0:
                if nostoPakka[i].maa == "ruutu":
                    nykyinenAse.append(nostoPakka[i].vaikutus())
                    nostoPakka.pop(i)
                    Muuttujat.voiJuosta = True                    
                else: i -= 1
    
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
        
        Muuttujat.huonenro = -1 # Opastuksen dialogin tahdittamiseen
        
    uusi_huone()
    peli_loop()


def uusi_huone():
    
    Muuttujat.huonenro += 1
    Muuttujat.voiParantua = True
    
    if Muuttujat.voiJuosta:
        Muuttujat.pakojaPeräkkäin = 0
    
    SiirtoAnimaatiot.piirrä_pelattava_kortti = False  
    nollaa_korttien_paikat() 
    
    jäljelleJääneet = []
    
    for i in range(len(poyta)):
        if not poyta[i].onhaamu:
            jäljelleJääneet.append(i)
            
            if len(jäljelleJääneet) > 1:
                SiirtoAnimaatiot.jäänyt_kortti2_sijX = 25 + i * 150
                SiirtoAnimaatiot.jäänyt_kortti2 = poyta[i]
                
            else:
                SiirtoAnimaatiot.jäänyt_kortti_sijX = 25 + i * 150
                SiirtoAnimaatiot.jäänyt_kortti = poyta[i]
    
    if len(jäljelleJääneet) > 0:
        SiirtoAnimaatiot.piirrä_jäänyt_kortti = True
        
        if len(jäljelleJääneet) > 1:
            SiirtoAnimaatiot.piirrä_jäänyt_kortti2 = True
    
    if not Muuttujat.opastustauko: poista_haamukortit()

    if not Muuttujat.opastustauko:
        while laske_poytakortit() < Muuttujat.huoneenKoko and nostoPakka.__len__() > 0:
            paljasta_kortti()
            
    else:
        for i in range(4):
            paljasta_kortti()
        Muuttujat.opastustauko = False
    
    if Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "tulvivaLattia" and Muuttujat.huoneitaViimePaosta < 2 and Muuttujat.huonenro > 3:
        Muuttujat.voiJuosta = False
        
    if (esinelöytyy("siivet") or (Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "ahtaatHuoneet")) and Muuttujat.pakojaPeräkkäin < 2:
        Muuttujat.voiJuosta = True
    elif esinelöytyy("siivet") and (Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "ahtaatHuoneet") and Muuttujat.pakojaPeräkkäin < 3:
        Muuttujat.voiJuosta = True
            
    SiirtoAnimaatiot.piirrä_pöydättävä_kortti = False

# Kauppaan siirryttäessä valitaan neljä kauppiasta pelitilanteen mukaan.
# Kauppiaiden myymät lumoukset, haasteet, kiroukset ja esineet arvotaan.
def valitse_kauppiaat():        
        
    if Muuttujat.HP < Muuttujat.maxHP / 2:
        Muuttujat.HP = math.floor(Muuttujat.maxHP / 2) 
    
    Muuttujat.valittuHaaste = None
    kauppiaat.clear()
    
    for i in range(4):
        uusiKauppias = Kauppias(sija=i+1)
        kauppiaat.append(uusiKauppias)
        
    KuvaValinnat.kauppias1 = True      
    KuvaValinnat.kauppias2 = True   
    KuvaValinnat.kauppias3 = True   
    KuvaValinnat.kauppias4 = True      

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
            
        case "ValitseTyrmä":
            uusiSkene = "PaaValikko"
            Muuttujat.skene = uusiSkene
            
        case "Seikkailu":
            # Tähän tulee myöhemmin varmistus
            uusiSkene = "PaaValikko"
            if not Muuttujat.peliOhi: nollaa_seikkailu()
            Muuttujat.skene = uusiSkene
            
        case "Kauppa":
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

                    if seikkailu_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        Muuttujat.skene = "Kauppa"
                        valitse_kauppiaat()
                                        
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

                    if seikkailu_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.valikko_iso = True
                        pääIkkuna.Efektit.valikko_hover = 3
                                        
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
                        
                    elif sano_lurjus_nappi.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mixer.get_busy():
                        n = random.randrange(1,9)
                        äänenNimi = "lurjus" + str(n)
                        toista_sfx(äänenNimi)
                                        
                    elif lopeta_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        pääIkkuna.Efektit.valikko_iso = False
                        pääIkkuna.Efektit.valikko_hover = 3
                    else:
                        pääIkkuna.Efektit.valikko_hover = 0
                        
        
        elif Muuttujat.skene == "ValitseTyrmä" :
            for event in pygame.event.get():

                if event.type == QUIT:
                    Muuttujat.käynnissä = False

                elif event.type == MOUSEBUTTONDOWN:
                    
                    if vaikea_nappi.rect.collidepoint(pygame.mouse.get_pos()):                        
                        mask = pygame.mask.from_surface(vaikea_nappi.image)
                        
                        if mask.get_at((event.pos[0]-vaikea_nappi.rect.x, event.pos[1]-vaikea_nappi.rect.y)):
                            Muuttujat.skene = "Seikkailu"
                            Muuttujat.tyrmävalinta = "Vaikea"
                            toista_sfx("click")
                            aloita_peli()
                                                    
                    elif helppo_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        mask = pygame.mask.from_surface(helppo_nappi.image)
                        
                        if mask.get_at((event.pos[0]-helppo_nappi.rect.x, event.pos[1]-helppo_nappi.rect.y)):
                            Muuttujat.skene = "Seikkailu" 
                            Muuttujat.tyrmävalinta = "Helppo"
                            toista_sfx("click")
                            aloita_peli()

                        
                    elif päävalikkoon_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        palaa_takaisin()
                        toista_sfx("click")
                        
                elif event.type == MOUSEMOTION:
 
                    if vaikea_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        KuvaValinnat.vaikea_ovi = True
                        KuvaValinnat.helppo_ovi = False
                        
                    elif helppo_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        KuvaValinnat.vaikea_ovi = False
                        KuvaValinnat.helppo_ovi = True
                    else:
                        KuvaValinnat.vaikea_ovi = False
                        KuvaValinnat.helppo_ovi = False
                    
                elif event.type == KEYDOWN:
                                            
                        if event.key == K_ESCAPE:
                            palaa_takaisin()
                            
        
        elif Muuttujat.skene == "Kauppa":
            for event in pygame.event.get():
                if event.type == QUIT:
                    Muuttujat.käynnissä = False

                elif event.type == MOUSEBUTTONDOWN:
                    
                    if kauppias1_nappi.rect.collidepoint(pygame.mouse.get_pos()) and KuvaValinnat.kauppias1:                        
                        
                        if kauppiaat[0].asioi():
                            toista_sfx("click")
                            kauppiaat[0].vaihda_tila("myyty")
                            KuvaValinnat.kauppias1 = False
                            
                        else:
                            toista_sfx("denied")

                                                    
                    elif kauppias2_nappi.rect.collidepoint(pygame.mouse.get_pos()) and KuvaValinnat.kauppias2:
                        
                        if kauppiaat[1].asioi():
                            toista_sfx("click")
                            kauppiaat[1].vaihda_tila("myyty")
                            KuvaValinnat.kauppias2 = False
                            
                        else:
                            toista_sfx("denied")

                    elif kauppias3_nappi.rect.collidepoint(pygame.mouse.get_pos()) and KuvaValinnat.kauppias3:
                        
                        if kauppiaat[2].asioi():
                            toista_sfx("click")
                            kauppiaat[2].vaihda_tila("myyty")
                            KuvaValinnat.kauppias3 = False
                            
                        else:
                            toista_sfx("denied")
                            
                    elif kauppias4_nappi.rect.collidepoint(pygame.mouse.get_pos()) and KuvaValinnat.kauppias4:
                        
                        if kauppiaat[3].asioi():
                            toista_sfx("click")
                            kauppiaat[3].vaihda_tila("myyty")
                            KuvaValinnat.kauppias4 = False
                            
                        else:
                            toista_sfx("denied")

                    elif jatka_nappi.rect.collidepoint(pygame.mouse.get_pos()):                        
                        mask = pygame.mask.from_surface(jatka_nappi.image)
                        
                        if mask.get_at((event.pos[0]-jatka_nappi.rect.x, event.pos[1]-jatka_nappi.rect.y)):
                            Muuttujat.skene = "ValitseTyrmä"
                            KuvaValinnat.helppo_ovi = False
                            KuvaValinnat.vaikea_ovi = False
                            toista_sfx("click")
                            aloita_peli()
                        
                    elif päävalikkoon_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        palaa_takaisin()
                        toista_sfx("click")
                        
                elif event.type == MOUSEMOTION:
                    
                    if kauppias1_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                            kauppiaat[0].vaihda_tila("huomio")
                            kauppiaat[1].vaihda_tila("odottaa")
                            kauppiaat[2].vaihda_tila("odottaa")
                            kauppiaat[3].vaihda_tila("odottaa")
                            
                            if kauppiaat[0].tila != "myyty":
                                KuvaValinnat.kauppa_info_laatikko = True
                            
                    elif kauppias2_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                            kauppiaat[0].vaihda_tila("odottaa")
                            kauppiaat[1].vaihda_tila("huomio")
                            kauppiaat[2].vaihda_tila("odottaa")
                            kauppiaat[3].vaihda_tila("odottaa")
                            
                            if kauppiaat[1].tila != "myyty":
                                KuvaValinnat.kauppa_info_laatikko = True
                            
                    elif kauppias3_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                            kauppiaat[0].vaihda_tila("odottaa")
                            kauppiaat[1].vaihda_tila("odottaa")
                            kauppiaat[2].vaihda_tila("huomio")
                            kauppiaat[3].vaihda_tila("odottaa")
                            
                            if kauppiaat[2].tila != "myyty":
                                KuvaValinnat.kauppa_info_laatikko = True
                                
                    elif kauppias4_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                            kauppiaat[0].vaihda_tila("odottaa")
                            kauppiaat[1].vaihda_tila("odottaa")
                            kauppiaat[2].vaihda_tila("odottaa")
                            kauppiaat[3].vaihda_tila("huomio")
                            
                            if kauppiaat[3].tila != "myyty":
                                KuvaValinnat.kauppa_info_laatikko = True
                            
                    else:
                        kauppiaat[0].vaihda_tila("odottaa")
                        kauppiaat[1].vaihda_tila("odottaa")
                        kauppiaat[2].vaihda_tila("odottaa")
                        kauppiaat[3].vaihda_tila("odottaa")
                        KuvaValinnat.kauppa_info_laatikko = False
        
        elif Muuttujat.skene == "Pikapeli" or Muuttujat.skene == "Opastus" or Muuttujat.skene == "Seikkailu":

            for event in pygame.event.get():
                korttejaPöydässä = laske_poytakortit()
                
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    valinta = 0
                                        
                    if event.key == K_ESCAPE:
                        if not Muuttujat.peliOhi: 
                            Muuttujat.voittoputki = 0
                            Muuttujat.häviöt += 1
                        palaa_takaisin()
                        
                    elif event.key == K_F1 and (Muuttujat.skene != "Seikkailu" or Muuttujat.peliOhi):
                        
                        if not Muuttujat.peliOhi: 
                            Muuttujat.voittoputki = 0
                            Muuttujat.häviöt += 1
                        if Muuttujat.skene == "Seikkailu": nollaa_seikkailu()
                        aloita_peli()
                    elif (event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4) and not Muuttujat.peliOhi:
                        valinta = valitse(event.key)

                        if valinta <= poyta.__len__() and not poyta[valinta - 1].onhaamu:
                            valitse_viholliskortin_kohde(nykyinenAse, poyta[valinta-1])
                            valitse_kohde(valinta, poyta[valinta-1])
                                                    
                    elif event.key == K_5 and not Muuttujat.peliOhi:
                        valinta = 5
                        if korttejaPöydässä > 1 and Muuttujat.voiJuosta and (Muuttujat.skene != "Opastus" or Muuttujat.huonenro > 1):
                            pakene_huoneesta()
                            
                        elif korttejaPöydässä < 2 and (Muuttujat.skene != "Opastus" or Muuttujat.huonenro > 4 or korttejaPöydässä == 0 or Muuttujat.huonenro == 0):
                            Muuttujat.voiJuosta = True
                            Muuttujat.huoneitaViimePaosta += 1
                            uusi_huone()
                        else:
                            print("Et voi poistua huoneesta nyt.")
                            
                    elif event.key == K_7:
                        Muuttujat.tyrmävalinta = "Vaikea"
                        Muuttujat.skene = "Kauppa"
                        valitse_kauppiaat()
                            
                    elif len(nykyinenAse) > 0 and event.key == K_6 and not (Muuttujat.peliOhi or (Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "pelkokerroin")):
                        toista_sfx("click")
                        Muuttujat.käytäAsetta = not Muuttujat.käytäAsetta
                                
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
                        if korttejaPöydässä > 1 and Muuttujat.voiJuosta and (Muuttujat.skene != "Opastus" or Muuttujat.huonenro > 1):
                            toista_sfx("click")
                            pakene_huoneesta()
                            
                        elif korttejaPöydässä < 2 and (Muuttujat.skene != "Opastus" or Muuttujat.huonenro > 4 or korttejaPöydässä == 0 or Muuttujat.huonenro == 0):
                            Muuttujat.voiJuosta = True
                            Muuttujat.huoneitaViimePaosta += 1
                            toista_sfx("click")
                            uusi_huone()
                      
                    if len(nykyinenAse) > 0 and not (Muuttujat.peliOhi or (Muuttujat.valittuHaaste != None and Muuttujat.valittuHaaste.id == "pelkokerroin")) and (nykyinenAse[0].rect.collidepoint(pygame.mouse.get_pos()) or nykyinenAse[-1].rect.collidepoint(pygame.mouse.get_pos())):
                        toista_sfx("click")
                        if Muuttujat.käytäAsetta:
                            Muuttujat.käytäAsetta = False
                        else:
                            Muuttujat.käytäAsetta = True

                    if valinta > 0 and valinta <= len(poyta):
                        if not poyta[valinta - 1].onhaamu:
                            pelaa_kortti(valinta)
                            
                    if päävalikkoon_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        if not Muuttujat.peliOhi: 
                            Muuttujat.voittoputki = 0
                            Muuttujat.häviöt += 1
                            
                        if Muuttujat.skene == "Seikkailu" and (Muuttujat.nostoPinoKortit > 0 or not Muuttujat.peliOhi):
                            nollaa_seikkailu()
                            
                        palaa_takaisin()
                        toista_sfx("click")
                        
                    if kauppaan_nappi.rect.collidepoint(pygame.mouse.get_pos()):
                        Muuttujat.tyrmävalinta = "Vaikea"
                        Muuttujat.skene = "Kauppa"
                        valitse_kauppiaat()
                                                                
                    elif uusipeli_nappi.rect.collidepoint(pygame.mouse.get_pos()) and (Muuttujat.skene != "Seikkailu" or Muuttujat.peliOhi):
                        if not Muuttujat.peliOhi:
                            Muuttujat.voittoputki = 0
                            Muuttujat.häviöt += 1
                        if Muuttujat.skene == "Seikkailu":
                            nollaa_seikkailu()
                            valitse_kauppiaat()
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
        seikkailu_nappi.piirrä(POHJA, 660, 480)
        pikapeli_nappi.piirrä(POHJA, 400, 480)
        opastus_nappi.piirrä(POHJA, 140, 480)
        asetukset_nappi.piirrä(POHJA, 400, 565)
        tekijät_nappi.piirrä(POHJA, 140, 565)
        lopeta_nappi.piirrä(POHJA, 660, 565)
        piirrä_valikon_kehys(pääIkkuna.Efektit.valikko_iso, pääIkkuna.Efektit.valikko_hover)
        
    elif skene == "ValitseTyrmä":
        
        valitsetyrmä_tausta.piirrä(POHJA)
        if KuvaValinnat.helppo_ovi: 
            helppo_nappi.piirrä(POHJA)
            helppo_info.piirrä(POHJA)
        if KuvaValinnat.vaikea_ovi: 
            vaikea_nappi.piirrä(POHJA)
            vaikea_info.piirrä(POHJA)
        
        piirrä_tekstit()
        piirrä_napit(1)
        
    elif skene == "Kauppa":
        
        kauppa_tausta.piirrä(POHJA)
        piirrä_tekstit()
        if KuvaValinnat.kauppias1: 
            kauppias1_nappi.piirrä(POHJA)
            
            kauppias1_teksti.päivitä_teksti("Kasvata korttejasi",24)
            kauppias1_teksti.rect.center = (150, 400)            
            kauppias1_teksti.piirrä(POHJA)
            
            kauppias1_hinta.päivitä_teksti("Hinta: " + str(kauppiaat[0].hinta), 24)
            kauppias1_hinta.rect.center = (150, 450)
            kauppias1_hinta.piirrä(POHJA)
        
        if KuvaValinnat.kauppias2: 
            kauppias2_nappi.piirrä(POHJA)
            
            kauppias2_teksti.päivitä_teksti("Paranna terveyttäsi",24)
            kauppias2_teksti.rect.center = (335, 400)
            
            kauppias2_teksti.piirrä(POHJA)
            
            kauppias1_hinta.päivitä_teksti("Hinta: " + str(kauppiaat[1].hinta), 24)
            kauppias1_hinta.rect.center = (335, 450)
            kauppias1_hinta.piirrä(POHJA)
            
        if KuvaValinnat.kauppias3: 
            kauppias3_nappi.piirrä(POHJA)
            
            kauppias3_teksti.rect.center = (550, 400)
            kauppias3_teksti.päivitä_teksti("Ota haaste",24)
            kauppias3_teksti.piirrä(POHJA)
            
            kauppias3_hinta.päivitä_teksti("Palkkio: 1", 24)
            kauppias3_hinta.rect.center = (550, 450)
            kauppias3_hinta.piirrä(POHJA)
            
        if KuvaValinnat.kauppias4: 
            kauppias4_nappi.piirrä(POHJA)
                        
            if kauppiaat[3].toiminto == "myyEsine":
                kauppias4_teksti.rect.center = (740, 400)
                kauppias4_teksti.päivitä_teksti("Osta esine",24)
                kauppias4_teksti.piirrä(POHJA)
                
                kauppias4_hinta.päivitä_teksti("Hinta: " + str(kauppiaat[3].hinta), 24)
                kauppias4_hinta.rect.center = (740, 450)
                kauppias4_hinta.piirrä(POHJA)
                
            else: 
                kauppias4_teksti.rect.center = (740, 400)
                kauppias4_teksti.päivitä_teksti("Vaihda esine",24)
                kauppias4_teksti.piirrä(POHJA)
                
                kauppias4_hinta.päivitä_teksti("Hinta: " + str(kauppiaat[3].hinta), 24)
                kauppias4_hinta.rect.center = (740, 450)
                kauppias4_hinta.piirrä(POHJA)
            
            
        jatka_nappi.piirrä(POHJA)
        
        if KuvaValinnat.kauppa_info_laatikko:
            kauppa_info.piirrä(POHJA)
        
        for kauppias in kauppiaat:
            
            kauppias.piirrä(POHJA)
            
            if kauppias.tila == "huomio":
                
                kauppias_info_otsikko.päivitä_teksti(kauppias.info_otsikko, 36)
                kauppias_info_otsikko.rect.center = (300, 40)
                kauppias_info_otsikko.piirrä(POHJA)
                
                kauppias_info_rivi1.päivitä_teksti(kauppias.info_rivi1, 24)
                kauppias_info_rivi1.rect.center = (300, 70)
                kauppias_info_rivi1.piirrä(POHJA)
                
                kauppias_info_rivi2.päivitä_teksti(kauppias.info_rivi2, 24)
                kauppias_info_rivi2.rect.center = (300, 90)
                kauppias_info_rivi2.piirrä(POHJA)
                
        
        piirrä_napit(1)

        
    elif skene == "Pikapeli" or skene == "Opastus" or skene == "Seikkailu":

        if skene == "Pikapeli": pikapeli_tausta.piirrä(POHJA)
        elif skene == "Opastus": opastus_tausta.piirrä(POHJA)
        elif skene == "Seikkailu": seikkailu_tausta.piirrä(POHJA) # Seikkailu-tausta kehitteillä
        
        if not Muuttujat.peliOhi:
            
            korttejaPöydässä = laske_poytakortit()

            if SiirtoAnimaatiot.piirrä_jäänyt_kortti:
                piirrä_jäänyt_kortti()
                
            if SiirtoAnimaatiot.piirrä_jäänyt_kortti2:
                piirrä_jäänyt_kortti2()
            
            piirrä_pakokortit()
            
            piirrä_käden_kortit(poyta)
            
            herttaViimeisin = False
            if len(poistoPakka) > 0:
                if Muuttujat.viimeksiPelattu.maa == "hertta":
                    herttaViimeisin = True
            
            if len(nykyinenAse) > 0 and (not SiirtoAnimaatiot.piirrä_pelattava_kortti or herttaViimeisin) or nykyinenAse.__len__() > 1:
                piirrä_ase(nykyinenAse)
            
            if len(nostoPakka) > 0:
                
                if esinelöytyy("lyhty"):
                    
                    if not piirrä_pöydättävä_kortti or len(poyta) == Muuttujat.huoneenKoko:
                        nostoPakka[-1].image = KorttiKuvakkeet.valitse_kortin_kuvake(nostoPakka[-1])
                        nostoPakka[-1].rect.x = 25
                        nostoPakka[-1].rect.y = 355
                        nostoPakka[-1].piirrä(POHJA)
                        
                    elif len(nostoPakka) > 1: 
                        nostoPakka[-2].image = KorttiKuvakkeet.valitse_kortin_kuvake(nostoPakka[-2])
                        nostoPakka[-2].rect.x = 25
                        nostoPakka[-2].rect.y = 355
                        nostoPakka[-2].piirrä(POHJA)
                    
                else: piirrä_nostopakka()
                
                
            
            if nykyinenAse.__len__() > 1:
                i = -1
                if nykyinenAse.__len__() > 2:
   
                    if SiirtoAnimaatiot.piirrä_pelattava_kortti and not herttaViimeisin and Muuttujat.käytäAsetta:
                        i -= 1
                        
                elif SiirtoAnimaatiot.piirrä_pelattava_kortti and not herttaViimeisin and Muuttujat.käytäAsetta:
                    i += 1

                if i < 0: 
                    # -2 = piirrä edellinen vihu
                    # -1 = piirrä päällimmäinen
                    # 0 = älä piirrä   
                    piirrä_viimeisin_lyöty(nykyinenAse[i])

            piirrä_poistettu_kortti(poistoPakka, nykyinenAse)
            
            if korttejaPöydässä < 2 and (skene != "Opastus" or Muuttujat.huonenro > 4 or korttejaPöydässä == 0 or Muuttujat.huonenro == 0):                
                piirrä_juoksunappi("etene")
            elif korttejaPöydässä > 1 and Muuttujat.voiJuosta and (skene != "Opastus" or Muuttujat.huonenro > 1):
                piirrä_juoksunappi("pakene")
            else:
                piirrä_juoksunappi("taistele")
            
            # Seikkailussa ei ole uusi peli -nappia
            if Muuttujat.skene == "Seikkailu": piirrä_napit(1)
            else: piirrä_napit()
            
            piirrä_tekstit(nostoPakka)
            piirrä_kortin_kehys(pääIkkuna.Efektit.kortti_hover)

            piirrä_pöydättävä_kortti()
            piirrä_pikavalinnan_kehys(pääIkkuna.Efektit.pikavalinta_hover)
            
            if Muuttujat.aseestaPoistoon > 0: 
                piirrä_vanha_asepino()
            
            if SiirtoAnimaatiot.piirrä_pelattava_kortti:
                piirrä_pelattava_kortti()
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