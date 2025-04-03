class Muuttujat():
    käynnissä = True
    peliOhi = False
    HP = 20
    maxHP = 20
    voiJuosta = True
    huoneitaViimePaosta = 0
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
    huoneenKoko = 4
    
    # Seikkailu-tilan muuttujat:
    tyrmävalinta = "Vaikea"     # Helppo/vaikea
    vaikeusaste = 0             # Jokainen taso kasvattaa pakan mustia kortteja yhdellä. Pyöristetään alaspäin.
    helmiä = 1                  # Seikkailu-tilan valuutta
    haasteOtettu = False        # Ruutu-kauppiaan vaihtelu riippuu pelaajan valinnoista
    punaistenTaso = 0           # Jokainen taso kasvattaa pakan punaisia kortteja yhdellä
    amuletinVoima = 0           # Jokainen taso kasvattaa pakan aseita yhdellä
    palkinto = 1                # Saadut helmet tyrmän jälkeen
    esineet = []
    tarjottuHaaste = None
    valittuHaaste = None
    pakojaPeräkkäin = 0
    