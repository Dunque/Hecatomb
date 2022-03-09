import pygame as pg
from random import uniform
from src.settings.settings import *
from src.sprites.anim import *
import math
from src.hud.hud import CrosshairGun, CrosshairShotGun
from src.weapons.bullets import GunBullet, ShotgunBullet, Explosion

vec = pg.math.Vector2


class SingletonMeta(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class Weapon(metaclass=SingletonMeta):
	def __init__(self, scene, x, y, image):
		self._layer = WEAPON_LAYER
		# Init sprite and groups
		self.groups = scene.all_sprites
		pg.sprite.Sprite.__init__(self, [])
		# Set scene instance and target_group
		self.scene = scene

		self.orig_image = image
		self.image = image
		self.rect = self.image.get_rect()

		self.active = False

		# Init position and rotation
		self.pos = vec(x, y) * TILESIZE
		self.rot = 0
		self.crosshair = None

		self.damage = 1

	def updatePos(self, x, y, player_rect):
		mouse_x, mouse_y = pg.mouse.get_pos()
		cam_moved = self.scene.camera.get_moved()

		mouse_x = mouse_x - cam_moved[0]
		mouse_y = mouse_y - cam_moved[1]

		x_offset = (player_rect[2] / 2)
		y_offset = (player_rect[3] / 2)

		if mouse_x > x + x_offset:
			middle = False
		elif mouse_x < x - x_offset:
			middle = False
		else:
			middle = True

		if mouse_y > y + y_offset:
			up = False
		elif mouse_y < y - y_offset:
			up = True
		else:
			up = False

		if up and middle:
			self.behind = True
		else:
			self.behind = False

		self.pos = vec(x, y)

		pg.display.update()

		# ROTATION
		rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
		if 90 < self.rot + 180 < 270:
			self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))
			is_flipped = False
		else:
			self.rot = int((180 / math.pi) * math.atan2(rel_y, rel_x))
			is_flipped = True
		self.image = pg.transform.flip(pg.transform.rotate(
			self.orig_image, self.rot), False, is_flipped)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos

	def deactivate(self):
		if self.crosshair:
			self.crosshair.kill()
		self.kill()
		self.active = False

	def activate(self):
		self.updatePos(self.scene.player.pos.x, self.scene.player.pos.y,
					   self.scene.player.image.get_rect())
		self.add(self.scene.all_sprites)
		if self.crosshair:
			self.crosshair.activate()
		self.active = True

	def attack(self):
		pass

	def stop_attack(self):
		pass


class Sword(Weapon, pg.sprite.Sprite):
	def __init__(self, scene, x, y):
		super().__init__(scene, x, y, scene.playerSwordImg)
		# Init image and store it to rotate easilly
		self.image = self.scene.playerSwordImg
		self.rect = self.image.get_rect()

		self.damage = 50

		self.rot_attack = 0
		self.reached = 0
		self.sword_speed = 16
		self.multiply_speed = 2.5
		self.top_limit_swing = 50
		self.down_limit_swing = 100
		self.attacking = False

		self.explosionWalls = Anim(scene.fire_ballExplosionSheet, (46, 46), 10, 0, 7)
		self.scale_explosion = 3

	def attack(self):
		self.attack_movement()
		if self.attacking:

			self.scene.camera.cameraShake(1,3)
			collision = pg.sprite.spritecollide(self, self.scene.mobs_SG, False)
			for enemies in collision:
				Explosion(self.scene, enemies.pos, self.explosionWalls, self.scene.mobs_SG, scale=self.scale_explosion,)
				enemies.takeDamage(self.damage)

	def attack_movement(self):
		if self.reached == 0:
			if self.rot_attack > -self.top_limit_swing:
				self.rot_attack -= self.sword_speed
			else:
				self.reached = 1
		elif self.reached == 1:
			self.attacking = True
			if self.rot_attack < self.down_limit_swing:
				self.rot_attack += self.sword_speed * self.multiply_speed
			else:
				self.reached = 2
				self.attacking = False
				SWORD_SOUND.play()
		elif self.reached == 2 and self.rot_attack > 0:
			self.rot_attack -= self.sword_speed

	def stop_attack(self):
		self.rot_attack = 0
		self.reached = 0
		self.attacking = False

	def updatePos(self, x, y, player_rect):
		mouse_x, mouse_y = pg.mouse.get_pos()
		cam_moved = self.scene.camera.get_moved()

		mouse_x = mouse_x - cam_moved[0]
		mouse_y = mouse_y - cam_moved[1]

		x_offset = (player_rect[2] / 2)
		y_offset = (player_rect[3] / 2)

		if mouse_x > x + x_offset:
			middle = False
		elif mouse_x < x - x_offset:
			middle = False
		else:
			middle = True

		if mouse_y > y + y_offset:
			up = False
		elif mouse_y < y - y_offset:
			up = True
		else:
			up = False

		if up and middle:
			self.behind = True
		else:
			self.behind = False

		self.pos = vec(x, y)

		pg.draw.circle(self.scene.screen, BLUE, (x - cam_moved[0], y - cam_moved[1]), 5)
		pg.display.update()

		# ROTATION
		rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
		if 90 < self.rot + 180 < 270:
			self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))
			is_flipped = False
		else:
			self.rot = int((180 / math.pi) * math.atan2(rel_y, rel_x))
			is_flipped = True
		self.image = pg.transform.flip(pg.transform.rotate(self.orig_image, self.rot - self.rot_attack), False,
									   is_flipped)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos


