import pygame as pg
from random import uniform
from src.settings.settings import *
from src.sprites.anim import *
import math
from src.weapons.bullets import GunBullet, ShotgunBullet

vec = pg.math.Vector2

class EnemyWeapon():
    def __init__(self, scene, dmg, rate, owner, x, y, image):
        self._layer = WEAPON_LAYER
        # Init sprite and groups
        self.groups = scene.all_sprites
        pg.sprite.Sprite.__init__(self, scene.all_sprites)
        # Set scene instance and target_group
        self.scene = scene

        self.owner = owner

        self.orig_image = image
        self.image = image
        self.rect = self.image.get_rect()

        # Init position and rotation
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

        self.damage = dmg
        self.bullet_rate = rate

    def updatePos(self, x, y):
        self.pos = vec(x, y)

        pg.display.update()

        # ROTATION
        self.rot = (self.scene.player.pos - self.pos).angle_to(vec(1, 0))

        if 90 < self.rot + 180 < 270:

            is_flipped = False
        else:
            self.rot = -self.rot
            is_flipped = True
        self.image = pg.transform.flip(pg.transform.rotate(
            self.orig_image, self.rot), False, is_flipped)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def attack(self):
        pass

    def stop_attack(self):
        pass

class EnemyFireWeapon(EnemyWeapon):
    def __init__(self, scene, dmg, rate, owner, x, y, image):
        super(EnemyFireWeapon, self).__init__(scene, dmg, rate, owner, x, y, image)

        # Init shoot direction vector and shoot offset
        # The shoot vector indicates the bullet direction and
        # the offset indicates the spawn point
        self.shoot_vector = vec(0, 1)
        self.shoot_offset = vec(16, 16)
        self.behind = False

        # Init gun stats (Cooldown and damage)
        # This stats will vary depending on the gun type
        # Cooldown -> wait time between shots
        # Damage   -> damage dealt by each bullet
        self.current_cd = 0
        self.can_shoot = True
        self.last_shot = 0

    def update(self):
        self.current_cd += 1

class EnemyGun(EnemyFireWeapon, pg.sprite.Sprite):
    def __init__(self, scene, dmg, rate, owner, x, y):
        self.scene = scene
        self.image = self.scene.playerGunImg
        self.rect = self.image.get_rect()
        super(EnemyGun, self).__init__(
            self.scene, dmg, rate, owner, x, y, self.image)

        self.barrel_offset = vec(55, -10)
        self.kickback = 200
        self.spread = 10

    def get_damage(self):
        return self.damage

    def attack(self):
        if self.owner.isActive:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.bullet_rate or self.last_shot == 0:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + self.barrel_offset.rotate(-self.rot)
                if self.rot <= -90 or self.rot >= 90:
                    dir = vec(dir.x * 1, dir.y * -1)
                    pos = self.pos + vec(self.barrel_offset.x, self.barrel_offset.y * -1).rotate(self.rot)
                self.scene.camera.cameraShake(1,3)
                FIRE_BULLET_SOUND.play()
                GunBullet(self.scene, self, pos, dir, self.scene.player_SG)
                push = int((180 / math.pi) * -math.atan2(dir[1], dir[0]))
                self.owner.vel = vec(-self.kickback, 0).rotate(-push)

class EnemyShotgun(EnemyFireWeapon, pg.sprite.Sprite):
    def __init__(self, scene, dmg, rate, owner, x, y):
        self.scene = scene
        self.image = self.scene.playerShotgunImg
        self.rect = self.image.get_rect()
        super(EnemyShotgun, self).__init__(
            self.scene, dmg, rate, owner, x, y, self.image)

        self.barrel_offset = vec(55, -10)
        self.kickback = 1000
        self.spread = 10

    def get_damage(self):
        return self.damage

    def attack(self):
        if self.owner.isActive:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.bullet_rate or self.last_shot == 0:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + self.barrel_offset.rotate(-self.rot)
                direction_disperse = 0.2
                if self.rot <= -90 or self.rot >= 90:
                    dir = vec(dir.x * 1, dir.y * -1)
                    pos = self.pos + vec(self.barrel_offset.x, self.barrel_offset.y * -1).rotate(self.rot)
                    direction_disperse = -0.2
                self.scene.camera.cameraShake(2,3)
                FIRE_BULLET_SOUND.play()
                ShotgunBullet(self.scene, self, pos, dir, self.scene.player_SG)
                ShotgunBullet(self.scene, self, (pos.x + dir.y * 10, pos.y + dir.x * 10), vec(dir.x+direction_disperse,dir.y+direction_disperse),self.scene.player_SG)
                ShotgunBullet(self.scene, self, (pos.x - dir.y * 10, pos.y - dir.x * 10), vec(dir.x-direction_disperse,dir.y-direction_disperse),self.scene.player_SG)
                push = int((180 / math.pi) * -math.atan2(dir[1], dir[0]))
                self.owner.vel = vec(-self.kickback, 0).rotate(-push)
