import pygame as pg
from settings import *
from anim import *
from entitydata import *
import math
from menus import WeaponMenu
import time

vec = pg.math.Vector2


def collide_hit_rect(one, two):
	return one.hit_rect.colliderect(two.rect)


# Abstract class that can represent all humanoid entities (player, enemies)
class Character(pg.sprite.Sprite):
	# TODO
	# Hay que añadir aqui al consturecotr de chjaracter el grupo de sprites
	# Hay que crear grupo jugador, grupo enemigos, gerupo objetos etc
	def __init__(self, game, x, y, animList, spriteGroup, entityData):
		pg.sprite.Sprite.__init__(self, spriteGroup)
		self.game = game
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
		if self.entityData.currentDeathAnimTimer >= self.entityData.deathAnimTimer:
			self.kill()
			if self.weapon is not None:
				self.weapon.kill()

	def collide_with_walls(self, dir):
		if dir == 'x':
			hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
			if hits:
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.0
				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
				self.vel.x = 0
				self.hit_rect.centerx = self.pos.x
		if dir == 'y':
			hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
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
		self.pos += self.vel * self.game.dt

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
	def __init__(self, game, x, y):

		# Aniamtion stuff
		self.idleAnim = Anim(game.playerIdleSheet, (SPRITESIZE, SPRITESIZE), 10, 0, 4)
		self.walkAnim = Anim(game.playerWalkSheet, (SPRITESIZE, SPRITESIZE), 7, 0, 6)
		self.deathAnim = Anim(game.playerDeathSheet, (SPRITESIZE, SPRITESIZE), 10, 0, 7)
		self.dodgeAnim = Anim(game.playerDodgeSheet, (SPRITESIZE, SPRITESIZE), 7, 0, 5)

		self.animList = [self.idleAnim, self.walkAnim, self.deathAnim, self.dodgeAnim,
						 self.dodgeAnim]  # repito esa animacion para hace pruebas de atque con los mobs

		# TODO
		# Hay que añadir aqui al consturecotr de chjaracter el grupo de sprites
		# Hay que crear grupo jugador, grupo enemigos, gerupo objetos etc
		super(Player, self).__init__(game, x, y, self.animList, game.all_sprites, PlayerStats())

		# AIMING
		self.weaponOffsetX = -20
		self.weaponOffsetY = -10
		self.weapon_slot = None
		self.weapon_menu = WeaponMenu(self.game)
		self.game.menus.append(self.weapon_menu)

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
			self.game.camera.cameraShake(2, 6)
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
		cam_moved = self.game.camera.get_moved()

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
			self.weapon.updatePos(self.pos.x - self.weaponOffsetX, self.pos.y - self.weaponOffsetY, self.rect)

	def change_weapon(self, slot):
		if self.weapon_slot != slot and slot == "top":
			if self.weapon is not None:
				self.weapon.deactivate()
			self.weapon = Gun(self.game, self.pos.x - self.weaponOffsetX, self.pos.y - self.weaponOffsetY)
			self.weapon.activate()
			self.weapon_slot = slot
		elif self.weapon_slot != slot and slot == "down":
			if self.weapon is not None:
				self.weapon.deactivate()
				self.weapon_slot = slot
		elif self.weapon_slot != slot and slot == "right":
			if self.weapon is not None:
				self.weapon.deactivate()
			self.weapon = Sword(self.game, self.pos.x - self.weaponOffsetX, self.pos.y - self.weaponOffsetY)
			self.weapon.activate()
			self.weapon_slot = slot
		elif self.weapon_slot != slot and slot == "left":
			if self.weapon is not None:
				self.weapon.deactivate()
			self.weapon = Sword(self.game, self.pos.x - self.weaponOffsetX, self.pos.y - self.weaponOffsetY)
			self.weapon.activate()
			self.weapon_slot = slot


