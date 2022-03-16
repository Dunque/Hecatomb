import pygame as pg
import numpy as np
from src.settings.settings import *
from src.map.room import Room
from src.map.map import Map

class CutsceneMap(Map):
    def __init__(self, scene, roomsfile, tileset, backgrounds):
        super(CutsceneMap, self).__init__(scene, tileset, backgrounds)
        self.parseRooms(roomsfile)

        self.generateTiles()

    #This function reads the txt file containing the rooms, and it transforms them into
    #string matrices which contain the information of the tiles, objects, enemies etc
    #of the room. It also copies the room into the finalMap variable.
    def parseRooms(self, mapFile):
        with open(mapFile, 'rt',encoding='utf-8') as f:
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