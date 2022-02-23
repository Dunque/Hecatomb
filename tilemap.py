from matplotlib.style import available
import pygame as pg
import numpy as np
from random import seed, randint, random, choice
from sprites import *
from settings import *
from tileset import Tileset

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
    def __init__(self, scene, roomsfile):
        self.scene = scene
        
        self.rooms = []

        #This boolean dictates if the map is active or not
        self.isPlaying = False

        #Load the tileset
        self.tileset = Tileset("./sprites/tilesetAshlands.png", (TILESIZE,TILESIZE), 0, 0)

        #The final mal will be a string matrix initialized to contain all empty strings
        #Later, it will be filled with each room's data
        self.finalMap = np.empty((5 * ROOMHEIGHT, 5 * ROOMWIDTH), dtype=str)

        self.tmpRooms = self.parseRooms(roomsfile)

        self.randomizeRooms()

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
        tmpRooms = []
        with open(mapFile, 'rt') as f:
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

    def generateTiles(self):
        for room in self.rooms:
            #First we choose a random floor for the room. This spices up things
            n_img=randint(1,4)
            if n_img==1:
                Floor(self.scene, room.limitX0, room.limitY0, self.scene.background1)
            elif n_img == 2:
                Floor(self.scene, room.limitX0, room.limitY0, self.scene.background2)
            elif n_img == 3:
                Floor(self.scene, room.limitX0, room.limitY0, self.scene.background3)
            elif n_img == 4:
                Floor(self.scene, room.limitX0, room.limitY0, self.scene.background4)
            #Now we proceed with the rest of the tiles
            for row in range(room.limitY0,room.limitY+1):
                for col in range(room.limitX0,room.limitX+1):
                    if self.finalMap[row][col] == '1':
                        Wall(self.scene, col, row, self.tileset.tiles[25])
                    elif self.finalMap[row][col] == '2':
                        Wall(self.scene, col, row, self.tileset.tiles[23])
                    elif self.finalMap[row][col] == '3':
                        n_img=randint(1,7)
                        if n_img==1:
                            Wall(self.scene, col, row, self.tileset.tiles[15])
                        elif n_img == 2:
                            Wall(self.scene, col, row, self.tileset.tiles[30])
                        elif n_img == 3:
                            Wall(self.scene, col, row, self.tileset.tiles[45])
                        elif n_img == 4:
                            Wall(self.scene, col, row, self.tileset.tiles[60])
                        elif n_img == 5:
                            Wall(self.scene, col, row, self.tileset.tiles[75])
                        elif n_img == 6:
                            Wall(self.scene, col, row, self.tileset.tiles[90])
                        elif n_img == 7:
                            Wall(self.scene, col, row, self.tileset.tiles[105])
                    elif self.finalMap[row][col] == 'P':
                        self.scene.player = Player(self.scene, col, row)
                    elif self.finalMap[row][col] == 'H':
                        room.addEnemy(Herald(self.scene, col, row))    
                    elif self.finalMap[row][col] == 'K':
                        room.addEnemy(Khan(self.scene, col, row))
                    elif self.finalMap[row][col] == 'W':
                        room.addEnemy(Worm(self.scene, col, row))
                    elif self.finalMap[row][col] == '-':
                        self.removeUnusedDoors(room,'-', row, col)
            #We initialize the room doors to be open, until the player wanders in
            room.openAllDoors()

    def update(self):
        # If the floor is still generating, wait
        if self.isPlaying == False:
            return
        else:
            # Update the active rooms
            for room in self.rooms:
                # Check if the player is in a given room by comparing their limits
                if self.scene.player.hit_rect.x in range((room.limitX0+1)*TILESIZE, (room.limitX-1)*TILESIZE) and self.scene.player.hit_rect.y in range((room.limitY0+1)*TILESIZE, (room.limitY-1)*TILESIZE):
                    if room.state == "UNCLEARED":
                        room.start_room()
                room.update()

class Room():
    def __init__(self, scene, matrix, limitX, limitY):
        # Class that defines a room
        # It contains references to the ENEMIES and the DOOR
        # the ENTER DOOR will close once the player enters the room and wont open until he finishes it
        # the EXIT DOOR will open once all enemies are defeated
        self.matrix = matrix
        self.scene = scene

        # Set the room boundaries in x axis
        self.limitX0 = limitX
        self.limitX = limitX + ROOMWIDTH - 1
        self.limitY0 = limitY
        self.limitY = limitY + ROOMHEIGHT - 1

        # State of the room can be UNCLEARED, PLAYING or CLEARED
        self.state = "UNCLEARED"

        #Entities present in the room
        self.enemies = []
        self.objects = []
        self.doors = []

    def addDoor(self, door):
        self.doors.append(door)

    def addObject(self, obj):
        self.objects.append(obj)

    def addEnemy(self, enemy):
        self.enemies.append(enemy)

    def closeAllDoors(self):
        for door in self.doors:
            door.close()
    
    def openAllDoors(self):
        for door in self.doors:
            door.open()

    def start_room(self):
        print(self.doors)
        print(self.enemies)
        # close the doors
        self.closeAllDoors()
                
        # acivate the enemies
        for enemy in self.enemies:
            self.scene.all_sprites.add(enemy)
            enemy.isActive = True
                
        self.state = "PLAYING"
    
    def switch_state(self):
        if self.state == "UNCLEARED":
            pass
        if self.state == "PLAYING":
            if self.enemies == []:
                self.state = "CLEARED"
                self.openAllDoors()
        if self.state == "CLEARED":
            pass
    
    def update(self):
        for enemy in self.enemies:
            if not enemy.entityData.isAlive:
                self.enemies.remove(enemy)
                
        self.switch_state()


class Camera:
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

        self.width_height = vec(width, height)
        self.halfs = vec(int(WIDTH / 2), int(HEIGHT / 2))
        self.def_cords = vec(CAMERA_X, CAMERA_Y)

        self.x = 0
        self.y = 0

        #Camera shake
        self.doShake = False
        self.shakeMaxTime = 0
        self.shakeTimer = 0
        self.shakeAmount = 0

    def apply(self, entity):
        return entity.rect.move(self.rect.topleft)

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

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def cameraShake(self, amount, time):
        self.doShake = True
        self.shakeAmount = amount
        self.shakeMaxTime = time