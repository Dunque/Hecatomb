import pygame as pg
from src.settings.settings import *
from src.sprites.anim import *
from src.settings.entitydata import *
from src.weapons.enemyweapons import *
from src.weapons.bullets import *
from src.entities.states.enemystates import *
from src.entities.character import *

vec = pg.math.Vector2


class HeraldGun(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        walkAnim = Anim(scene.heraldWalkSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(scene.heraldDeathSheet,
                         (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 5)
        animList = [walkAnim, walkAnim, deathAnim, walkAnim, walkAnim]

        super(HeraldGun, self).__init__(scene, x, y,
                                     animList, (scene.mobs_SG), HeraldStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.weaponOffsetX = -20
        self.weaponOffsetY = -10

        self.weapon = EnemyGun(self.scene, 15, 1800, self, self.rect.centerx -
                               self.weaponOffsetX, self.rect.centery - self.weaponOffsetY)
        self.state = EnemyGroundedState(self, "GROUNDED")


class HeraldShotgun(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        walkAnim = Anim(scene.herald2WalkSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(scene.herald2DeathSheet,
                         (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 5)
        animList = [walkAnim, walkAnim, deathAnim, walkAnim, walkAnim]

        super(HeraldShotgun, self).__init__(scene, x, y,
                                        animList, (scene.mobs_SG), HeraldStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.weaponOffsetX = -20
        self.weaponOffsetY = -10

        self.weapon = EnemyShotgun(self.scene, 20, 2500, self, self.rect.centerx -
                               self.weaponOffsetX, self.rect.centery - self.weaponOffsetY)
        self.state = EnemyGroundedState(self, "GROUNDED")

class KhanGun(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        walkAnim = Anim(scene.khanWalkSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(
            scene.khanDeathSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 6)
        animList = [walkAnim, walkAnim, deathAnim, walkAnim, walkAnim]

        super(KhanGun, self).__init__(scene, x, y,
                                          animList, (scene.mobs_SG), KhanStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.weaponOffsetX = -20
        self.weaponOffsetY = -10

        self.weapon = EnemyGun(self.scene, 10, 2000, self, self.rect.centerx -
                                   self.weaponOffsetX, self.rect.centery - self.weaponOffsetY)
        self.state = EnemyGroundedState(self, "GROUNDED")

class KhanShotgun(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        walkAnim = Anim(scene.khanWalkSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(
            scene.khanDeathSheet, (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 6)
        animList = [walkAnim, walkAnim, deathAnim, walkAnim, walkAnim]

        super(KhanShotgun, self).__init__(scene, x, y,
                                   animList, (scene.mobs_SG), KhanStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.weaponOffsetX = -20
        self.weaponOffsetY = -10

        self.weapon = EnemyShotgun(self.scene, 15, 3000, self, self.rect.centerx -
                                   self.weaponOffsetX, self.rect.centery - self.weaponOffsetY)
        self.state = EnemyGroundedState(self, "GROUNDED")


class Worm(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        idleAnim = Anim(scene.wormIdleSheet, (90, 90), 10, 0, 9)
        walkAnim = Anim(scene.wormWalkSheet, (90,90 ), 7, 0, 9)
        deathAnim = Anim(scene.wormDeathSheet, (90, 90), 4, 0, 8)
        attackAnim = Anim(scene.wormAttackSheet, (90, 90), 2, 0, 16)
        animList = [idleAnim, walkAnim, deathAnim, attackAnim, attackAnim]

        super(Worm, self).__init__(scene, x, y,
                                   animList, (scene.mobs_SG), WormStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.hasAttacked = False
        self.attackOffset = vec(30, 30)
        self.explosionWalls = Anim(
            scene.fire_ballExplosion2Sheet, (48, 48), 5, 0, 8)

        self.state = EnemyGroundedState(self, "GROUNDED")

class Eye(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff

        walkAnim = Anim(scene.eyeWalkSheet, (48,92), 7, 0, 7)
        deathAnim = Anim(scene.eyeDeathSheet, (148, 92), 4, 0, 4)

        animList = [walkAnim, walkAnim, deathAnim, walkAnim, walkAnim]

        super(Eye, self).__init__(scene, x, y,
                                   animList, (scene.mobs_SG), EyeStats())

        self.acc = vec(0, 0)
        self.rect.center = self.pos

        self.hasAttacked = False
        self.attackOffset = vec(30, 30)
        self.explosionWalls = Anim(
            scene.fire_ballExplosion2Sheet, (48, 48), 5, 0, 8)


        self.state = KamikazeGroundedState(self, "GROUNDED")

