#from matplotlib.style import available
import pygame as pg
import numpy as np
from random import seed, randint, choice
from src.settings.settings import *
from src.entities.ground import *
from src.map.room import Room
from src.map.map import Map

#el generador de mapas furrula asi:
#tu pones unas salas en el txt, una de ellas tiene que tener
#el spawn del jugador, y otra de ellas tiene que tener
#la salida. LAs habiaciones se ponen una a una en el mapa
#interconectadas de forma aleatoria, pero se pone solo
#una vez cada una. Es decir, si queremos tener 8 salas,
#ponemos 8 salas en el txt, y si queremos tener 2 veces la
#misma sala, la duplicamos en el txt.
class RandMap(Map):
    def __init__(self, scene, roomsfile, tileset, backgrounds):
        super(RandMap,self).__init__(scene, roomsfile, tileset, backgrounds)

        self.tmpRooms = self.parseRooms(roomsfile)
        self.randomizeRooms()

    #This function reads the txt file containing the rooms, and it transforms them into
    #string matrices which contain the information of the tiles, objects, enemies etc
    #of the room
    def parseRooms(self, mapFile):
        tmpRooms = []
        with open(mapFile, 'rt',encoding='utf-8') as f:
            tmpRoom = []
            for line in f:
                if line.__contains__("/"):
                    roomMatrix = np.array(list(map(list, tmpRoom)))
                    tmpRooms.append(roomMatrix)
                    tmpRoom = []
                elif len(line) == 0 or line.isspace():
                    pass
                else:
                    tmpRoom.append(line.strip())
        return tmpRooms

    #This function copies the contents of a given room into the global map
    def insertRoomInMap(self,roomMatrix, x, y):
        i = 0
        j = 0
        #Copy it to the position relative to the global map
        for row in range(y, y + ROOMHEIGHT):
            for col in range(x, x + ROOMWIDTH):
                self.finalMap[row][col] = roomMatrix[i][j]
                j += 1
            i += 1
            j = 0

    #This function inserts the first room in a random position in a 5x5 room grid.
    #Then, for each consequent room, it checks if their adyacent spaces are empty,
    #and adds all free possible spaces into an array. Finally, it takes one random
    #free space and places the next room in there. This process is repeated until
    #all rooms have been placed in the grid
    def randomizeRooms(self):
        # Random seed
        seed()
        #Avaliable rooms for the generator
        avaliableRooms = self.tmpRooms
        # Random position to insert the first room
        x = randint(0,4)
        y = randint(0,4)
        #Insert the room in the global map
        roomMatrix = avaliableRooms.pop(0)
        self.insertRoomInMap(roomMatrix, x*ROOMWIDTH, y*ROOMHEIGHT)

        #Store the room in a list, including it's coordinates in the final map
        self.rooms.append(Room(self.scene, roomMatrix, x*ROOMWIDTH, y*ROOMHEIGHT))

        # Now we continue with the rest of the rooms
        # We repeat this loop until we have chosen a position for each room in the avaliableRooms list
        avaliablePositions = []
        l = 0
        while len(avaliableRooms) > 0:
            #We check the four cardinal directions of each room we have placed, to insert a new one
            #in any of those free directions
            room = self.rooms[l]
            avaliablePositions.extend(self.checkAdyacentSpaces(room))
            l+=1
            #We choose randomly where to insert the next room from all the avaliable spaces
            pos = choice(avaliablePositions)
            #We remove the chosen position from the list, as we are going to insert a room there, so it's no longer avaliable
            avaliablePositions = list(filter((pos).__ne__, avaliablePositions))

            #Get the room out of the room list and instert it in the global map
            roomMatrix = avaliableRooms.pop(0)
            self.insertRoomInMap(roomMatrix, pos[0], pos[1])
            self.rooms.append(Room(self.scene, roomMatrix, pos[0], pos[1]))

    def checkAdyacentSpaces(self,room):
        avaliablePositions = []
        try:
            #Above the actual room
            if room.limitY0 != 0 and self.finalMap[room.limitY0-ROOMHEIGHT][room.limitX0] == "":
                avaliablePositions.append((room.limitX0,room.limitY0-ROOMHEIGHT))
        except IndexError as e:
            pass
        try:       
            #Below the actual room
            if room.limitY != self.finalMap.shape[0] and self.finalMap[room.limitY0+ROOMHEIGHT][room.limitX0] == "":
                avaliablePositions.append((room.limitX0,room.limitY0+ROOMHEIGHT))
        except IndexError as e:
            pass
        try:        
            #To the left of the actual room
            if room.limitX0 != 0 and self.finalMap[room.limitY0][room.limitX0-ROOMWIDTH] == "":
                avaliablePositions.append((room.limitX0-ROOMWIDTH,room.limitY0))
        except IndexError as e:
            pass
        try:   
            #To the right of the actual room
            if room.limitX != self.finalMap.shape[1] and self.finalMap[room.limitY0][room.limitX0+ROOMWIDTH] == "":
                avaliablePositions.append((room.limitX0+ROOMWIDTH,room.limitY0))
        except IndexError as e:
            pass
        return avaliablePositions

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
            room.addDoor(Door(self.scene, col, row, ROCK_IMAGE))
        else:
            Wall(self.scene, col, row, self.tileset.tiles[15])