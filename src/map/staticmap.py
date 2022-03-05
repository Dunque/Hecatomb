import pygame as pg
import numpy as np
from random import seed, randint, random, choice
from src.entities.player import *
from src.entities.enemies import *
from src.settings.settings import *
from src.sprites.tileset import Tileset
from src.entities.objects import Chest
from src.entities.ground import *
from src.map.camera import *
from src.map.room import Room
from abc import ABC, abstractmethod

vec = pg.math.Vector2


class Notifier(ABC):

    @abstractmethod
    def notify(self):
        pass

class StaticMap(Notifier):
    def __init__(self, scene, roomsfile):
        self.scene = scene

        self.rooms = []

        #This boolean dictates if the map is active or not
        self.isPlaying = False

        #Load the tileset
        self.tileset = Tileset(
            "./sprites/tilesetAshlands.png", (TILESIZE, TILESIZE), 0, 0)

        self.finalMap = self.parseFullMap(roomsfile)
        
        self.parseRooms()

        self.generateTiles()

        self.tilewidth = len(self.finalMap[0])
        self.tileheight = len(self.finalMap)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

        self.scene.camera = Camera(self.width, self.height)

        self.isPlaying = True

    #This function reads the txt file containing the rooms, and it transforms them into
    #string matrices which contain the information of the tiles, objects, enemies etc
    #of the room
    def parseRooms(self):
        for row in range(5):
            for col in range(5):
                roomMatrix = self.finalMap[row*ROOMHEIGHT: (row*ROOMHEIGHT + ROOMHEIGHT), col*ROOMWIDTH: (col*ROOMWIDTH + ROOMWIDTH)]
                self.rooms.append(
                    Room(self.scene, roomMatrix, col*ROOMWIDTH, row*ROOMHEIGHT))

    def parseFullMap(self, mapFile):
        with open(mapFile, 'rt') as f:
            tmpRoom = []
            for line in f:
                tmpRoom.append(line.strip())
            matrix = np.array(list(map(list, tmpRoom)))
        return matrix


    def generateTiles(self):
        for room in self.rooms:
            #First we choose a random floor for the room. This spices things up
            n_img = randint(1, 4)
            if n_img == 1:
                Floor(self.scene, room.limitX0,
                      room.limitY0, self.scene.background1)
            elif n_img == 2:
                Floor(self.scene, room.limitX0,
                      room.limitY0, self.scene.background2)
            elif n_img == 3:
                Floor(self.scene, room.limitX0,
                      room.limitY0, self.scene.background3)
            elif n_img == 4:
                Floor(self.scene, room.limitX0,
                      room.limitY0, self.scene.background4)
            #Now we proceed with the rest of the tiles
            for row in range(room.limitY0, room.limitY+1):
                for col in range(room.limitX0, room.limitX+1):
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
                    elif self.finalMap[row][col] == 'P':
                        self.scene.player = Player(self.scene, col, row)
                    elif self.finalMap[row][col] == 'H':
                        room.addEnemy(Herald(self.scene, col, row))
                    elif self.finalMap[row][col] == 'K':
                        room.addEnemy(Khan(self.scene, col, row))
                    elif self.finalMap[row][col] == 'W':
                        room.addEnemy(Worm(self.scene, col, row))
                    elif self.finalMap[row][col] == '-':
                        room.addDoor(Door(self.scene, col, row, ROCK_IMAGE))
                    elif self.finalMap[row][col] == 'C':
                        Chest(self.scene, col, row)
                        pass
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
