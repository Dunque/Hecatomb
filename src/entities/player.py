import pygame as pg
from src.settings.settings import *
from src.sprites.anim import *
from src.settings.entitydata import *
from src.hud.menus import WeaponMenu
from src.weapons.weapons import *
from src.weapons.bullets import *
from src.entities.states.playerstates import *
from src.entities.character import *
from src.hud.hud import DialogoInGame

vec = pg.math.Vector2

class Player(Character):
    def __init__(self, scene, x, y):

        # Aniamtion stuff
        idleAnim = Anim(scene.playerIdleSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 4)
        walkAnim = Anim(scene.playerWalkSheet,
                        (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 6)
        deathAnim = Anim(scene.playerDeathSheet,
                         (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 10, 0, 7)
        self.dodgeAnim = Anim(scene.playerDodgeSheet,
                         (CHARACTER_SPRITE_SIZE, CHARACTER_SPRITE_SIZE), 7, 0, 5)
        animList = [idleAnim, walkAnim, deathAnim]

        super(Player, self).__init__(scene, x, y, animList,
                                     (scene.all_sprites, scene.player_SG), PlayerStats())
        # AIMING
        self.weaponOffsetX = -20
        self.weaponOffsetY = -10
        self.weapon_slot = None
        self.weapon_menu = WeaponMenu(self.scene)
        self.scene.menus.append(self.weapon_menu)

        # DODGING
        self.dodgeDir = vec(0, 0)

        self.interact = False
        self.state = PlayerGroundedState(self, "GROUNDED")



    def die(self):
        if self.weapon:
            self.weapon.deactivate()
        if self.deathAnim.current_frame == self.deathAnim.max_frame - 1:
            self.scene.player_SG.remove(self)
            self.scene.DEATH_SOUND.play()
            self.kill()

    def allowMovement(self):
        self.state.move = True

    def stopMovement(self):
        self.state.move = False

    def update(self):
        super(Player, self).update()
        self.state.handleInput()

        # WEAPON
        if self.weapon is not None:
            self.weapon.updatePos(self.pos.x - self.weaponOffsetX,
                                  self.pos.y - self.weaponOffsetY, self.rect)

    def change_weapon(self, slot):
        if self.weapon_slot != slot and slot == "top":
            if self.weapon is not None:
                self.weapon.deactivate()
            self.scene.CHANGE_SOUND.play()
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
            self.scene.SWORD_SOUND.play()
            self.weapon = Sword(self.scene, self.pos.x -
                                self.weaponOffsetX, self.pos.y - self.weaponOffsetY)
            pg.mouse.set_visible(True)
            self.weapon.activate()
            self.weapon_slot = slot
        elif self.weapon_slot != slot and slot == "left":
            if self.weapon is not None:
                self.weapon.deactivate()
            self.scene.CHANGE_SOUND.play()
            self.weapon = Shotgun(self.scene, self.pos.x -
                                  self.weaponOffsetX, self.pos.y - self.weaponOffsetY)
            pg.mouse.set_visible(False)
            self.weapon.activate()
            self.weapon_slot = slot

    def takeDamage(self, dmg):
        super(Player, self).takeDamage(dmg)