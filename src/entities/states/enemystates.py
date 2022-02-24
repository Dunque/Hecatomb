import pygame as pg
from math import pi, atan2
from src.entities.states.state import State

vec = pg.math.Vector2

class EnemyState(State):
    def __init__(self, character, name):
        super(EnemyState, self).__init__(character,name)
    
    def toState(self, targetState):
        self.character.state.onExitState()
        self.character.state = targetState
        self.character.state.onEnterState()


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

        self.character.weapon.updatePos(self.character.rect.centerx - self.character.weaponOffsetX,
                              self.character.rect.centery - self.character.weaponOffsetY, self.character.rect)
        self.character.weapon.attack()


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