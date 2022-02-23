import pygame as pg
from anim import *
import math
from random import uniform

from settings import PICKUP_LAYER, WEAPON_LAYER

vec = pg.math.Vector2

#Bullets have a targetGroup that dictates the sprite group that will colide with them
class Bullet:
	def __init__(self, scene, weapon, pos, dir, image, targetGroup):
		self.groups = scene.all_sprites, scene.bullets_SG
		pg.sprite.Sprite.__init__(self, self.groups)
		self.scene = scene
		self.weapon = weapon
		self.targetGroup = targetGroup

		rot = int((180 / math.pi) * -math.atan2(dir[1], dir[0]))
		self.image = pg.transform.rotate(image, rot)
		self.rect = self.image.get_rect()
		self.pos = pos
		self.rect.center = pos

		spread_val = self.weapon.spread
		self.vel = dir.rotate(uniform(-spread_val, spread_val)) * 1000
		self.spawn_time = pg.time.get_ticks()

		self.scale_explosion = 1
		self.destroy_scene = False

	def get_damage(self):
		return self.damage * self.weapon.get_damage()

	def update(self):
		self.pos += self.vel * self.scene.dt
		self.rect.center = self.pos
		self.check_collision()

	def check_collision(self):
		target = pg.sprite.spritecollideany(self, self.targetGroup)
		if pg.sprite.spritecollideany(self, self.scene.walls_SG):
			Explosion(self.scene, self.pos, self.explosionWalls, self.targetGroup, scale=self.scale_explosion, destroy=self.destroy_scene)
			self.kill()
		elif target:
			Explosion(self.scene, self.pos, self.explosionWalls, self.targetGroup, scale=self.scale_explosion,)
			target.takeDamage(self.get_damage())
			self.kill()
		if pg.time.get_ticks() - self.spawn_time > self.lifetime:
			self.kill()


class GunBullet(Bullet,pg.sprite.Sprite):
	def __init__(self, scene, weapon, pos, dir, targetGroup):
		super().__init__(scene, weapon, pos, dir, scene.gunBulletImg, targetGroup)

		self.explosionWalls = Anim(scene.fire_ballExplosionSheet, (46, 46), 5, 0, 7)

		self.lifetime = 1000
		self.damage = 1


class ShotgunBullet(Bullet, pg.sprite.Sprite):
	def __init__(self, scene, weapon, pos, dir, targetGroup):
		super().__init__(scene, weapon, pos, dir, scene.gunBulletImg, targetGroup)

		self.explosionWalls = Anim(scene.fire_ballExplosionSheet, (46, 46), 10, 0, 7)

		self.lifetime = 1000
		self.damage = 1
		self.scale_explosion = 2
		self.destroy_scene = True


class Explosion(pg.sprite.Sprite):
	def __init__(self, scene, pos, anim, targetGroup, scale = 1, destroy = False, dealsDamage = False, damage = 0):
		self._layer = PICKUP_LAYER
		self.groups = scene.all_sprites, scene.bullets_SG
		pg.sprite.Sprite.__init__(self, self.groups)
		self.scene = scene
		self.targetGroup = targetGroup
		self.dealsDamage = dealsDamage
		self.damage = damage
		self.explosionAnim = anim
		orig_size = vec(self.explosionAnim.get_frame().get_rect()[2], self.explosionAnim.get_frame().get_rect()[3])
		self.new_size = orig_size * scale
		self.image = self.explosionAnim.get_frame()
		self.rect = self.image.get_rect()
		self.pos = pos
		if scale > 1:
			self.rect.center = (pos.x-(scale * orig_size.x/2), pos.y-(scale * orig_size.y/2))
			self.rect[2] *= scale
			self.rect[3] *= scale
		else:
			self.rect.center = pos
		self.destroy = destroy

	def update(self):
		self.image = pg.transform.scale(self.explosionAnim.get_frame(), self.new_size)
		if self.explosionAnim.current_frame == self.explosionAnim.max_frame - 1:
			self.kill()
		if self.destroy:
			pg.sprite.spritecollide(self, self.scene.walls_SG, True)
		enemycollision = pg.sprite.spritecollide(self, self.targetGroup, False)
		if self.dealsDamage:
			for enemies in enemycollision:
				enemies.entityData.takeDamage(self.damage)