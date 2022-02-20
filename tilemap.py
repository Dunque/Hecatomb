import pygame as pg
import numpy as np
from random import seed, randint, random, choice
from sprites import *
from settings import *

vec = pg.math.Vector2

#el generador de mapas furrula asi:
#tu pones unas salas en el txt, una de ellas tiene que tener
#el spawn del jugador, y otra de ellas tiene que tener
#la salida. LAs habiaciones se ponen una a una en el mapa
#interconectadas de forma aleatoria, pero se pone solo
#una vez cada una. Es decir, si queremos tener 8 salas,
#ponemos 8 salas en el txt, y si queremos tener 2 veces la
#misma sala, la duplicamos en el txt.
class Map:
    def __init__(self, scene, filename):
        self.scene = scene
        self.mapFile = filename
        
        self.tmpRooms = []
        self.rooms = []
        self.roomData = []

        #This boolean dictates if the map is active or not
        self.isPlaying = False

        #The final mal will be a string matrix initialized to contain all empty strings
        #Later, it will be filled with each room's data
        self.finalMap = np.empty((5 * ROOMHEIGHT, 5 * ROOMWIDTH), dtype=str)

        self.parseRooms()

        self.joinRooms()

        self.tilewidth = len(self.finalMap[0])
        self.tileheight = len(self.finalMap)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

    #This function reads the txt file containing the rooms, and it transforms them into
    #string matrices which contain the information of the tiles, objects, enemies etc
    #of the room
    def parseRooms(self):
        with open(self.mapFile, 'rt') as f:
            tmpRoom = []
            for line in f:
                if line.__contains__("/"):
                    roomMatrix = np.array(list(map(list, tmpRoom)))
                    self.tmpRooms.append(roomMatrix)
                    tmpRoom = []
                elif len(line) == 0 or line.isspace():
                    pass
                else:
                    tmpRoom.append(line.strip())

    #This function inserts the first room in a random position in a 5x5 room grid.
    #Then, for each consequent room, it checks if their adyacent spaces are empty,
    #and adds all free possible spaces into an array. Finally, it takes one random
    #free space and places the next room in there. This process is repeated until
    #all rooms have been placed in the grid
    def joinRooms(self):

        # Random seed
        seed()
        
        #Avaliable rooms for the generator
        avaliableRooms = self.tmpRooms

        # Random position to insert the first room
        x = randint(0,4)
        y = randint(0,4)
        #x = 1
        #y = 4
        print("initial x,y: ", x*ROOMWIDTH, ", ", y*ROOMHEIGHT)

        roomMatrix = avaliableRooms.pop(0)
        #print(roomMatrix)
        i = 0
        j = 0
        #Copy it to the position relative to the global map
        for row in range(y*ROOMHEIGHT, y*ROOMHEIGHT + ROOMHEIGHT):
            for col in range(x*ROOMWIDTH, x*ROOMWIDTH + ROOMWIDTH):
                self.finalMap[row][col] = roomMatrix[i][j]
                j += 1
            i += 1
            j = 0

        #Store the room in a list, including it's coordinates in the final map
        self.rooms.append(Room(roomMatrix, x*ROOMWIDTH, y*ROOMHEIGHT))

        # Now we continue with the rest of the rooms
        # We repeat this loop until we have chosen a position for each room in the avaliableRooms list
        avaliablePositions = []
        l = 0
        while len(avaliableRooms) > 0:
            #We check the four cardinal directions of each room we have placed, to insert a new one
            #in any of those free directions

            room = self.rooms[l]

            try:
                #Above the actual room
                if room.limitY0 != 0 and self.finalMap[room.limitY0-ROOMHEIGHT][room.limitX0] == "":
                    avaliablePositions.append((room.limitX0,room.limitY0-ROOMHEIGHT))
                    print("room ", l, " above in: : ", room.limitX0, ", ", room.limitY0-ROOMHEIGHT)
            except IndexError as e:
                pass

            try:       
                #Below the actual room
                if room.limitY != self.finalMap.shape[0] and self.finalMap[room.limitY0+ROOMHEIGHT][room.limitX0] == "":
                    avaliablePositions.append((room.limitX0,room.limitY0+ROOMHEIGHT))
                    print("room ", l, " below in: : ", room.limitX0, ", ", room.limitY0+ROOMHEIGHT)
            except IndexError as e:
                pass

            try:        
                #To the left of the actual room
                if room.limitX0 != 0 and self.finalMap[room.limitY0][room.limitX0-ROOMWIDTH] == "":
                    avaliablePositions.append((room.limitX0-ROOMWIDTH,room.limitY0))
                    print("room ", l, " to the left in: : ", room.limitX0-ROOMWIDTH, ", ", room.limitY0)
            except IndexError as e:
                pass

            try:   
                #To the right of the actual room
                if room.limitX != self.finalMap.shape[1] and self.finalMap[room.limitY0][room.limitX0+ROOMWIDTH] == "":
                    avaliablePositions.append((room.limitX0+ROOMWIDTH,room.limitY0))
                    print("room ", l, " to the right in: : ", room.limitX0+ROOMWIDTH, ", ", room.limitY0)
            except IndexError as e:
                pass
            
            l+=1
            
            print("Avaliable positions: ", avaliablePositions)
            print()
            print("--------------------------------------------")
            print()
            #We choose randomly where to insert the next room from all the avaliable spaces
            pos = choice(avaliablePositions)
            #We remove the chosen position from the list, as we are going to insert a room there, so it's no longer avaliable
            avaliablePositions = list(filter((pos).__ne__, avaliablePositions))
            print("next x,y: ", pos[0], ", ", pos[1])

            #Get the room out of the room list and instert it in the global map
            roomMatrix = avaliableRooms.pop(0)
            i = 0
            j = 0
            #Copy it to the position relative to the global map
            for row in range(pos[1], pos[1] + ROOMHEIGHT):
                for col in range(pos[0], pos[0] + ROOMWIDTH):
                    self.finalMap[row][col] = roomMatrix[i][j]
                    j += 1
                i += 1
                j = 0
            
            #Store the room in a list, including it's coordinates in the final map
            print("ROOM TO INSERT: ", pos[0], ", ", pos[1])
            self.rooms.append(Room(roomMatrix, pos[0], pos[1]))
            print(self.rooms)
            print("size of len(self.rooms): ", len(self.rooms))

    def closeDoors(self, wallChar, row, col):
        door = 0
        try:
            #These are the limits of the map, so we skip the check
            if row == 0 or col == 0 or row == self.finalMap.shape[1]-1 or row == self.finalMap.shape[0]-1:
                door = 0
            else:
                if self.finalMap[row+1][col] == wallChar:
                    door += 1
                if self.finalMap[row-1][col] == wallChar:
                    door += 1
                if self.finalMap[row][col+1] == wallChar:
                    door += 1
                if self.finalMap[row][col-1] == wallChar:
                    door += 1
        except IndexError as e:
            pass

        if door >= 2:
            pass
        else:
            # ahi que mirar que tileset quereis aqui
            Wall(self.scene, col, row, ROCK_IMAGE)

    def generateMap(self):
        for row in range(self.finalMap.shape[0]):
            for col in range(self.finalMap.shape[1]):
                if self.finalMap[row][col] == '1':

                    n_img=randint(1,6)
                    if n_img==1:
                        Wall(self.scene, col, row, ARBUSTO_IMAGE_1)
                    elif n_img == 2:
                        Wall(self.scene, col, row, ARBUSTO_IMAGE_2)
                    elif n_img == 3:
                        Wall(self.scene, col, row, ROCK_IMAGE_2)
                    elif n_img == 4:
                        Wall(self.scene, col, row, ROCK_IMAGE_3)
                    elif n_img == 5:
                        Wall(self.scene, col, row, ROCK_IMAGE_4)
                    elif n_img == 6:
                        Wall(self.scene, col, row, ROCK_IMAGE_5)
                elif self.finalMap[row][col] == 't':
                    Wall(self.scene, col, row,TRUNK_IMAGE1)
                elif self.finalMap[row][col] == 'r':
                    Wall(self.scene, col, row,TRUNK_IMAGE2)
                elif self.finalMap[row][col] == 'o':
                    Wall(self.scene, col, row,TRUNK_IMAGE3)
                elif self.finalMap[row][col] == '2':
                    Wall(self.scene, col, row, ARBOL_IMAGE1)
                elif self.finalMap[row][col] == '3':
                    Wall(self.scene, col, row, ARBOL_IMAGE2)
                elif self.finalMap[row][col] == '4':
                    Wall(self.scene, col, row, ARBOL_IMAGE3)
                elif self.finalMap[row][col] == '5':
                    Wall(self.scene, col, row, ARBOL_IMAGE4)
                elif self.finalMap[row][col] == 'P':
                    self.scene.player = Player(self.scene, col, row)
                elif self.finalMap[row][col] == 'W':
                    Worn(self.scene, col, row)
                elif self.finalMap[row][col] == 'B':
                    Bully(self.scene, col, row)
                elif self.finalMap[row][col] == '-':
                    self.closeDoors('-', row, col)

        self.scene.camera = Camera(self.width, self.height)

    def update(self):
        # If the floor is still generating, wait
        if self.isPlaying == False:
            return
        else:
                # Update the active rooms
            for (boundaries, room) in self.rooms:
                if self.scene.player.rect.x in range(boundaries[0]+2*TILESIZE, boundaries[1]):
                    if room.state == "UNCLEARED":
                        room.start_room()

                room.update()

                    #Above the actual room
                    # if room.limitY0 != 0 and self.finalMap[room.limitY0-ROOMHEIGHT][room.limitX0] == "":
                    #     avaliablePositions.append((room.limitX0,room.limitY0-ROOMHEIGHT))
                    #     print("room above in: : ", room.limitX0, ", ", room.limitY0-ROOMHEIGHT)
                            
                    # #Below the actual room
                    # if room.limitY != self.finalMap.shape[0] and self.finalMap[room.limitY0+ROOMHEIGHT][room.limitX0] == "":
                    #     avaliablePositions.append((room.limitX0,room.limitY0+ROOMHEIGHT))
                    #     print("room below in: : ", room.limitX0, ", ", room.limitY0+ROOMHEIGHT)
                            
                    # #To the left of the actual room
                    # if room.limitX0 != 0 and self.finalMap[room.limitY0][room.limitX0-ROOMWIDTH] == "":
                    #     avaliablePositions.append((room.limitX0-ROOMWIDTH,room.limitY0))
                    #     print("room to the left in: : ", room.limitX0-ROOMWIDTH, ", ", room.limitY0)
                        
                    # #To the right of the actual room
                    # if room.limitX != self.finalMap.shape[1] and self.finalMap[room.limitY0][room.limitX0+ROOMWIDTH] == "":
                    #     avaliablePositions.append((room.limitX0+ROOMWIDTH,room.limitY0))
                    #     print("room to the right in: : ", room.limitX0+ROOMWIDTH, ", ", room.limitY0)

