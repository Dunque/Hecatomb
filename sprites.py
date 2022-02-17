import pygame as pg
from settings import *
from anim import *
from entitydata import *
import math
vec = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

#Abstract class that can represent all humanoid entities (player, enemies)
class Character(pg.sprite.Sprite):
    #TODO 
    #Hay que añadir aqui al consturecotr de chjaracter el grupo de sprites
    #Hay que crear grupo jugador, grupo enemigos, gerupo objetos etc
    def __init__(self, scene, x, y, animList, spriteGroup, entityData):
        pg.sprite.Sprite.__init__(self, spriteGroup)
        self.scene = scene
        self.entityData = entityData

        #Assign animations
        self.idleAnim = animList[0]
        self.walkAnim = animList[1]
        self.deathAnim = animList[2]
        self.dodgeAnim = animList[3]
        self.attackAnim = animList[4]

        #Set the idle animation as the starting one 
        self.currentAnim = self.idleAnim

        #Get the first frame of the anim to set up the rect
        self.image = self.deathAnim.get_frame()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        #Boolean to flip the sprite
        self.isFlipped = False

        #MOVEMENT
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        #Player hitbox is smaller
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rot = 0

        #AIMING
        self.weaponOffsetX = 0
        self.weaponOffsetY = 0
        self.weapon = None

        #DODGING
        self.dodgeDir = vec(0,0)
        # ATTACK
        self.AttackDir = vec(0, 0)
        #STATES
        # "GROUNDED", "DODGING", "DYING"
        self.currentState = "GROUNDED"

    #Handles movement logic
    def move(self):
        pass
    
    #Handles the rotation of the equipped weapon
    def aim(self):
        pass
    
    #Plays the death animation and destroys the entity
    def die(self):
        self.entityData.currentDeathAnimTimer += 1
        if (self.entityData.currentDeathAnimTimer >= self.entityData.deathAnimTimer):
            self.kill()
            self.weapon.kill()

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.scene.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.0
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.scene.walls, False, collide_hit_rect)
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
            #Not moving -> idle animation
            if self.vel == vec(0,0):
                self.currentAnim = self.idleAnim
            else:
                self.currentAnim = self.walkAnim

            #Movement and aiming
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
            if (self.entityData.currentAttackTimer <= self.entityData.AttackTimer ):
                self.entityData.currentAttackTimer += 1
                self.vel = self.AttackDir
            else:
                self.currentState = "GROUNDED"
                self.entityData.currentAttackTimer = 0
            return

        if (self.currentState == "DODGING"):
            self.currentAnim = self.dodgeAnim
            if (self.entityData.currentDodgeTimer <= self.entityData.dodgeTimer ):
                self.entityData.currentDodgeTimer += 1
                self.vel = self.dodgeDir

            else:
                self.currentState = "GROUNDED"
                self.entityData.currentDodgeTimer = 0
            return

    def update(self):
        #Check if the character should die
        if (self.entityData.isAlive == False):
            self.currentState = "DYING"

        #Update current state
        self.stateUpdate()

        if 90 < self.rot + 180 < 270:
            self.isFlipped = False
        else:
            self.isFlipped = True

        #MOVEMENT
        self.pos += self.vel * self.scene.dt

        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')

        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')

        self.rect.center = self.hit_rect.center

        #ANIMATION
        self.image = self.currentAnim.get_frame()
        self.image = pg.transform.flip(self.image, self.isFlipped, False)

        # Update entity's data
        self.entityData.update()

class Player(Character):
    def __init__(self, scene, x, y):

        #Aniamtion stuff
        self.idleAnim = Anim(scene.playerIdleSheet,(SPRITESIZE,SPRITESIZE),10,0,4)
        self.walkAnim = Anim(scene.playerWalkSheet,(SPRITESIZE,SPRITESIZE),7,0,6)
        self.deathAnim = Anim(scene.playerDeathSheet,(SPRITESIZE,SPRITESIZE),10,0,7)
        self.dodgeAnim = Anim(scene.playerDodgeSheet,(SPRITESIZE,SPRITESIZE),7,0,5)

        self.animList = [self.idleAnim, self.walkAnim, self.deathAnim, self.dodgeAnim,self.dodgeAnim] #repito esa animacion para hace pruebas de atque con los mobs
        
        #TODO 
        #Hay que añadir aqui al consturecotr de chjaracter el grupo de sprites
        #Hay que crear grupo jugador, grupo enemigos, gerupo objetos etc
        super(Player, self).__init__(scene, x, y, self.animList, scene.all_sprites, PlayerStats())

        #AIMING
        self.weaponOffsetX = -20
        self.weaponOffsetY = -10
        self.weapon = Gun(self.scene, self.pos.x - self.weaponOffsetX, self.pos.y - self.weaponOffsetY, self)

    def move(self):
        #We are able to move freely
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
        #Left click
        if mouse[0]:
            self.scene.camera.cameraShake(2,6)

        if keys[pg.K_SPACE]:
            self.currentState = "DODGING"
            self.dodgeDir = self.vel * self.entityData.dodgeSpeed

        ##DEBUG KEY TO KILL YOURSELF
        if keys[pg.K_0]:
            self.takeDamage(100)

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

        #WEAPON
        self.weapon.updatePos(self.pos.x - self.weaponOffsetX, self.pos.y - self.weaponOffsetY)


