from src.entities.states.playerstates import PlayerGroundedState
from src.settings.settings import *


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CharacterStats:
    def __init__(self):
        #Life related stats
        self.isAlive = True
        self.maxHP = 100
        self.actualHP = self.maxHP

        #Movement and actions (dodge, charge, etc)
        self.moveSpeed = 100

        #Stablishing invencibility frames in order to not be able
        #to be damaged several times in the span of miliseconds
        self.vulnerable = True
        self.iframes = 10
        self.currentIframe = 0

    def takeDamage(self, dmg):
        #Substracting damage received to actual health
        self.actualHP = self.actualHP - dmg
        self.vulnerable = False

        #Die
        if (self.actualHP <= 0):
            self.isAlive = False

    def heal(self, hp):
        #Check in order to not heal more than the max hp allows
        if self.actualHP + hp > self.maxHP:
            self.actualHP = self.maxHP
        else:
            self.actualHP += hp

    def update(self):
        #If the character is invulneable, we start counting the
        #frames of invincibility that elapse in order to turn it
        #vulnerable again
        if (self.vulnerable == False):
            self.currentIframe += 1
            if (self.currentIframe >= self.iframes):
                self.vulnerable = True
        #If the character is vulnerable again, we reset the timer
        else:
            self.currentIframe = 0


class PlayerStats(CharacterStats, metaclass=SingletonMeta):
    def __init__(self, scene):
        super(PlayerStats, self).__init__()
        self.scene = scene
        #Health
        self.maxHP = 100
        self.actualHP = self.maxHP

        #Movement
        self.speed = 300
        self.dodgeSpeed = 2 #It's a multiplier
        self.dodgeTimer = 35

        #Dodge
        self.dodgeSpeed = 2 #It's a multiplier
        self.dodgeTimer = 60
        self.currentDodgeTimer = 0

        self.iframes = 20

        self.los_dineros = 0
        self.weapons = []

    def mas_dineros(self, dineros):
        self.scene.hud.time_dineros = None
        self.scene.hud.draw_dineros = True
        self.los_dineros += dineros
        self.los_dineros = round(self.los_dineros, 2)

    def menos_dineros(self, dineros):
        self.los_dineros -= dineros
        self.los_dineros = round(self.los_dineros, 2)

    def add_weapon(self, weapon):
        if weapon not in self.weapons:
            self.weapons.append(weapon)

    def load_weapons(self):
        return self.weapons

    def reset(self):
        self.weapons = []
        self.los_dineros = 0
        self.actualHP = self.maxHP
        self.isAlive = True

class HeraldStats(CharacterStats):
    def __init__(self):
        super(HeraldStats, self).__init__()
        #Health
        self.maxHP = 50
        self.actualHP = self.maxHP

        self.speed = 150
        self.AttackTimer = 60
        self.currentAttackTimer = 0
        
class WormStats(CharacterStats):
    def __init__(self):
        super(WormStats, self).__init__()
        #Health
        self.maxHP = 50
        self.actualHP = self.maxHP

        #Movement
        self.speed = 150
        self.AttackTimer = 100
        self.currentAttackTimer = 0

class KhanStats(CharacterStats):
    def __init__(self):
        super(KhanStats, self).__init__()
        #Health
        self.maxHP = 50
        self.actualHP = self.maxHP

        self.speed = 150
        self.AttackTimer = 60
        self.currentAttackTimer = 0

class EyeStats(CharacterStats):
    def __init__(self):
        super(EyeStats, self).__init__()
        #Health
        self.maxHP = 25
        self.actualHP = self.maxHP

        #Movement
        self.speed = 550
        self.AttackTimer = 100
        self.currentAttackTimer = 0