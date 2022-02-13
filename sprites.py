import pygame as pg
from settings import *
from tilemap import collide_hit_rect
from anim import *
import math
vec = pg.math.Vector2

#Abstract class that can represent all humanoid entities (player, enemies)
class Character(pg.sprite.Sprite):

    def __init__(self, game, x, y, animation, groups):

        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        #Aniamtion stuff

        self.walkAnim = Anim(self.game.playerWalkSheet,(SPRITESIZE,SPRITESIZE),5,0,6)
        self.idleAnim = Anim(self.game.playerIdleSheet,(SPRITESIZE,SPRITESIZE),5,0,4)
        self.dodgeAnim = Anim(self.game.playerDodgeSheet,(SPRITESIZE,SPRITESIZE),5,0,5)

        self.image = self.walkAnim.get_frame()
        self.original_image = self.image
        self.rect = self.image.get_rect()

        self.isFlipped = False

        #MOVEMENT
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rot = 0

        #GUN
        self.gun_offset_X = -20
        self.gun_offset_Y = -10
        self.gun = Gun(self.game, self.pos.x - self.gun_offset_X, self.pos.y - self.gun_offset_Y)

    def get_keys(self):
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
        self.get_keys()

        cam_moved = self.game.camera.get_moved()

        mouse_x, mouse_y = pg.mouse.get_pos()

        mouse_x = mouse_x - cam_moved[0]
        mouse_y = mouse_y - cam_moved[1]

        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))

        if 90 < self.rot + 180 < 270:
            self.isFlipped = False
        else:
            self.isFlipped = True

        #ANIMATION
        self.image = self.walkAnim.get_frame()

        #MOVEMENT
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')

        self.rect.center = self.hit_rect.center

        #GUN
        self.gun.update_position(self.pos.x - self.gun_offset_X, self.pos.y - self.gun_offset_Y, self.rect)

        #FLIP SPRITE
        self.image = pg.transform.flip(self.image, self.isFlipped, False)

        #Debug points
        pg.draw.circle(self.game.screen, RED, (self.hit_rect.centerx,self.hit_rect.centery), 50)
        pg.display.update()



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        #Aniamtion stuff

        self.walkAnim = Anim(self.game.playerWalkSheet,(SPRITESIZE,SPRITESIZE),5,0,6)
        self.idleAnim = Anim(self.game.playerIdleSheet,(SPRITESIZE,SPRITESIZE),5,0,4)
        self.dodgeAnim = Anim(self.game.playerDodgeSheet,(SPRITESIZE,SPRITESIZE),5,0,5)
        self.deathAnim = Anim(self.game.playerDeathSheet,(SPRITESIZE,SPRITESIZE),15,0,7)

        self.image = self.deathAnim.get_frame()
        self.original_image = self.image
        self.rect = self.image.get_rect()

        self.isFlipped = False

        #MOVEMENT
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.rot = 0

        #GUN
        self.gun_offset_X = -20
        self.gun_offset_Y = -10
        self.gun = Gun(self.game, self.pos.x - self.gun_offset_X, self.pos.y - self.gun_offset_Y)

    def get_keys(self):
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
        self.get_keys()

        cam_moved = self.game.camera.get_moved()

        mouse_x, mouse_y = pg.mouse.get_pos()

        mouse_x = mouse_x - cam_moved[0]
        mouse_y = mouse_y - cam_moved[1]

        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))

        if 90 < self.rot + 180 < 270:
            self.isFlipped = False
        else:
            self.isFlipped = True

        #ANIMATION
        self.image = self.deathAnim.get_frame()

        #MOVEMENT
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')

        self.rect.center = self.hit_rect.center

        #GUN
        self.gun.update_position(self.pos.x - self.gun_offset_X, self.pos.y - self.gun_offset_Y, self.rect)

        #FLIP SPRITE
        self.image = pg.transform.flip(self.image, self.isFlipped, False)

        #Debug points
        pg.draw.circle(self.game.screen, RED, (self.hit_rect.centerx,self.hit_rect.centery), 50)
        pg.display.update()


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
    def __init__(self, game, x, y):
        # Init sprite and groups
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        # Init data
        #self.data = gun_data

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

    def update_position(self, x, y, player_rect):
        mouse_x, mouse_y = pg.mouse.get_pos()
        cam_moved = self.game.camera.get_moved()

        mouse_x = mouse_x - cam_moved[0]
        mouse_y = mouse_y - cam_moved[1]

        x_offset = (player_rect[2] / 2)
        y_offset = (player_rect[3] / 2)

        if mouse_x > x + x_offset:
            x_offset_side = 50
            middle = False
        elif mouse_x < x - x_offset:
            x_offset_side = 0
            middle = False
        else:
            x_offset_side = mouse_x - x
            middle = True

        if mouse_y > y + y_offset:
            y_offset_side = 50
            up = False
        elif mouse_y < y - y_offset:
            y_offset_side = 0
            up = True
        else:
            y_offset_side = mouse_y - y
            up = False

        if up and middle:
            self.behind = True
        else:
            self.behind = False

        #self.pos = vec(x - x_offset + x_offset_side, y - y_offset + y_offset_side)
        #self.pos = vec(x - x_offset + x_offset_side, y - y_offset + y_offset_side)
        self.pos = vec(x,y)

        pg.draw.circle(self.game.screen, BLUE, (x-cam_moved[0],y-cam_moved[1]), 5)
        pg.display.update()
        
        #ROTATION
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        if 90 < self.rot + 180 < 270:
            self.rot = int((180 / math.pi) * -math.atan2(rel_y, rel_x))
            is_flipped = False
        else:
            self.rot = int((180 / math.pi) * math.atan2(rel_y, rel_x))
            is_flipped = True
        self.image = pg.transform.flip(pg.transform.rotate(self.game.playerGunImg, self.rot), False, is_flipped)
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
