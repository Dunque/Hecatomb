import pygame as pg
from src.settings.settings import *
from src.settings.entitydata import *

vec = pg.math.Vector2


def collide_hit_rect(one, two):
    if hasattr(two,'hit_rect') and two.hit_rect:
        return one.hit_rect.colliderect(two.hit_rect)
    return one.hit_rect.colliderect(two.rect)


# Abstract class that can represent all humanoid entities (player, enemies)
class Character(pg.sprite.Sprite):
    def __init__(self, scene, x, y, animList, spriteGroup, entityData):
        self._layer = CHARACTER_LAYER
        pg.sprite.Sprite.__init__(self, spriteGroup)
        self.scene = scene
        self.entityData = entityData

        # Assign animations
        self.idleAnim = animList[0]
        self.walkAnim = animList[1]
        self.deathAnim = animList[2]

        # Set the idle animation as the starting one
        self.currentAnim = self.idleAnim

        # Get the first frame of the anim to set up the rect
        self.image = self.currentAnim.get_frame()
        self.original_image = self.image
        self.rect = self.image.get_rect()

        # ROtation and sprite flip
        self.rot = 0
        self.isFlipped = False

        # MOVEMENT
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        #Smaller rect, to soften collisions
        self.hit_rect = HIT_RECT.copy()
        self.hit_rect.center = self.rect.center

        # AIMING
        self.weaponOffsetX = 0
        self.weaponOffsetY = 0
        self.weapon = None

        # STATES
        self.state = None

    # Plays the death animation and destroys the entity
    def die(self):
        if self.deathAnim.current_frame == self.deathAnim.max_frame - 1:
            self.scene.ENEMY_DEATH_SOUND.play()
            self.kill()

    #Wall collision funtion, takes into account both rect and hit_rect
    def collide_with_walls(self, dir):
        collisions = list(self.scene.walls_SG) + list(self.scene.npc_SG)
        hits = pg.sprite.spritecollide(self, collisions, False, collide_hit_rect)
        if dir == 'x' and hits:
            if self.vel.x > 0:
                self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.
            if self.vel.x < 0:
                self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
            self.vel.x = 0
            self.hit_rect.centerx = self.pos.x
        if dir == 'y' and hits:
            if self.vel.y > 0:
                if hasattr(hits[0], 'hit_rect') and hits[0].hit_rect:
                    self.pos.y = hits[0].hit_rect.top - self.hit_rect.height / 2.0
                else:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2.0
            if self.vel.y < 0:
                if hasattr(hits[0], 'hit_rect') and hits[0].hit_rect:
                    self.pos.y = hits[0].hit_rect.bottom + self.hit_rect.height / 2.0
                else:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2.0
            self.vel.y = 0
            self.hit_rect.centery = self.pos.y

    def takeDamage(self, dmg, sound=None):
        if self.entityData.vulnerable and (self.state.name != "DODGING"):
            if sound:
                sound.play()
            self.entityData.takeDamage(dmg)

    def update(self):
        self.state.update()

        # MOVEMENT and collision
        self.pos += self.vel * self.scene.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.hit_rect.center

        # ANIMATION
        self.image = self.currentAnim.get_frame()
        self.image = pg.transform.flip(self.image, self.isFlipped, False)

        # Update entity's data
        self.entityData.update()