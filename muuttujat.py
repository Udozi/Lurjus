class Muuttujat():
    käynnissä = True
    peliOhi = False
    HP = 20
    maxHP = 20
    voiJuosta = True
    voiParantua = True
    skene = "PaaValikko"
    aseestaPoistoon = 0
    viimeksiPelattu = None
    huonenro = 1
    opastustauko = False
    käytäAsetta = True
    häviöt = 0
    finaalit = 0
    voitot = 0
    superVoitot = 0 # HP == maxHP
    voittoputki = 0
    nostoPinoKortit = 0
    
    # Seikkailu-tilan muuttujat:
    tyrmävalinta = "Vaikea"     # Helppo/vaikea
    vaikeusaste = 0             # Jokainen taso kasvattaa pakan mustia kortteja yhdellä. Pyöristetään alaspäin.
    helmiä = 0                  # Seikkailu-tilan valuutta
    haasteOtettu = False        # Ruutu-kauppiaan vaihtelu riippuu pelaajan valinnoista
    punaistenTaso = 0           # Jokainen taso kasvattaa pakan punaisia kortteja yhdellä
    palkinto = 1                # Saadut helmet tyrmän jälkeen
    esineet = []