class FireWeapon(Weapon):
	def __init__(self, scene, x, y, image):
		super().__init__(scene, x, y, image)

		# Init shoot direction vector and shoot offset
		# The shoot vector indicates the bullet direction and
		# the offset indicates the spawn point
		self.shoot_vector = vec(0, 1)
		self.shoot_offset = vec(16, 16)
		self.behind = False

		# Init gun stats (Cooldown and damage)
		# This stats will vary depending on the gun type
		# Cooldown -> wait time between shoots
		# Damage   -> damage dealt by bullet
		self.current_cd = 0
		self.can_shoot = True
		self.last_shot = 0

	def update(self):
		self.current_cd += 1


class Gun(FireWeapon, pg.sprite.Sprite):
	def __init__(self, scene, x, y):
		self.scene = scene
		self.image = self.scene.playerGunImg
		self.rect = self.image.get_rect()
		super().__init__(self.scene, x, y, self.image)

		self.barrel_offset = vec(55, -10)
		self.bullet_rate = 300
		self.damage = 12
		self.kickback = 200
		self.spread = 5
		self.crosshair = CrosshairGun(self.scene)

	def get_damage(self):
		return self.damage

	def deactivate(self):
		self.kill()
		self.crosshair.kill()
		self.active = False

	def attack(self):
		if self.active:
			self.scene.camera.cameraShake(1,3)
			now = pg.time.get_ticks()
			if now - self.last_shot > self.bullet_rate or self.last_shot == 0:
				self.last_shot = now
				dir = vec(1, 0).rotate(-self.rot)
				pos = self.pos + self.barrel_offset.rotate(-self.rot)
				if self.rot <= -90 or self.rot >= 90:
					dir = vec(dir.x * 1, dir.y * -1)
					pos = self.pos + vec(self.barrel_offset.x, self.barrel_offset.y * -1).rotate(self.rot)
				FIRE_BULLET_SOUND.play()
				GunBullet(self.scene, self, pos, dir, self.scene.mobs_SG)
				push = int((180 / math.pi) * -math.atan2(dir[1], dir[0]))
				self.scene.player.vel = vec(-self.kickback, 0).rotate(-push)


class Shotgun(FireWeapon, pg.sprite.Sprite):
	def __init__(self, scene, x, y):
		self.scene = scene
		self.image = self.scene.playerShotgunImg
		self.rect = self.image.get_rect()
		super().__init__(self.scene, x, y, self.image)

		self.barrel_offset = vec(55, -10)
		self.bullet_rate = 1000
		self.damage = 20
		self.kickback = 1000
		self.spread = 5
		self.crosshair = CrosshairShotGun(self.scene)

	def get_damage(self):
		return self.damage

	def deactivate(self):
		self.kill()
		self.crosshair.kill()
		self.active = False

	def attack(self):
		if self.active:
			self.scene.camera.cameraShake(2,4)
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
				FIRE_BULLET_SOUND.play()
				ShotgunBullet(self.scene, self, pos, dir, self.scene.mobs_SG)
				ShotgunBullet(self.scene, self, (pos.x + dir.y * 10, pos.y + dir.x * 10), vec(dir.x+direction_disperse,dir.y+direction_disperse),self.scene.mobs_SG)
				ShotgunBullet(self.scene, self, (pos.x - dir.y * 10, pos.y - dir.x * 10), vec(dir.x-direction_disperse,dir.y-direction_disperse),self.scene.mobs_SG)
				push = int((180 / math.pi) * -math.atan2(dir[1], dir[0]))
				self.scene.player.vel = vec(-self.kickback, 0).rotate(-push)
