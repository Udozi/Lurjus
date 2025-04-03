haasteet = []

class Haaste():
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
        haasteet.append(self)

haaste1 = Haaste("palkkiometsästäjä","Palkkiometsästäjä","nostopakkaan sekoitetaan","suuruinen vihollinen.")
haaste2 = Haaste("muuttuvaLabyrintti","Muuttuva labyrintti","voit pelata samasta","huoneesta vain 2 korttia.")
haaste3 = Haaste("hermomyrkky","Hermomyrkky","otat kaksinkertaista vahinkoa", "ilman asetta.")
haaste4 = Haaste("tulvivaLattia","Tulviva lattia","sinun pitää pakojen välissä","läpäistä kaksi huonetta.")
haaste5 = Haaste("pelkokerroin", "Pelkokerroin", "sinun on aina käytettävä", "asettasi.")
haaste6 = Haaste("taikamuuri", "Taikamuuri", "aseiden alkukestävyys on", "2 x niiden voima.")
haaste7 = Haaste("ahtaatHuoneet", "Ahtaat huoneet", "huoneen koko on 3 korttia,", "mutta voit paeta kahdesti peräkkäin.")
haaste8 = Haaste("mustasukkaisuus", "Mustasukkaisuus", "hylätty käyttämätön ase vahingoittaa", "sinua 2 x voimansa verran.")