class Room:
    def __init__(self, matrix, limitX, limitY):
        # Class that defines a room
        # It contains references to the ENEMIES and the DOOR
        # the ENTER DOOR will close once the player enters the room and wont open until he finishes it
        # the EXIT DOOR will open once all enemies are defeated
        self.matrix = matrix

        # Set the room boundaries in x axis
        self.limitX0 = limitX
        self.limitX = limitX + ROOMWIDTH - 1
        self.limitY0 = limitY
        self.limitY = limitY + ROOMHEIGHT - 1

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

        self.width_height = vec(width, height)
        self.halfs = vec(int(WIDTH / 2), int(HEIGHT / 2))
        self.def_cords = vec(CAMERA_X, CAMERA_Y)

        self.def_cords = vec(CAMERA_X, CAMERA_Y)

        self.x = 0
        self.y = 0

        #Camera shake
        self.doShake = False
        self.shakeMaxTime = 0
        self.shakeTimer = 0
        self.shakeAmount = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def get_moved(self):
        return self.x, self.y

    def update(self, target):
        self.x = -target.rect.centerx + int(WIDTH / 2)
        self.y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - WIDTH), self.x)  # right
        self.y = max(-(self.height - HEIGHT), self.y)  # bottom

        # Shake logic
        if self.doShake:
            if (self.shakeTimer <= self.shakeMaxTime):
                self.shakeTimer += 1
                self.x += randint(0, self.shakeAmount) - \
                    self.shakeAmount // 2
                self.y += randint(0, self.shakeAmount) - \
                    self.shakeAmount // 2
            else:
                self.doShake = False
                self.shakeMaxTime = 0
                self.shakeTimer = 0
                self.shakeAmount = 0

        self.camera = pg.Rect(self.x, self.y, self.width, self.height)

    def cameraShake(self, amount, time):
        self.doShake = True
        self.shakeAmount = amount
        self.shakeMaxTime = time