class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(GREEN)
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
	def __init__(self, game, x, y, image):
		# Init sprite and groups
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, [])
		# Set game instance and target_group
		self.game = game

		self.orig_image = image
		self.image = image
		self.rect = self.image.get_rect()

		# Init position and rotation
		self.pos = vec(x, y) * TILESIZE
		self.rot = 0

		self.damage = 1

	def updatePos(self, x, y, player_rect):
		mouse_x, mouse_y = pg.mouse.get_pos()
		cam_moved = self.game.camera.get_moved()

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

		pg.draw.circle(self.game.screen, BLUE, (x - cam_moved[0], y - cam_moved[1]), 5)
		pg.display.update()

		# ROTATION
		rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
		if 90 < self.rot + 180 < 270:
			self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))
			is_flipped = False
		else:
			self.rot = int((180 / math.pi) * math.atan2(rel_y, rel_x))
			is_flipped = True
		self.image = pg.transform.flip(pg.transform.rotate(self.orig_image, self.rot), False, is_flipped)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos

	def deactivate(self):
		self.remove(self.game.all_sprites)

	def activate(self):
		self.updatePos(self.game.player.pos.x, self.game.player.pos.y, self.game.player.image.get_rect())
		self.add(self.game.all_sprites)

	def attack(self):
		pass

	def stop_attack(self):
		pass


class Sword(Weapon, pg.sprite.Sprite):
	def __init__(self, game, x, y):
		super().__init__(game, x, y, game.playerSwordImg)
		# Init image and store it to rotate easilly
		self.image = self.game.playerSwordImg
		self.rect = self.image.get_rect()

		self.damage = 10

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
			collision = pg.sprite.spritecollide(self, self.game.mobs, False)
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
		cam_moved = self.game.camera.get_moved()

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

		pg.draw.circle(self.game.screen, BLUE, (x - cam_moved[0], y - cam_moved[1]), 5)
		pg.display.update()

		# ROTATION
		rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
		if 90 < self.rot + 180 < 270:
			self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))
			is_flipped = False
		else:
			self.rot = int((180 / math.pi) * math.atan2(rel_y, rel_x))
			is_flipped = True
		self.image = pg.transform.flip(pg.transform.rotate(self.orig_image, self.rot - self.rot_attack), False, is_flipped)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos


class FireWeapon(Weapon):
	def __init__(self, game, x, y):
		super().__init__(game, x, y, game.playerGunImg)

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

	def update(self):
		self.current_cd += 1


class Gun(FireWeapon, pg.sprite.Sprite):
	def __init__(self, game, x, y):
		super().__init__(game, x, y)

		# Init image and store it to rotate easilly
		self.image = self.game.playerGunImg
		self.rect = self.image.get_rect()


class Mob(Character):
	def __init__(self, game, x, y):
		# Aniamtion stuff
		self.idleAnim = Anim(game.wormIdleSheet, (90, 90), 10, 0, 9)
		self.walkAnim = Anim(game.wormWalkSheet, (90, 90), 7, 0, 9)
		self.deathAnim = Anim(game.wormDeathSheet, (90, 90), 13, 0, 8)
		self.attackAnim = Anim(game.wormAttackSheet, (90, 90), 3, 0, 16)
		self.animList = [self.idleAnim, self.walkAnim, self.deathAnim, self.attackAnim, self.attackAnim]

		super(Mob, self).__init__(game, x, y, self.animList, game.all_sprites, MobStats())

		self.groups = game.all_sprites, game.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.pos = vec(x, y) * TILESIZE
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.rect.center = self.pos
		self.rot = 0

		self.health = 100

		self.time_hit = None
		self.delta_time_hit = 0.3

	def aim(self):
		self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))

	def move(self):
		self.acc = vec(150).rotate(-self.rot)
		self.vel = self.acc * self.game.dt * 15
		self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

	def update(self):
		self.stateUpdate()
		super(Mob, self).update()

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
