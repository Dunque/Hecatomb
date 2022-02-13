import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from anim import *
import math
vec = pg.math.Vector2

#Abstract class that can represent all humanoid entities (player, enemies)
class Character(pg.sprite.Sprite):
    #TODO 
    #Hay que añadir aqui al consturecotr de chjaracter el grupo de sprites
    #Hay que crear grupo jugador, grupo enemigos, gerupo objetos etc
    def __init__(self, game, x, y, animList, spriteGroup):
        pg.sprite.Sprite.__init__(self, spriteGroup)
        self.game = game

        #Assign animations
        self.idleAnim = animList[0]
        self.walkAnim = animList[1]
        self.deathAnim = animList[2]
        self.dodgeAnim = animList[3]

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
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rot = 0

        #AIMING
        self.weaponOffsetX = 0
        self.weaponOffsetY = 0
        self.weapon = None

        #STATE MACHINE MANAGEMENT
        self.isActive = False

        self.current_dodge_time = 0
        self.dodge_direction = Vector2(0,0)

        self.stateList = ["IDLE", "WALKING", "DODGING", "DYING"]
        self.currentState = "IDLE"

    #Handles movement logic
    def move(self):
        pass
    
    #Handles the rotation of the equipped weapon
    def aim(self):
        pass
    
    #Plays the death animation and destroys the entity
    def die(self):
        pass

    def stateUpdate(self):
        #Not moving, idle state
        if self.vel == vec(0,0):
            self.currentAnim = self.idleAnim
            self.currentState = "IDLE"
        else:
            self.currentAnim = self.walkAnim
            self.currentState = "WALKING"

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


    def update(self):

        #Movement and aiming
        self.move()
        self.aim()

        if 90 < self.rot + 180 < 270:
            self.isFlipped = False
        else:
            self.isFlipped = True

        #ANIMATION
        self.image = self.currentAnim.get_frame()
        self.image = pg.transform.flip(self.image, self.isFlipped, False)

        #Update current state
        self.stateUpdate()

        #MOVEMENT
        self.pos += self.vel * self.game.dt

        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')

        self.rect.center = self.hit_rect.center

        #WEAPON
        self.weapon.updatePos(self.pos.x - self.weaponOffsetX, self.pos.y - self.weaponOffsetY, self.isFlipped)


class Player(Character):
    def __init__(self, game, x, y):

        #Aniamtion stuff
        self.idleAnim = Anim(game.playerIdleSheet,(SPRITESIZE,SPRITESIZE),10,0,4)
        self.walkAnim = Anim(game.playerWalkSheet,(SPRITESIZE,SPRITESIZE),7,0,6)
        self.deathAnim = Anim(game.playerDeathSheet,(SPRITESIZE,SPRITESIZE),10,0,7)
        self.dodgeAnim = Anim(game.playerDodgeSheet,(SPRITESIZE,SPRITESIZE),5,0,5)

        self.animList = [self.idleAnim, self.walkAnim, self.deathAnim, self.dodgeAnim]
        
        #TODO 
        #Hay que añadir aqui al consturecotr de chjaracter el grupo de sprites
        #Hay que crear grupo jugador, grupo enemigos, gerupo objetos etc
        super(Player, self).__init__(game, x, y, self.animList, game.all_sprites)

        #AIMING
        self.weaponOffsetX = -20
        self.weaponOffsetY = -10
        self.weapon = Gun(self.game, self.pos.x - self.weaponOffsetX, self.pos.y - self.weaponOffsetY, self)

    def move(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

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


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Gun(pg.sprite.Sprite):
    def __init__(self, game, x, y, character):
        # Init sprite and groups
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        # Init data
        #self.data = gun_data
        self.char = character

        # Set game instance and target_group
        self.game = game
        #self.target_group = target_group
        
        # Init image and store it to rotate easilly
        self.image = self.game.playerGunImg
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

    def updatePos(self, x, y, flipWeapon):
        mouse_x, mouse_y = pg.mouse.get_pos()
        cam_moved = self.game.camera.get_moved()

        mouse_x = mouse_x - cam_moved[0]
        mouse_y = mouse_y - cam_moved[1]

        self.pos = vec(x,y)

        pg.draw.circle(self.game.screen, BLUE, (x-cam_moved[0],y-cam_moved[1]), 5)
        pg.display.update()
        
        #ROTATION
        rel_x, rel_y = mouse_x - self.char.rect.centerx, mouse_y - self.char.rect.centery
        if 90 < self.rot + 180 < 270:
            self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))
            #is_flipped = False
        else:
            self.rot = int((180 / math.pi) * math.atan2(rel_y, rel_x))
            #is_flipped = True
        self.image = pg.transform.flip(pg.transform.rotate(self.game.playerGunImg, self.rot), False, flipWeapon)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    """ def shoot(self):
        if (self.can_shoot):
                self.game.audio_mgr.play_sfx("gun")

                shoot_pos_x = self.pos.x+self.shoot_offset.x 
                shoot_pos_y = self.pos.y+self.shoot_offset.y
                Bullet(shoot_pos_x, shoot_pos_y, self.shoot_vector, self.game, self.target_group, self.data)
                self.current_cd = 0
                self.can_shoot = False """

    def update(self):

        self.current_cd += 1 

        """ if (self.current_cd >= self.data.cooldown):
            self.can_shoot = True """
        
        #self.rect.x = self.pos.x+(self.shoot_offset*0.5).x
        #self.rect.y = self.pos.y+(self.shoot_offset*0.5).y

""" class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, shoot_direction, game, target_group, gun_data):
        self.groups = game.all_sprites
        
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
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
        hits = pg.sprite.spritecollide(self, self.game.walls_gr, False)
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