import pygame as pg
from settings import *
from anim import *
from entitydata import *
from menus import WeaponMenu
import time
from random import uniform

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
		pg.sprite.Sprite.__init__(self, spriteGroup)
		self.scene = scene
		self.entityData = entityData

		# Assign animations
		self.idleAnim = animList[0]
		self.walkAnim = animList[1]
		self.deathAnim = animList[2]
		self.dodgeAnim = animList[3]
		self.attackAnim = animList[4]

		# Set the idle animation as the starting one
		self.currentAnim = self.idleAnim

		# Get the first frame of the anim to set up the rect
		self.image = self.deathAnim.get_frame()
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
		# "GROUNDED", "DODGING", "DYING"
		self.currentState = "GROUNDED"


	# Handles movement logic
	def move(self):
		pass

	# Handles the rotation of the equipped weapon
	def aim(self):
		pass

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
		if self.entityData.vulnerable and (self.currentState != "DODGING"):
			self.entityData.takeDamage(dmg)

	def stateUpdate(self):
		if (self.currentState == "GROUNDED"):
			# Not moving -> idle animation
			if self.vel == vec(0, 0):
				self.currentAnim = self.idleAnim
			else:
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

		if (self.currentState == "ATTACK"):
			self.currentAnim = self.attackAnim
			self.aim()
			if (self.entityData.currentAttackTimer <= self.entityData.AttackTimer):
				self.entityData.currentAttackTimer += 1
				self.vel = self.AttackDir
			else:
				self.currentState = "GROUNDED"
				self.entityData.currentAttackTimer = 0
			return

		if (self.currentState == "DODGING"):
			self.currentAnim = self.dodgeAnim
			if (self.entityData.currentDodgeTimer <= self.entityData.dodgeTimer):
				self.entityData.currentDodgeTimer += 1
				self.vel = self.dodgeDir

			else:
				self.currentState = "GROUNDED"
				self.entityData.currentDodgeTimer = 0
			return

	def update(self):
		# Check if the character should die
		if (self.entityData.isAlive == False):
			self.currentState = "DYING"

		# Update current state
		self.stateUpdate()

		if 90 < self.rot + 180 < 270:
			self.isFlipped = False
		else:
			self.isFlipped = True

		# MOVEMENT
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
		if self.entityData.actualHP <= 0:
			self.entityData.isAlive = False

class Player(Character):
	def __init__(self, scene, x, y):

		# Aniamtion stuff
		self.idleAnim = Anim(scene.playerIdleSheet,
							 (SPRITESIZE, SPRITESIZE), 10, 0, 4)
		self.walkAnim = Anim(scene.playerWalkSheet, (SPRITESIZE, SPRITESIZE), 7, 0, 6)
		self.deathAnim = Anim(scene.playerDeathSheet,
							  (SPRITESIZE, SPRITESIZE), 10, 0, 7)
		self.dodgeAnim = Anim(scene.playerDodgeSheet,
							  (SPRITESIZE, SPRITESIZE), 7, 0, 5)

		self.animList = [self.idleAnim, self.walkAnim, self.deathAnim, self.dodgeAnim,
						 self.dodgeAnim]  # repito esa animacion para hace pruebas de atque con los mobs

		# TODO
		# Hay que añadir aqui al consturecotr de chjaracter el grupo de sprites
		# Hay que crear grupo jugador, grupo enemigos, gerupo objetos etc
		super(Player, self).__init__(scene, x, y,
									 self.animList, scene.all_sprites, PlayerStats())

		# AIMING
		self.weaponOffsetX = -20
		self.weaponOffsetY = -10
		self.weapon_slot = None
		self.weapon_menu = WeaponMenu(self.scene)
		self.scene.menus.append(self.weapon_menu)

	def move(self):
		# We are able to move freely
		self.vel = vec(0, 0)
		keys = pg.key.get_pressed()
		if keys[pg.K_a]:
			self.vel.x = -self.entityData.speed
		if keys[pg.K_d]:
			self.vel.x = self.entityData.speed
		if keys[pg.K_w]:
			self.vel.y = -self.entityData.speed
		if keys[pg.K_s]:
			self.vel.y = self.entityData.speed
		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071

		mouse = pg.mouse.get_pressed()
		# Left click
		if mouse[0]:
			self.scene.camera.cameraShake(2, 6)
			if self.weapon:
				self.weapon.attack()
		elif not mouse[0]:
			if self.weapon:
				self.weapon.stop_attack()

		if keys[pg.K_SPACE]:
			self.currentState = "DODGING"
			self.dodgeDir = self.vel * self.entityData.dodgeSpeed

		##DEBUG KEY TO KILL YOURSELF
		if keys[pg.K_0]:
			self.takeDamage(100)

		if keys[pg.K_TAB]:
			self.show_menu = True
		else:
			self.show_menu = False

	def aim(self):
		cam_moved = self.scene.camera.get_moved()

		mouse_x, mouse_y = pg.mouse.get_pos()

		mouse_x = mouse_x - cam_moved[0]
		mouse_y = mouse_y - cam_moved[1]

		rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
		self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))

		if 90 < self.rot + 180 < 270:
			self.isFlipped = False
			self.weaponOffsetX = -20
		else:
			self.isFlipped = True
			self.weaponOffsetX = 20

	def update(self):
		super(Player, self).update()

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
			pg.mouse.set_visible(True)
			self.weapon.activate()
			self.weapon_slot = slot


