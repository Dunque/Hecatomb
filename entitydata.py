from settings import *

class CharacterStats:
    def __init__(self):
        #Life related stats
        self.isAlive = True
        self.maxHP = 100
        self.actualHP = self.maxHP

        #Movement and actions (dodge, charge, etc)
        self.moveSpeed = 100
        self.dodgeSpeed = 2 #It's a multiplier
        self.dodgeTimer = 35
        self.currentDodgeTimer = 0
        self.currentAttackTimer = 0
        #Stablishing invencibility frames in order to not be able
        #to be damaged several times in the span of miliseconds
        self.vulnerable = True
        self.iframes = 25
        self.currentIframe = 0

        #Death animation timers
        self.deathAnimTimer = 69
        self.currentDeathAnimTimer = 0

    def takeDamage(self, dmg):
        #Substracting damage received to actual health
        self.actualHP = self.actualHP - dmg
        self.vulnerable = False
        
        #Die
        if (self.actualHP <= 0):
            self.isAlive = False

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

class PlayerStats(CharacterStats):
    def __init__(self):
        super(PlayerStats, self).__init__()
        #Health
        self.maxHP = 100
        self.actualHP = self.maxHP

        #Movement
        self.speed = 300
        self.dodgeSpeed = 2 #It's a multiplier
        self.dodgeTimer = 35

class MobStats(CharacterStats):
    def __init__(self):
        super(MobStats, self).__init__()
        #Health
        self.maxHP = 100
        self.actualHP = self.maxHP

        #Movement
        self.speed = 300
        self.Attackspeed = 2 #It's a multiplier
        self.AttackTimer = 225
  