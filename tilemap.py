import pygame as pg
import random
import numpy as np
from sprites import *
from settings import *

vec = pg.math.Vector2

class Map:
    def __init__(self, game, filename):
        self.game = game
        self.mapFile = filename
        self.rooms = []

        self.finalMap = np.empty((80,120), dtype=str)

        self.parseRooms()
    
    def parseRooms(self):
        with open(self.mapFile, 'rt') as f:
            tmpRoom = []
            for line in f:
                if line.__contains__("/"):
                    roomMatrix = np.array(list(map(list, tmpRoom)))
                    #print(roomMatrix)
                    self.rooms.append(roomMatrix)
                    tmpRoom = []
                elif len(line) == 0 or line.isspace():
                    pass
                else:
                    tmpRoom.append(line.strip())
        
        self.joinRooms()

        self.tilewidth = len(self.finalMap[0])
        self.tileheight = len(self.finalMap)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

    #TODO hacer que esto sea aleatorio, y mejorar el mapa global a una matriz enorme en vez de ir
    #juntando matrices pequeñas con el concatenate
    def joinRooms(self):
        # - - - - - 
        # |       |
        # |       |
        # |       |
        # - - - - -
        
        #self.finalMap = np.concatenate([self.rooms[3],self.rooms[2]],axis = 1)
        map1 = np.concatenate([self.rooms[0],self.rooms[2],self.rooms[2],self.rooms[1]],axis = 1)
        map2 = np.concatenate([self.rooms[3],self.rooms[4],self.rooms[4],self.rooms[0]],axis = 1)
        self.finalMap = np.concatenate([map1,map2],axis = 0)

    def closeDoors(self,wallChar,row,col):
        door = 0
        try:
            #These are the limits of the map, so we skip the check
            if row == 0 or col == 0 or row == self.finalMap.shape[1]-1 or row == self.finalMap.shape[0]-1:
                door = 0
            else:
                if self.finalMap[row+1][col] == wallChar:
                    door +=1
                if self.finalMap[row-1][col] == wallChar:
                    door +=1
                if self.finalMap[row][col+1] == wallChar:
                    door +=1
                if self.finalMap[row][col-1] == wallChar:
                    door +=1
        except IndexError as e:
            pass

        if door >= 2:
            pass
        else:
            Wall(self.game, col, row,ROCK_IMAGE) #ahi que mirar que tileset quereis aqui

    def generateMap(self):
        for row in range(self.finalMap.shape[0]):
            for col in range(self.finalMap.shape[1]):
                if self.finalMap[row][col] == '1':
                    Wall(self.game, col, row,FENCE_IMAGE)
                if self.finalMap[row][col] == '2':
                    Wall(self.game, col, row,ARBOL_IMAGE1)
                if self.finalMap[row][col] == '3':
                    Wall(self.game, col, row,ARBOL_IMAGE2)
                if self.finalMap[row][col] == '4':
                    Wall(self.game, col, row,ARBOL_IMAGE3)
                if self.finalMap[row][col] == '5':
                    Wall(self.game, col, row,ARBOL_IMAGE4)
                if self.finalMap[row][col] == 'P':
                    self.game.player = Player(self.game, col, row)
                if self.finalMap[row][col] == 'W':
                    Mob(self.game, col, row)
                if self.finalMap[row][col] == '-':
                    self.closeDoors('-',row,col)     

        self.game.camera = Camera(self.width, self.height)

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

        self.width_height = vec(width,height)
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
                self.x += random.randint(0, self.shakeAmount) - self.shakeAmount // 2
                self.y += random.randint(0, self.shakeAmount) - self.shakeAmount // 2
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