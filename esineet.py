mahdollisetEsineet = []

class Esine():
    id = ""
    nimi = ""
    kuvaus1 = ""
    kuvaus2 = ""
    
    def __init__(self, id = "", nimi = "", kuvaus1 = "", kuvaus2 = ""):
        
        super().__init__()
        self.id = id
        self.nimi = nimi
        self.kuvaus1 = kuvaus1
        self.kuvaus2 = kuvaus2
        mahdollisetEsineet.append(self)
        
# Esineet ja niiden sijainti koodissa (#kommentti)
esine1 = Esine("savukaapu","Savukaapu","Voit paeta kesken huoneen.") #pelaa_kortti
esine2 = Esine("magneetti","Magneetti","Aloitat pelin satunnaisella","aseella nostopakasta.") #aloita_peli
esine3 = Esine("teleportti","Teleportti","Pako huoneesta sekoittaa nostopinon","ja poistaa sieltä vihollisen.") #pakene_huoneesta
esine4 = Esine("lyhty","Lyhty","Nostopinon ylin kortti paljastetaan.") #paljasta_kortti
esine5 = Esine("siivet","Siivet","Voit paeta kahdesti peräkkäin") #peli_loop
esine6 = Esine("amuletti","Amuletti","Kasvata aseitasi +1 jokaista", "ottamaasi haastetta kohden.") #aloita_peli
esine7 = Esine("kartta", "Kartta", "Voit suorittaa haasteita", "helpoissakin tyrmissä.") #aloita_peli
#esine8 = Esine("reppu", "Reppu", "Voit säilyttää yhtä", "asetta tai taikajuomaa") #pelaa_kortti ? peli_loop ?

