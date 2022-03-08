import pygame as pg
from math import pi, atan2
from src.entities.states.state import State

vec = pg.math.Vector2

class PlayerState(State):
    def __init__(self, character, name):
        super(PlayerState, self).__init__(character,name)

    def toState(self, targetState):
        self.character.state = targetState

    def handleInput(*args):
        pass


class PlayerGroundedState(PlayerState):
    def __init__(self, character, name):
        super(PlayerGroundedState, self).__init__(character,name)
        self.move = True

    def update(self):
        #Vibe check
        if (self.character.entityData.isAlive == False):
            self.toState(PlayerDyingState(self.character, "DYING"))

        if self.character.vel == vec(0, 0):
            self.character.currentAnim = self.character.idleAnim
        else:
            self.character.currentAnim = self.character.walkAnim
    
    def handleInput(self):
        self.character.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if self.move:
            if keys[pg.K_a]:
                self.character.vel.x = -self.character.entityData.speed
            if keys[pg.K_d]:
                self.character.vel.x = self.character.entityData.speed
            if keys[pg.K_w]:
                self.character.vel.y = -self.character.entityData.speed
            if keys[pg.K_s]:
                self.character.vel.y = self.character.entityData.speed
            if self.character.vel.x != 0 and self.character.vel.y != 0:
                self.character.vel *= 0.7071

            mouse = pg.mouse.get_pressed()
            # Left click
            if mouse[0]:
                if self.character.weapon is not None:
                    self.character.weapon.attack()
            elif not mouse[0]:
                if self.character.weapon is not None:
                    self.character.weapon.stop_attack()

            if keys[pg.K_SPACE]:
                self.character.dodgeDir = self.character.vel * \
                    self.character.entityData.dodgeSpeed
                self.toState(PlayerDodgingState(self.character, "DODGING"))

            ##DEBUG KEY TO KILL YOURSELF
            if keys[pg.K_0]:
                self.character.takeDamage(9999)

            #Weapon wheel
            if keys[pg.K_TAB]:
                self.character.show_menu = True
            else:
                self.character.show_menu = False

        if keys[pg.K_e]:
            self.character.interact = True
        else:
            self.character.interact = False

            #AMING MOVEMENT
            cam_moved = self.character.scene.camera.get_moved()

            mouse_x, mouse_y = pg.mouse.get_pos()

            mouse_x = mouse_x - cam_moved[0]
            mouse_y = mouse_y - cam_moved[1]

            rel_x, rel_y = mouse_x - self.character.rect.centerx, mouse_y - self.character.rect.centery
            self.character.rot = int((180 / pi) * -atan2(rel_y, rel_x))

            if 90 < self.character.rot + 180 < 270:
                self.character.isFlipped = False
                self.character.weaponOffsetX = -20
            else:
                self.character.isFlipped = True
                self.character.weaponOffsetX = 20

class PlayerDodgingState(PlayerState):

    def __init__(self, character, name):
        super(PlayerDodgingState, self).__init__(character, name)

    def update(self):
        self.character.currentAnim = self.character.dodgeAnim
        if self.character.weapon is not None:
            self.character.weapon.deactivate()
        if self.character.currentAnim.current_frame != self.character.currentAnim.max_frame - 1:
            self.character.vel = self.character.dodgeDir
        else:
            if self.character.weapon is not None:
                self.character.weapon.activate()
            self.toState(PlayerGroundedState(self.character, "GROUNDED"))
    
    def handleInput(self):
        pass


class PlayerDyingState(PlayerState):

    def __init__(self, character, name):
        super(PlayerDyingState, self).__init__(character, name)

    def update(self):
        self.character.vel = vec(0, 0)
        self.character.currentAnim = self.character.deathAnim
        if self.character.weapon:
            self.character.weapon.kill()
        self.character.die()

    def handleInput(self):
        pass
