import pygame as pg
from math import pi, atan2
from src.weapons.bullets import Explosion
from src.entities.states.state import State
from src.settings.settings import *

vec = pg.math.Vector2

class EnemyState(State):
    def __init__(self, character, name):
        super(EnemyState, self).__init__(character,name)
    
    def toState(self, targetState):
        self.character.state = targetState


class EnemyGroundedState(EnemyState):
    def __init__(self, character, name):
        super(EnemyGroundedState, self).__init__(character, name)

    def update(self):
        #Vibe check
        if (self.character.entityData.isAlive == False):
            self.toState(EnemyDyingState(self.character, "DYING"))

        self.character.currentAnim = self.character.walkAnim
        #MOVE
        self.character.acc = vec(self.character.entityData.speed).rotate(-self.character.rot)
        self.character.vel = self.character.acc * self.character.scene.dt * 15
        self.character.pos += self.character.vel * self.character.scene.dt + 0.5 * self.character.acc * self.character.scene.dt ** 2

        #AIM
        self.character.rot = (self.character.scene.player.pos - self.character.pos).angle_to(vec(1, 0))
        if 90 < self.character.rot + 180 < 270:
            self.character.isFlipped = False
            self.character.weaponOffsetX = -20
        else:
            self.character.isFlipped = True
            self.character.weaponOffsetX = 20

        if self.character.weapon:
            self.character.weapon.updatePos(self.character.rect.centerx - self.character.weaponOffsetX,
                                self.character.rect.centery - self.character.weaponOffsetY, self.character.rect)
            self.character.weapon.attack()
        else:
            if pg.sprite.spritecollide(self.character, self.character.scene.player_SG, False):
                self.toState(EnemyAttackingState(self.character, "ATTACKING"))

class EnemyDyingState(EnemyState):

    def __init__(self, character, name):
        super(EnemyDyingState, self).__init__(character, name)

    def update(self):
        self.character.vel = vec(0, 0)
        self.character.currentAnim = self.character.deathAnim
        if self.character.weapon:
            self.character.weapon.kill()
        self.character.die()

    def handleInput(self):
        pass


class EnemyAttackingState(EnemyState):

    def __init__(self, character, name):
        super(EnemyAttackingState, self).__init__(character, name)

    def update(self):
        #Vibe check
        if (self.character.entityData.isAlive == False):
            self.toState(EnemyDyingState(self.character, "DYING"))

        self.character.currentAnim = self.character.attackAnim
        if self.character.currentAnim.current_frame == self.character.currentAnim.max_frame - 5:
            self.character.vel = vec(0, 0)
            self.character.acc = vec(0, 0)


            dir = vec(1, 0).rotate(-self.character.rot)
            pos = self.character.pos + self.character.attackOffset.rotate(-self.character.rot)
            if self.character.rot <= -90 or self.character.rot >= 90:
                dir = vec(dir.x * 1, dir.y * -1)
                pos = self.character.pos + vec(self.character.attackOffset.x,
                        self.character.attackOffset.y * -1).rotate(self.character.rot)
            
            Explosion(self.character.scene, pos, self.character.explosionWalls,
                        self.character.scene.player_SG, scale=3, dealsDamage=True, damage=10)

        elif self.character.currentAnim.current_frame == self.character.currentAnim.max_frame - 1:
            self.toState(EnemyGroundedState(self.character, "GROUNDED"))

    def handleInput(self):
        pass


class KamikazeGroundedState(EnemyState):
    def __init__(self, character, name):
        super(KamikazeGroundedState, self).__init__(character, name)

    def update(self):
        #Vibe check
        if (self.character.entityData.isAlive == False):
            self.toState(KamikazeDyingState(self.character, "DYING"))

        self.character.currentAnim = self.character.walkAnim
        #MOVE
        self.character.acc = vec(
            self.character.entityData.speed).rotate(-self.character.rot)
        self.character.vel = self.character.acc * self.character.scene.dt * 15
        self.character.pos += self.character.vel * self.character.scene.dt + \
            0.5 * self.character.acc * self.character.scene.dt ** 2

        #AIM
        self.character.rot = (
            self.character.scene.player.pos - self.character.pos).angle_to(vec(1, 0))
        if 90 < self.character.rot + 180 < 270:
            self.character.isFlipped = False
            self.character.weaponOffsetX = -20
        else:
            self.character.isFlipped = True
            self.character.weaponOffsetX = 20

        #If this enemy collides with you, it also explodes
        if pg.sprite.spritecollide(self.character, self.character.scene.player_SG, False):
            self.character.entityData.isAlive = False


class KamikazeDyingState(EnemyDyingState):

    def __init__(self, character, name):
        super(KamikazeDyingState, self).__init__(character, name)

    def update(self):

        Explosion(self.character.scene, self.character.pos, self.character.explosionWalls,
                  self.character.scene.player_SG, scale=6, dealsDamage=True, damage=40)
        #EXPLOSION_SOUND.play()
        Explosion(self.character.scene, self.character.pos, self.character.explosionWalls,
                self.character.scene.mobs_SG, scale=6, dealsDamage=True, damage=40)
        super(KamikazeDyingState, self).update()

    def handleInput(self):
        pass
