import pygame

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