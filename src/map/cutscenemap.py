import pygame as pg
import numpy as np
from random import randint
from src.entities.player import *
from src.entities.enemies import *
from src.settings.settings import *
from src.sprites.tileset import Tileset
from src.entities.objects import *
from src.entities.ground import *
from src.map.camera import *
from src.map.room import Room
from abc import ABC, abstractmethod
from src.entities.npc import NPCBase

vec = pg.math.Vector2


class Notifier(ABC):

    @abstractmethod
    def notify(self):
        pass


class CutsceneMap(Notifier):
    def __init__(self, scene, roomsfile):
        self.scene = scene

        #This boolean dictates if the map is active or not
        self.isPlaying = False

        #Load the tileset
        self.tileset = Tileset(
            "./sprites/tilesetAshlands.png", (TILESIZE, TILESIZE), 0, 0)

        self.finalMap = np.empty((ROOMHEIGHT, ROOMWIDTH), dtype=str)

        self.rooms = []
        
        self.parseRooms(roomsfile)

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
    def parseRooms(self, mapFile):

        with open(mapFile, 'rt') as f:
            tmpRoom = []
            for line in f:
                if line.__contains__("/"):
                    roomMatrix = np.array(list(map(list, tmpRoom)))
                elif len(line) == 0 or line.isspace():
                    pass
                else:
                    tmpRoom.append(line.strip())

        #Insert the room in the room list
        self.rooms.append(Room(self.scene, roomMatrix, 0, 0))
        #Copy it to the global map. In this case, the global map is only one room
        i = 0
        j = 0
        #Copy it to the position relative to the global map
        for row in range(0, ROOMHEIGHT):
            for col in range(0, ROOMWIDTH):
                self.finalMap[row][col] = tmpRoom[i][j]
                j += 1
            i += 1
            j = 0

    def generateTiles(self):
        for room in self.rooms:
            #First we choose a random floor for the room. This spices things up
            Floor(self.scene, room.limitX0,
                room.limitY0, self.scene.background1)
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
                    elif self.finalMap[row][col] == 'C':
                        Chest(self.scene, col, row, textLines=7)
                    elif self.finalMap[row][col] == '4':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=1))
                    elif self.finalMap[row][col] == '5':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=2))
                    elif self.finalMap[row][col] == '6':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=3))
                    elif self.finalMap[row][col] == '7':
                        room.addNPC(NPCBase(self.scene, col, row, textLines=4))
                    elif self.finalMap[row][col] == '8':
                        room.addObject(Candelabro(self.scene, col, row))
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
                self.notify(room, "start")
                room.update()
