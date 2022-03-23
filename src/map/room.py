from abc import ABC, abstractmethod

from src.scenes.score import addScoreClearedRoom
from src.settings.settings import *


class Observer(ABC):

	@abstractmethod
	def startRoom(self):
		pass

class RoomState:
    def __init__(self,room,name):
        self.room = room
        self.name = name
        pass

    def toState(self, targetState):
        self.room.state = targetState

    def update(*args):
        pass

class RoomStateUncleared(RoomState):
    def __init__(self, room, name):
        super(RoomStateUncleared, self).__init__(room, name)

class RoomStatePlaying(RoomState):
    def __init__(self, room, name):
        super(RoomStatePlaying, self).__init__(room, name)
        # close the doors
        self.room.closeAllDoors()
        # acivate the enemies
        for enemy in self.room.enemies:
            self.room.scene.all_sprites.add(enemy)
            enemy.isActive = True

    def update(self):
        if self.room.enemies == []:
            self.room.scene.WIN_ROOM_SOUND.play()
            self.toState(RoomStateCleared(self.room, "CLEARED"))
            # Add score for clearing room
            addScoreClearedRoom()
        else:
            for enemy in self.room.enemies:
                if not enemy.entityData.isAlive:

                    self.room.enemies.remove(enemy)

class RoomStateCleared(RoomState):
    def __init__(self, room, name):
        super(RoomStateCleared, self).__init__(room, name)

        self.room.openAllDoors()

        for obj in self.room.objects:
            obj.isActive = True

    def update(self):
        if self.room.npcs == []:
            pass
        else:
            for npc in self.room.npcs:
                #print(npc.talked)
                if npc.talked:
                    self.room.scene.talkedCount += 1
                    self.room.npcs.remove(npc)


class Room(Observer):
    def __init__(self, scene, matrix, limitX, limitY):
        # Class that defines a room
        # It contains references to the ENEMIES and the DOOR
        # the ENTER DOOR will close once the player enters the room and wont open until he finishes it
        # the EXIT DOOR will open once all enemies are defeated
        self.matrix = matrix
        self.scene = scene

        # Set the room boundaries
        self.limitX0 = limitX
        self.limitX = limitX + ROOMWIDTH - 1
        self.limitY0 = limitY
        self.limitY = limitY + ROOMHEIGHT - 1

        # State of the room can be UNCLEARED, PLAYING or CLEARED
        self.state = RoomStateUncleared(self, "UNCLEARED")

        #Entities present in the room
        self.enemies = []
        self.npcs = []
        self.objects = []
        self.doors = []

    def addDoor(self, door):
        self.doors.append(door)

    def addObject(self, obj):
        self.objects.append(obj)

    def addEnemy(self, enemy):
        self.enemies.append(enemy)

    def addNPC(self, npc):
        self.npcs.append(npc)

    def closeAllDoors(self):
        for door in self.doors:
            door.close()
    
    def openAllDoors(self):
        for door in self.doors:
            door.open()

    def startRoom(self):
        if self.state.name == "UNCLEARED":
            self.state = RoomStatePlaying(self,"PLAYING")
    
    def update(self):
        #print(self.state.name)
        self.state.update()
