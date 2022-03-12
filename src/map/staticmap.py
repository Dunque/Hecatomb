import pygame as pg
import numpy as np
from random import seed
from src.settings.settings import *
from src.map.room import Room
from src.map.map import Map

class StaticMap(Map):
    def __init__(self, scene, roomsfile, tileset, backgrounds):
        super(StaticMap,self).__init__(scene, roomsfile, tileset, backgrounds)

        self.finalMap = self.parseFullMap(roomsfile)
        self.parseRooms()
        seed(1)
        self.generateTiles()

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
        with open(mapFile, 'rt',encoding='utf-8') as f:
            tmpRoom = []
            for line in f:
                tmpRoom.append(line.strip())
            matrix = np.array(list(map(list, tmpRoom)))
        return matrix