class Wall(pg.sprite.Sprite):
	def __init__(self, scene, x, y, tileset):
		self.groups = scene.all_sprites, scene.walls_SG
		pg.sprite.Sprite.__init__(self, self.groups)
		self.scene = scene
		self.image = tileset  # pg.Surface((TILESIZE, TILESIZE))
		# self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.pos = vec(x, y)
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

class SingletonMeta(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__call__(*args, **kwargs)
			cls._instances[cls] = instance
		return cls._instances[cls]


class Weapon(metaclass=SingletonMeta):
	def __init__(self, scene, x, y, image):
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

		pg.draw.circle(self.scene.screen, BLUE,
					   (x - cam_moved[0], y - cam_moved[1]), 5)
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
		self.sword_speed = 8
		self.multiply_speed = 2.5
		self.top_limit_swing = 50
		self.down_limit_swing = 100
		self.attacking = False

	def attack(self):
		self.attack_movement()
		if self.attacking:
			collision = pg.sprite.spritecollide(self, self.scene.mobs_SG, False)
			for enemies in collision:
				enemies.take_hit(self.damage)

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
		self.damage = 100
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
			now = pg.time.get_ticks()
			if now - self.last_shot > self.bullet_rate or self.last_shot == 0:
				self.last_shot = now
				dir = vec(1, 0).rotate(-self.rot)
				pos = self.pos + self.barrel_offset.rotate(-self.rot)
				if self.rot <= -90 or self.rot >= 90:
					dir = vec(dir.x * 1, dir.y * -1)
					pos = self.pos + vec(self.barrel_offset.x, self.barrel_offset.y * -1).rotate(self.rot)
				Bullet(self.scene, pos, dir)
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
		self.damage = 800
		self.kickback = 1000
		self.spread = 10
		self.crosshair = CrosshairGun(self.scene)

	def get_damage(self):
		return self.damage

	def deactivate(self):
		self.kill()
		self.crosshair.kill()
		self.active = False

	def attack(self):
		if self.active:
			now = pg.time.get_ticks()
			if now - self.last_shot > self.bullet_rate or self.last_shot == 0:
				self.last_shot = now
				dir = vec(1, 0).rotate(-self.rot)
				pos = self.pos + self.barrel_offset.rotate(-self.rot)
				if self.rot <= -90 or self.rot >= 90:
					dir = vec(dir.x * 1, dir.y * -1)
					pos = self.pos + vec(self.barrel_offset.x, self.barrel_offset.y * -1).rotate(self.rot)
				ShotgunBullet(self.scene, pos, dir)
				push = int((180 / math.pi) * -math.atan2(dir[1], dir[0]))
				self.scene.player.vel = vec(-self.kickback, 0).rotate(-push)


class CrosshairGun(pg.sprite.Sprite):
	def __init__(self, scene):
		self.scene = scene
		self.groups = scene.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.image = scene.gunCrosshairImg
		self.rect = self.image.get_rect()
		self.rect.center = pg.mouse.get_pos()

	def update(self):
		cam_moved = self.scene.camera.get_moved()

		mouse_x, mouse_y = pg.mouse.get_pos()

		mouse_x = mouse_x - cam_moved[0]
		mouse_y = mouse_y - cam_moved[1]
		self.rect.center = mouse_x, mouse_y

	def activate(self):
		self.add(self.scene.all_sprites)


class Bullet(pg.sprite.Sprite):
	def __init__(self, scene, pos, dir):
		self.groups = scene.all_sprites, scene.bullets_SG
		pg.sprite.Sprite.__init__(self, self.groups)
		self.scene = scene

		self.explosionWalls = Anim(scene.fire_ballExplosionSheet, (46, 46), 5, 0, 7)

		rot = int((180 / math.pi) * -math.atan2(dir[1], dir[0]))
		self.image = pg.transform.rotate(scene.bulletImg, rot)
		self.rect = self.image.get_rect()
		self.pos = pos
		self.rect.center = pos
		spread_val = self.scene.player.weapon.spread
		self.vel = dir.rotate(uniform(-spread_val, spread_val)) * 1000
		self.spawn_time = pg.time.get_ticks()

		self.lifetime = 1000
		self.damage = 5

	def get_damage(self):
		return self.damage * self.scene.player.weapon.get_damage()

	def update(self):
		self.pos += self.vel * self.scene.dt
		self.rect.center = self.pos
		target = pg.sprite.spritecollideany(self, self.scene.mobs_SG)
		if pg.sprite.spritecollideany(self, self.scene.walls_SG):
			self.scene.camera.cameraShake(self.damage, self.damage)
			Explosion(self.scene, self.pos, self.explosionWalls)
			self.kill()
		elif target:
			Explosion(self.scene, self.pos, self.explosionWalls)
			target.take_hit(self.get_damage())
			self.kill()
		if pg.time.get_ticks() - self.spawn_time > self.lifetime:
			self.kill()


class ShotgunBullet(pg.sprite.Sprite):
	def __init__(self, scene, pos, dir):
		self.groups = scene.all_sprites, scene.bullets_SG
		pg.sprite.Sprite.__init__(self, self.groups)
		self.scene = scene

		self.explosionWalls = Anim(scene.fire_ballExplosionSheet, (46, 46), 10, 0, 7)

		rot = int((180 / math.pi) * -math.atan2(dir[1], dir[0]))
		self.image = pg.transform.rotate(scene.bulletImg, rot)
		self.rect = self.image.get_rect()
		self.pos = pos
		self.rect.center = pos
		spread_val = self.scene.player.weapon.spread
		self.vel = dir.rotate(uniform(-spread_val, spread_val)) * 1000
		self.spawn_time = pg.time.get_ticks()

		self.lifetime = 1000
		self.damage = 15

	def get_damage(self):
		return self.damage * self.scene.player.weapon.get_damage()

	def update(self):
		self.pos += self.vel * self.scene.dt
		self.rect.center = self.pos
		target = pg.sprite.spritecollideany(self, self.scene.mobs_SG)
		if pg.sprite.spritecollideany(self, self.scene.walls_SG):
			self.scene.camera.cameraShake(self.damage, self.damage)
			Explosion(self.scene, self.pos, self.explosionWalls, scale=5, destroy=True)
			self.kill()
		elif target:
			Explosion(self.scene, self.pos, self.explosionWalls, scale=5)
			target.take_hit(self.get_damage())
			self.kill()
		if pg.time.get_ticks() - self.spawn_time > self.lifetime:
			self.kill()


class Explosion(pg.sprite.Sprite):
	def __init__(self, scene, pos, anim, scale = 1, destroy = False):
		self.groups = scene.all_sprites, scene.bullets_SG
		pg.sprite.Sprite.__init__(self, self.groups)
		self.scene = scene

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
			aa = pg.sprite.spritecollide(self, self.scene.walls_SG, True)


class Mob(Character):
	def __init__(self, scene, x, y):
		# Aniamtion stuff
		self.idleAnim = Anim(scene.wormIdleSheet, (90, 90), 10, 0, 9)
		self.walkAnim = Anim(scene.wormWalkSheet, (90, 90), 7, 0, 9)
		self.deathAnim = Anim(scene.wormDeathSheet, (90, 90), 5, 0, 8)
		self.attackAnim = Anim(scene.wormAttackSheet, (90, 90), 7, 0, 16)
		self.animList = [self.idleAnim, self.walkAnim, self.deathAnim, self.attackAnim, self.attackAnim]

		super(Mob, self).__init__(scene, x, y, self.animList, scene.all_sprites, MobStats())

		self.groups = scene.all_sprites, scene.mobs_SG
		pg.sprite.Sprite.__init__(self, self.groups)

		self.scene = scene
		self.pos = vec(x, y) * TILESIZE
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.rect.center = self.pos
		self.rot = 0

		self.health = 100

		self.time_hit = None
		self.delta_time_hit = 0.3

	def update(self):
		self.stateUpdate()
		super(Mob, self).update()

		if self.health <= 0:
			self.die()

	def aim(self):
		self.rot = (self.scene.player.pos - self.pos).angle_to(vec(1, 0))


	def move(self):
		self.acc = vec(150).rotate(-self.rot)
		self.vel = self.acc * self.scene.dt * 15
		self.pos += self.vel * self.scene.dt + 0.5 * self.acc * self.scene.dt ** 2

	def take_hit(self, weapon_damage):
		time_now = time.time()
		if not self.time_hit:
			self.time_hit = time_now
		delta = time_now - self.time_hit
		if delta == 0 or delta > self.delta_time_hit:
			self.health -= weapon_damage
			self.time_hit = time_now


	def die(self):
		self.kill()

class Bully(Character):
	def __init__(self, scene, x, y):
		# Aniamtion stuff
		self.idleAnim = Anim(scene.BullyIdleSheet, (52, 47), 7, 0, 3)
		self.walkAnim = Anim(scene.BullyWalkSheet, (60, 47), 15, 0, 9)
		self.deathAnim = Anim(scene.BullyDeathSheet, (40, 47), 13, 0, 5)
		self.attackAnim = Anim(scene.BullyAttackSheet, (59, 47), 7, 0, 6)
		self.animList = [self.idleAnim, self.walkAnim, self.deathAnim, self.attackAnim, self.attackAnim]

		super(Bully, self).__init__(scene, x, y, self.animList, scene.all_sprites, BullyStats())

		self.groups = scene.all_sprites, scene.bully_SG
		pg.sprite.Sprite.__init__(self, self.groups)

		self.scene = scene
		self.pos = vec(x, y) * TILESIZE
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.rect.center = self.pos
		self.rot = 0

		self.health = 100

		self.time_hit = None
		self.delta_time_hit = 0.3

	def aim(self):
		self.rot = (self.scene.player.pos - self.pos).angle_to(vec(1, 0))


	def move(self):
		self.acc = vec(150).rotate(-self.rot)
		self.vel = self.acc * self.scene.dt * 15
		self.pos += self.vel * self.scene.dt + 0.5 * self.acc * self.scene.dt ** 2


	def update(self):
		self.stateUpdate()
		super(Bully, self).update()

		if self.health <= 0:
			self.die()

	def take_hit(self, weapon_damage):
		time_now = time.time()
		if not self.time_hit:
			self.time_hit = time_now
		delta = time_now - self.time_hit
		if delta == 0 or delta > self.delta_time_hit:
			self.health -= weapon_damage
			self.time_hit = time_now


	def die(self):
		self.kill()


class Fireball(pg.sprite.Sprite):
	def __init__(self, scene, x, y):
		self.groups = scene.all_sprites, scene.fireBalls_SG
		pg.sprite.Sprite.__init__(self, self.groups)
		self.scene = scene
		self.image = scene.fire_ballMoveSheet
		self.rect = self.image.get_rect()
		pg.sprite.Sprite.__init__(self, self.groups)
		self.pos = vec(x, y) * TILESIZE
		self.rect.center = self.pos
		spread = uniform(-FIRE_BALL_SPREAD, FIRE_BALL_SPREAD)
		self.vel = FIRE_BALL_SPEED
		self.spawn_time = pg.time.get_ticks()
		self.rot = 0

	def update(self):
		self.acc = vec(150).rotate(-self.rot)
		self.vel = self.acc * self.scene.dt * 15
		self.pos += self.vel * self.scene.dt + 0.5 * self.acc * self.scene.dt ** 2
		self.rect.center = self.pos
		if pg.sprite.spritecollideany(self, self.scene.walls_SG):
			self.kill()
		if pg.time.get_ticks() - self.spawn_time > FIRE_BALL_LIFETIME:
			self.kill()


class Door(pg.sprite.Sprite):
	def __init__(self, scene, x, y, isExit):
		# Assing the groups and init sprite
		self.groups = scene.all_sprites, scene.walls_gr
		pg.sprite.Sprite.__init__(self, self.groups)

		# Assign scene manager reference
		self.scene = scene

		# Init sprite and rect
		sprite_sheet = "./sprites/door_sprite.png"
		self.original_image = pg.image.load(sprite_sheet).convert_alpha()
		self.original_image = pg.transform.scale(
			self.original_image, (TILESIZE, TILESIZE))

		self.image = self.original_image

		self.rect = pg.Rect((0, 0), (TILESIZE, TILESIZE))

		# Set position in tilemap
		self.x = x
		self.y = y

		# Set position in world
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

	def open_door(self):
		# In order to open the door we remove the image and
		# remove it from "walls" group
		self.scene.walls_gr.remove(self)
		self.scene.all_sprites.remove(self)

	def close_door(self):
		# In order to close the door we add the image and
		# add it to the "walls" group
		self.scene.walls_gr.add(self)
		self.scene.all_sprites.add(self)

		self.groups = self.scene.all_sprites, self.scene.walls_gr

		self.image = self.original_image
