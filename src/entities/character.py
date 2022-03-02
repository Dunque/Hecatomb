import pygame as pg
from src.settings.settings import *
from src.settings.entitydata import *

vec = pg.math.Vector2


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


# Abstract class that can represent all humanoid entities (player, enemies)
class Character(pg.sprite.Sprite):
    # TODO
    # Hay que añadir aqui al consturecotr de chjaracter el grupo de sprites
    # Hay que crear grupo jugador, grupo enemigos, gerupo objetos etc
    def __init__(self, scene, x, y, animList, spriteGroup, entityData):
        self._layer = CHARACTER_LAYER
        pg.sprite.Sprite.__init__(self, spriteGroup)
        self.scene = scene
        self.entityData = entityData

        # Assign animations
        self.idleAnim = animList[0]
        self.walkAnim = animList[1]
        self.deathAnim = animList[2]
        # Optional animations
        self.dodgeAnim = animList[3]
        self.attackAnim = animList[4]

        # Set the idle animation as the starting one
        self.currentAnim = self.idleAnim

        # Get the first frame of the anim to set up the rect
        self.image = self.currentAnim.get_frame()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        # Boolean to flip the sprite
        self.isFlipped = False

        # MOVEMENT
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        # Player hitbox is smaller
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rot = 0

        # AIMING
        self.weaponOffsetX = 0
        self.weaponOffsetY = 0
        self.weapon = None

        # DODGING
        self.dodgeDir = vec(0, 0)
        # ATTACK
        self.AttackDir = vec(0, 0)
        # STATES
        self.state = None

        #This boolean dictates if the character can move, aim, take damage, etc
        self.isActive = False

    # Plays the death animation and destroys the entity
    def die(self):
        self.entityData.currentDeathAnimTimer += 1
        if (self.entityData.currentDeathAnimTimer >= self.entityData.deathAnimTimer):
            ENEMY_DEATH_SOUND.play()
            self.kill()

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.scene.walls_SG, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.0
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.scene.walls_SG, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2.0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2.0
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def takeDamage(self, dmg):
        if self.isActive:
            if self.entityData.vulnerable and (self.state.name != "DODGING"):
                self.entityData.takeDamage(dmg)

    def update(self):
        if self.isActive:

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