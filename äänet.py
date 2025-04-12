import pygame

pygame.mixer.set_num_channels(8)
sfx = pygame.mixer.Channel(1)
voice = pygame.mixer.Channel(2)
lurjusVolume = 0.2

potion_ääni = pygame.mixer.Sound("sfx/potion.wav")
potion_ääni.set_volume(0.3)
hyökkäys_ääni = pygame.mixer.Sound("sfx/hyökkäys.wav")
hyökkäys_ääni.set_volume(0.5)
damage_ääni = pygame.mixer.Sound("sfx/damage.wav")
damage_ääni.set_volume(0.2)
kerää_ase_ääni = pygame.mixer.Sound("sfx/kerää_ase.wav")
kerää_ase_ääni.set_volume(0.5)
click_ääni = pygame.mixer.Sound("sfx/click.wav")
click_ääni.set_volume(0.2)
denied_ääni = pygame.mixer.Sound("sfx/denied.wav")
denied_ääni.set_volume(1.0)
lurjus1_ääni = pygame.mixer.Sound("sfx/lurjus1.wav")
lurjus1_ääni.set_volume(lurjusVolume)
lurjus2_ääni = pygame.mixer.Sound("sfx/lurjus2.wav")
lurjus2_ääni.set_volume(lurjusVolume)
lurjus3_ääni = pygame.mixer.Sound("sfx/lurjus3.wav")
lurjus3_ääni.set_volume(lurjusVolume)
lurjus4_ääni = pygame.mixer.Sound("sfx/lurjus4.wav")
lurjus4_ääni.set_volume(lurjusVolume)
lurjus5_ääni = pygame.mixer.Sound("sfx/lurjus5.wav")
lurjus5_ääni.set_volume(lurjusVolume)
lurjus6_ääni = pygame.mixer.Sound("sfx/lurjus6.wav")
lurjus6_ääni.set_volume(lurjusVolume)
lurjus7_ääni = pygame.mixer.Sound("sfx/lurjus7.wav")
lurjus7_ääni.set_volume(lurjusVolume)
lurjus8_ääni = pygame.mixer.Sound("sfx/lurjus8.wav")
lurjus8_ääni.set_volume(lurjusVolume)
lurjus9_ääni = pygame.mixer.Sound("sfx/lurjus9.wav")
lurjus9_ääni.set_volume(lurjusVolume)

def toista_sfx(sfx):
    match sfx:
        case "potion":
            potion_ääni.play()
        case "hyökkäys":
            hyökkäys_ääni.play()
        case "damage":
            damage_ääni.play()
        case "kerää_ase":
            kerää_ase_ääni.play()
        case "click":
            click_ääni.play()
        case "denied":
            denied_ääni.play()
        case "lurjus1":
            lurjus1_ääni.play()
        case "lurjus2":
            lurjus2_ääni.play()
        case "lurjus3":
            lurjus3_ääni.play()
        case "lurjus4":
            lurjus4_ääni.play()
        case "lurjus5":
            lurjus5_ääni.play()
        case "lurjus6":
            lurjus6_ääni.play()
        case "lurjus7":
            lurjus7_ääni.play()
        case "lurjus8":
            lurjus8_ääni.play()
        case "lurjus9":
            lurjus9_ääni.play()