class Wall(pg.sprite.Sprite):
    def __init__(self, scene, x, y):
        self.groups = scene.all_sprites, scene.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.scene = scene
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Gun(pg.sprite.Sprite):
    def __init__(self, scene, x, y, character):
        # Init sprite and groups
        self.groups = scene.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        # Init data
        #self.data = gun_data
        self.char = character

        # Set scene instance and target_group
        self.scene = scene
        #self.target_group = target_group
        
        # Init image and store it to rotate easilly
        self.image = self.scene.playerGunImg
        self.rect = self.image.get_rect()

        # Init position and rotation
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

        # Init shoot direction vector and shoot offset
        # The shoot vector indicates the bullet direction and
        # the offset indicates the spawn point
        self.shoot_vector = vec(0,1)
        self.shoot_offset = vec(16, 16)
        self.behind = False

        # Init gun stats (Cooldown and damage)
        # This stats will vary depending on the gun type
        # Cooldown -> wait time between shoots
        # Damage   -> damage dealt by bullet
        self.current_cd = 0
        self.can_shoot = True

        self.damage = 1

    def updatePos(self, x, y):
        mouse_x, mouse_y = pg.mouse.get_pos()
        cam_moved = self.scene.camera.get_moved()

        mouse_x = mouse_x - cam_moved[0]
        mouse_y = mouse_y - cam_moved[1]

        self.pos = vec(x,y)
        
        #ROTATION
        rel_x, rel_y = mouse_x - self.char.rect.centerx, mouse_y - self.char.rect.centery

        if 90 < self.rot + 180 < 270:
            self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))
            flipWeapon = False
        else:
            self.rot = int((180 / math.pi) * math.atan2(rel_y, rel_x))
            flipWeapon = True
        self.image = pg.transform.flip(pg.transform.rotate(self.scene.playerGunImg, self.rot), False, flipWeapon)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    """ def shoot(self):
        if (self.can_shoot):
                self.scene.audio_mgr.play_sfx("gun")

                shoot_pos_x = self.pos.x+self.shoot_offset.x 
                shoot_pos_y = self.pos.y+self.shoot_offset.y
                Bullet(shoot_pos_x, shoot_pos_y, self.shoot_vector, self.scene, self.target_group, self.data)
                self.current_cd = 0
                self.can_shoot = False """

    def update(self):

        self.current_cd += 1 

        """ if (self.current_cd >= self.data.cooldown):
            self.can_shoot = True """
        
        #self.rect.x = self.pos.x+(self.shoot_offset*0.5).x
        #self.rect.y = self.pos.y+(self.shoot_offset*0.5).y

""" class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, shoot_direction, scene, target_group, gun_data):
        self.groups = scene.all_sprites
        
        pg.sprite.Sprite.__init__(self, self.groups)
        self.scene = scene
        
        self.image = pg.Surface((TILESIZE/8, TILESIZE/8))
        self.image.fill(gun_data.bullet_color)
        self.rect = self.image.get_rect()

        self.pos = vec(x, y)
        self.direction = shoot_direction
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
        self.speed = gun_data.bullet_speed
        self.target_group = target_group

        self.damage = gun_data.damage

        self.alive_time = 0
        self.max_alive_time = gun_data.reach

    
    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.scene.walls_gr, False)
        if hits: 
            self.kill()
    
    def collide_with_enemy(self):
        hits = pg.sprite.spritecollide(self, self.target_group, False)
        if hits:
            for hit in hits:
                hit.take_damage(self.damage)
                self.kill()
        
    def move(self):
        self.pos.x += self.direction.x * self.speed
        self.pos.y += self.direction.y * self.speed

    def update(self):
        # Check for bullet dissapear
        self.alive_time+=1
        if (self.alive_time > self.max_alive_time):
            self.kill()

        # Check collisions
        self.collide_with_enemy()
        self.collide_with_walls()

        # Compute movement
        self.move()
        
        # Update render position
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y   """

class Mob(Character):
    def __init__(self, scene, x, y):
        # Aniamtion stuff
        self.idleAnim = Anim(scene.wormIdleSheet, (90, 90), 10, 0, 9)
        self.walkAnim = Anim(scene.wormWalkSheet, (90, 90), 7, 0, 9)
        self.deathAnim = Anim(scene.wormDeathSheet, (90, 90), 13, 0, 8)
        self.attackAnim = Anim(scene.wormAttackSheet, (90, 90), 7, 0, 16)
        self.animList = [self.idleAnim, self.walkAnim, self.deathAnim, self.attackAnim ,self.attackAnim]

        super(Mob, self).__init__(scene, x, y, self.animList, scene.all_sprites, MobStats())

        self.groups = scene.all_sprites, scene.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.scene = scene
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0

    def aim(self):
        self.rot = (self.scene.player.pos - self.pos).angle_to(vec(1, 0))

    def move(self):
        self.acc = vec(150).rotate(-self.rot)
        self.vel = self.acc * self.scene.dt * 15
        self.pos += self.vel * self.scene.dt + 0.5 * self.acc * self.scene.dt ** 2



    def update(self):
        self.stateUpdate()
        super(Mob, self).update()


