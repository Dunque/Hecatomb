import pygame as pg
from settings import *
from anim import *
from entitydata import *
from menus import WeaponMenu
from weapons import *
from enemyweapons import *
from bullets import *
from state import *
from enemystates import *
from hud import DialogoInGame

import math
from random import uniform

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


class Player(Character):
    def __init__(self, scene, x, y):

        # Aniamtion stuff
        idleAnim = Anim(scene.playerIdleSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 4)
        walkAnim = Anim(scene.playerWalkSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(scene.playerDeathSheet,
                         (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 7)
        dodgeAnim = Anim(scene.playerDodgeSheet,
                         (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 5)

        animList = [idleAnim, walkAnim, deathAnim, dodgeAnim, dodgeAnim]

        super(Player, self).__init__(scene, x, y, animList, (scene.all_sprites,scene.player_SG), PlayerStats())
        # AIMING
        self.weaponOffsetX = -20
        self.weaponOffsetY = -10
        self.weapon_slot = None
        self.weapon_menu = WeaponMenu(self.scene)
        self.scene.menus.append(self.weapon_menu)

        #Player should be active by default
        self.isActive = True

		self.interact = False
		DialogoInGame(scene, 'dialogo')
		self.state = PlayerGroundedState(self, "GROUNDED")

	def die(self):
		if self.weapon:
			self.weapon.kill()
		super(Player,self).die()
        self.interact = False
        self.state = PlayerGroundedState(self, "GROUNDED")

    def update(self):
        super(Player, self).update()
        self.state.handleInput()

        # WEAPON
        if self.weapon is not None:
            self.weapon.updatePos(self.pos.x - self.weaponOffsetX,
                                  self.pos.y - self.weaponOffsetY, self.rect)

    def change_weapon(self, slot):
        if self.weapon_slot != slot and slot == "top":
            if self.weapon is not None:
                self.weapon.deactivate()
            self.weapon = Gun(self.scene, self.pos.x - self.weaponOffsetX,
                              self.pos.y - self.weaponOffsetY)
            pg.mouse.set_visible(False)
            self.weapon.activate()
            self.weapon_slot = slot
        elif self.weapon_slot != slot and slot == "down":
            if self.weapon is not None:
                self.weapon.deactivate()
                pg.mouse.set_visible(True)
                self.weapon_slot = slot
        elif self.weapon_slot != slot and slot == "right":
            if self.weapon is not None:
                self.weapon.deactivate()
            self.weapon = Sword(self.scene, self.pos.x -
                                self.weaponOffsetX, self.pos.y - self.weaponOffsetY)
            pg.mouse.set_visible(True)
            self.weapon.activate()
            self.weapon_slot = slot
        elif self.weapon_slot != slot and slot == "left":
            if self.weapon is not None:
                self.weapon.deactivate()
            self.weapon = Shotgun(self.scene, self.pos.x -
                                  self.weaponOffsetX, self.pos.y - self.weaponOffsetY)
            pg.mouse.set_visible(False)
            self.weapon.activate()
            self.weapon_slot = slot


class Herald(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        walkAnim = Anim(scene.heraldWalkSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(scene.heraldDeathSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 5)
        animList = [walkAnim,walkAnim,deathAnim,walkAnim,walkAnim]

        super(Herald, self).__init__(scene, x, y, animList, (scene.mobs_SG) , HeraldStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.weaponOffsetX = -20
        self.weaponOffsetY = -10

        self.weapon = EnemyGun(self.scene, self, self.rect.centerx - self.weaponOffsetX, self.rect.centery - self.weaponOffsetY)
        self.state = EnemyGroundedState(self, "GROUNDED")


class Khan(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        walkAnim = Anim(scene.khanWalkSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(scene.khanDeathSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 6)
        animList = [walkAnim,walkAnim,deathAnim,walkAnim,walkAnim]

        super(Khan, self).__init__(scene, x, y, animList, (scene.mobs_SG) , KhanStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.weaponOffsetX = -20
        self.weaponOffsetY = -10

        self.weapon = EnemyShotgun(self.scene, self, self.rect.centerx - self.weaponOffsetX, self.rect.centery - self.weaponOffsetY)
        self.state = EnemyGroundedState(self, "GROUNDED")


class Worm(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        idleAnim = Anim(scene.wormIdleSheet, (90, 90), 10, 0, 9)
        walkAnim = Anim(scene.wormWalkSheet, (90, 90), 7, 0, 9)
        deathAnim = Anim(scene.wormDeathSheet, (90, 90), 4, 0, 8)
        attackAnim = Anim(scene.wormAttackSheet, (90, 90), 3, 0, 16)
        animList = [idleAnim, walkAnim, deathAnim, attackAnim, attackAnim]

        super(Worm, self).__init__(scene, x, y, animList, (scene.mobs_SG) , WormStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0

        self.hasAttacked = False
        self.attackOffset = vec(30,30)
        self.explosionWalls = Anim(scene.fire_ballExplosionSheet, (46, 46), 10, 0, 7)

    def aim(self):
        self.rot = (self.scene.player.pos - self.pos).angle_to(vec(1, 0))

    def move(self):
        self.acc = vec(self.entityData.speed).rotate(-self.rot)
        self.vel = self.acc * self.scene.dt * 15
        self.pos += self.vel * self.scene.dt + 0.5 * self.acc * self.scene.dt ** 2

    def stateUpdate(self):
        if (self.currentState == "GROUNDED"):
            self.currentAnim = self.walkAnim
            # Movement and aiming
            self.move()
            self.aim()
            return

        if (self.currentState == "DYING"):
            self.vel = vec(0, 0)
            self.currentAnim = self.deathAnim
            self.die()
            return

        if (self.currentState == "ATTACKING"):
            self.currentAnim = self.attackAnim
            if not self.hasAttacked and (self.entityData.currentAttackTimer >= self.entityData.AttackTimer):
                self.entityData.currentAttackTimer += 1
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + self.attackOffset.rotate(-self.rot)
                if self.rot <= -90 or self.rot >= 90:
                    dir = vec(dir.x * 1, dir.y * -1)
                    pos = self.pos + vec(self.attackOffset.x, self.attackOffset.y * -1).rotate(self.rot)
                explosion_pos=self.pos + (self.scene.player.pos - self.pos)
                Explosion(self.scene, pos, self.explosionWalls, self.scene.player_SG,scale=3, dealsDamage=True, damage=1)
                self.hasAttacked = True
            elif (self.entityData.currentAttackTimer <= self.entityData.AttackTimer):
                self.entityData.currentAttackTimer += 1
                self.vel = vec(0, 0)
            else:
                self.currentState="GROUNDED"
                self.entityData.currentAttackTimer = 0
                self.hasAttacked = False
            return


class Wall(pg.sprite.Sprite):
    def __init__(self, scene, x, y, tileset):
        self._layer = WALL_LAYER
        self.groups = scene.all_sprites, scene.walls_SG
        pg.sprite.Sprite.__init__(self, self.groups)

        self.scene = scene
        self.image = tileset
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)

        #tilemap position
        self.x = x
        self.y = y

        #Global position
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Floor(pg.sprite.Sprite):
    def __init__(self, scene, x, y, tileset):
        self._layer = FLOOR_LAYER
        self.groups = scene.all_sprites, scene.floors_SG
        pg.sprite.Sprite.__init__(self, self.groups)

        self.scene = scene
        self.image = tileset
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)

        #tilemap position
        self.x = x
        self.y = y

        #Global position
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Door(Wall):
    def __init__(self, scene, x, y, tileset):
        self.origImage = tileset
        super(Door,self).__init__(scene,x,y,tileset)

    def open(self):
        # In order to open the door we remove the image and
        # remove it from "walls" group
        self.scene.walls_SG.remove(self)
        self.scene.all_sprites.remove(self)

    def close(self):
        # In order to close the door we add the image and
        # add it to the "walls" group
        self.scene.walls_SG.add(self)
        self.scene.all_sprites.add(self)

        self.groups = self.scene.all_sprites, self.scene.walls_SG

        self.image = self.origImage
