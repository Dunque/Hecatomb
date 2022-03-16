import pygame as pg
import numpy as np
from random import randint, choice
from src.entities.player import *
from src.entities.enemies import *
from src.settings.settings import *
from src.entities.objects import *
from src.entities.ground import *
from src.map.camera import *
from src.map.room import Room
from abc import ABC, abstractmethod
from src.entities.npc import NPCBase, TacoTruck

vec = pg.math.Vector2


class Notifier(ABC):

    @abstractmethod
    def notify(self):
        pass

class Map(Notifier):
    def __init__(self, scene, tileset, backgrounds):
        self.scene = scene
        #Load the tileset
        self.tileset = tileset
        self.backgrounds = backgrounds

        self.finalMap = np.empty((5 * ROOMHEIGHT, 5 * ROOMWIDTH), dtype=str)
        self.rooms = []
        
        self.tilewidth = len(self.finalMap[0])
        self.tileheight = len(self.finalMap)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

        self.scene.camera = Camera(self.width, self.height)

        self.isPlaying = True

    #This function gets called each time the symbol parser detects a "-" (a door), and it checks
    #if this door is connected to another door. If it is not, thie function replaces it with a 
    #wall.
    def removeUnusedDoors(self, room, wallChar, row, col):
        nearbyDoorCounter = 0
        try:
            #These are the limits of the map, so we skip the check
            if row == 0 or col == 0 or row == self.finalMap.shape[1]-1 or row == self.finalMap.shape[0]-1:
                nearbyDoorCounter = 0
            else:
                if self.finalMap[row+1][col] == wallChar:
                    nearbyDoorCounter += 1
                if self.finalMap[row-1][col] == wallChar:
                    nearbyDoorCounter += 1
                if self.finalMap[row][col+1] == wallChar:
                    nearbyDoorCounter += 1
                if self.finalMap[row][col-1] == wallChar:
                    nearbyDoorCounter += 1
        except IndexError as e:
            pass

        if nearbyDoorCounter >= 2:
            room.addDoor(Door(self.scene, col, row, self.tileset.tiles[0]))
        else:
            Wall(self.scene, col, row, self.tileset.tiles[15])

    def generateTiles(self):
        for room in self.rooms:
            #First we choose a random floor for the room. This spices things up
            Floor(self.scene, room.limitX0, room.limitY0, choice(self.backgrounds))

            #Now we proceed with the rest of the tiles
            for row in range(room.limitY0, room.limitY+1):
                for col in range(room.limitX0, room.limitX+1):

                    #-----------------------TILES-------------------------
                    if self.finalMap[row][col] == '1':
                        Wall(self.scene, col, row, self.tileset.tiles[25])
                    elif self.finalMap[row][col] == '2':
                        Wall(self.scene, col, row, self.tileset.tiles[23])
                    elif self.finalMap[row][col] == 'E':
                        Wall(self.scene, col, row, self.tileset.tiles[68])
                    elif self.finalMap[row][col] == 'S':
                        Wall(self.scene, col, row, self.tileset.tiles[69])
                    elif self.finalMap[row][col] == 'c':
                        Wall(self.scene, col, row, self.tileset.tiles[70])
                    elif self.finalMap[row][col] == 'u':
                        Wall(self.scene, col, row, self.tileset.tiles[27])
                    elif self.finalMap[row][col] == 'v':
                        Wall(self.scene, col, row, self.tileset.tiles[28])
                    elif self.finalMap[row][col] == 'e':
                        Wall(self.scene, col, row, self.tileset.tiles[42])
                    elif self.finalMap[row][col] == 'a':
                        Wall(self.scene, col, row, self.tileset.tiles[43])
                    elif self.finalMap[row][col] == 'm':
                        Wall(self.scene, col, row, self.tileset.tiles[57])
                    elif self.finalMap[row][col] == 'o':
                        Wall(self.scene, col, row, self.tileset.tiles[58])
                    elif self.finalMap[row][col] == '3':
                        Wall(self.scene, col, row,
                             self.tileset.tiles[15 * randint(1, 7)])

                    elif self.finalMap[row][col] == '-':
                        self.removeUnusedDoors(room, '-', row, col)

                    elif self.finalMap[row][col] == '8':
                        room.addObject(Candelabro(self.scene, col, row))
                    
                    #------------------PLAYER--------------------------
                    elif self.finalMap[row][col] == 'P':
                        self.scene.player = Player(self.scene, col, row)

                    #------------------ENEMIES--------------------------
                    elif self.finalMap[row][col] == 'H':
                        room.addEnemy(HeraldGun(self.scene, col, row))
                    elif self.finalMap[row][col] == 'h':
                        room.addEnemy(HeraldShotgun(self.scene, col, row))

                    elif self.finalMap[row][col] == 'K':
                        room.addEnemy(KhanGun(self.scene, col, row))
                    elif self.finalMap[row][col] == 'k':
                        room.addEnemy(KhanShotgun(self.scene, col, row))

                    elif self.finalMap[row][col] == 'W':
                        room.addEnemy(Worm(self.scene, col, row))
                    elif self.finalMap[row][col] == 'Y':
                        room.addEnemy(Eye(self.scene, col, row))

                    #----------------------NPCS----------------------------
                    elif self.finalMap[row][col] == '4':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=1))
                    elif self.finalMap[row][col] == '5':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=2))
                    elif self.finalMap[row][col] == '6':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=3))
                    elif self.finalMap[row][col] == '7':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=4))
                    elif self.finalMap[row][col] == 'R':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=5))
                    elif self.finalMap[row][col] == 'T':
                        TacoTruck(self.scene, col, row, textLines=[10,11])

                    #----------------------OBJECTS--------------------------
                    elif self.finalMap[row][col] == 'C':
                        room.addObject(Chest(self.scene, col, row, textLines=7))
                    elif self.finalMap[row][col] == 'M':
                        room.addObject(Medkit(self.scene, col, row, 40))
                    elif self.finalMap[row][col] == '0':
                        room.addObject(Exit(self.scene, col, row))

            #We initialize the room doors to be open, until the player wanders in
            room.openAllDoors()

    def notify(self, room, notification):
        if notification == "start":
            room.startRoom()

    def update(self):
        # If the floor is still generating, wait
        if self.isPlaying == False:
            return
        else:
            # Update the active rooms
            for room in self.rooms:
                # Check if the player is in a given room by comparing their limits
                if self.scene.player.hit_rect.x in range((room.limitX0+1)*TILESIZE, (room.limitX-1)*TILESIZE) and self.scene.player.hit_rect.y in range((room.limitY0+1)*TILESIZE, (room.limitY-1)*TILESIZE):
                    self.notify(room, "start")

                room.update()
