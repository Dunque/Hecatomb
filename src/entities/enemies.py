import pygame as pg
from src.settings.settings import *
from src.sprites.anim import *
from src.settings.entitydata import *
from src.weapons.enemyweapons import *
from src.weapons.bullets import *
from src.entities.states.enemystates import *
from src.entities.character import *

vec = pg.math.Vector2


class Herald(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        walkAnim = Anim(scene.heraldWalkSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(scene.heraldDeathSheet,
                         (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 5)
        animList = [walkAnim, walkAnim, deathAnim, walkAnim, walkAnim]

        super(Herald, self).__init__(scene, x, y,
                                     animList, (scene.mobs_SG), HeraldStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.weaponOffsetX = -20
        self.weaponOffsetY = -10

        self.weapon = EnemyGun(self.scene, self, self.rect.centerx -
                               self.weaponOffsetX, self.rect.centery - self.weaponOffsetY)
        self.state = EnemyGroundedState(self, "GROUNDED")


class Khan(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        walkAnim = Anim(scene.khanWalkSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(
            scene.khanDeathSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 6)
        animList = [walkAnim, walkAnim, deathAnim, walkAnim, walkAnim]

        super(Khan, self).__init__(scene, x, y,
                                   animList, (scene.mobs_SG), KhanStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.weaponOffsetX = -20
        self.weaponOffsetY = -10

        self.weapon = EnemyShotgun(self.scene, self, self.rect.centerx -
                                   self.weaponOffsetX, self.rect.centery - self.weaponOffsetY)
        self.state = EnemyGroundedState(self, "GROUNDED")


class Worm(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        idleAnim = Anim(scene.wormIdleSheet, (90, 90), 10, 0, 9)
        walkAnim = Anim(scene.wormWalkSheet, (90, 90), 7, 0, 9)
        deathAnim = Anim(scene.wormDeathSheet, (90, 90), 4, 0, 8)
        attackAnim = Anim(scene.wormAttackSheet, (90, 90), 3, 0, 16)
        animList = [idleAnim, walkAnim, deathAnim, attackAnim, attackAnim]

        super(Worm, self).__init__(scene, x, y,
                                   animList, (scene.mobs_SG), WormStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0

        self.hasAttacked = False
        self.attackOffset = vec(30, 30)
        self.explosionWalls = Anim(
            scene.fire_ballExplosionSheet, (46, 46), 10, 0, 7)

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
                    pos = self.pos + \
                        vec(self.attackOffset.x,
                            self.attackOffset.y * -1).rotate(self.rot)
                explosion_pos = self.pos + (self.scene.player.pos - self.pos)
                Explosion(self.scene, pos, self.explosionWalls,
                          self.scene.player_SG, scale=3, dealsDamage=True, damage=1)
                self.hasAttacked = True
            elif (self.entityData.currentAttackTimer <= self.entityData.AttackTimer):
                self.entityData.currentAttackTimer += 1
                self.vel = vec(0, 0)
            else:
                self.currentState = "GROUNDED"
                self.entityData.currentAttackTimer = 0
                self.hasAttacked = False
            return
