import random
import numpy as np

room_cats = ['empty', 'blocks', 'checkers']
directions = ['up', 'down', 'left', 'right']

# room_dict is a dictionary of some sample rooms
# the numbers correspond to a certain tile in a tile set
# e.g. the 0s and 3s are floor tiles, and the 20, 28 etc are wall tiles
# tiles 1 are blocks

room_dict = {
    'empty': np.array([[ 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                       [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [ 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
                       [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [ 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]]),
              
    'blocks': np.array([[ 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                        [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [ 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
                        [ 1, 0, 2, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                        [ 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
                        [ 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                        [ 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
                        [ 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                        [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [ 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]]),
               
    'checkers': np.array([[ 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                          [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [ 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                          [ 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
                          [ 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                          [ 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                          [ 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [ 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]])
        }

class maze():
    def __init__(self, w, h):
        # layout is a 2D array that stores all the rooms in the maze
        self.layout = self.generate_maze(w, h)
        
    def generate_maze(self, tiles_wide, tiles_high):
        # this picks a room with a random key from the room_dict and fills 
        # the maze with them
        maze_map = np.array([[room(random.choice(room_cats), (j, i))
                              for i in range(tiles_wide)]
                                for j in range(tiles_high)])
        # make a deep copy of the maze_map so that we can change the rooms
        maze_copy = maze_map.copy()
        w = tiles_wide - 1
        h = tiles_high - 1
        # make doors according to a room's position in the maze
        for i in range(len(maze_copy)):
            for rm in maze_copy[i]:
                # first do the rooms in the corners
                if rm.pos == (0, 0):
                    rm.map = self.make_doors(rm.map, ['down', 'right'])
                elif rm.pos == (0, w):
                    rm.map = self.make_doors(rm.map, ['down', 'left'])
                elif rm.pos == (h, 0):
                    rm.map = self.make_doors(rm.map, ['up', 'right'])
                elif rm.pos == (h, w):
                    rm.map = self.make_doors(rm.map, ['up', 'left'])
                else:
                    # for the rooms not in corners, see if they are at the borders
                    if rm.pos[1] == 0:
                        rm.map = self.make_doors(rm.map, ['down', 'up', 'right'])
                    elif rm.pos[1] == w:
                        rm.map = self.make_doors(rm.map, ['down', 'up', 'left'])
                    elif rm.pos[0] == 0:
                        rm.map = self.make_doors(rm.map, ['left', 'down', 'right'])
                    elif rm.pos[0] == h:
                        rm.map = self.make_doors(rm.map, ['left', 'up', 'right'])
                    else:
                        # if not on the border, place a door in all 4 directions
                        rm.map = self.make_doors(rm.map, ['left', 'up', 'right', 'down'])
        return maze_copy
    
    def make_doors(self, room_map, locations_list):
        # again, copy the array so that changes are permanent
        rm = room_map.copy()
        room_height = len(rm)
        room_width = len(rm[0])
        for location in locations_list:
            # locations_list is a list that contains where doors should be placed
            if location == 'right':
                middle = room_height // 2
                rm[middle - 2][room_width - 1] = 27
                rm[middle - 1][room_width - 1] = rm[middle - 1][room_width - 2]
                rm[middle][room_width - 1] = rm[middle][room_width - 2]
                rm[middle + 1][room_width - 1] = 9
            elif location == 'up':
                middle = room_width // 2
                rm[0][middle - 2] = 29
                rm[0][middle - 1] = rm[1][middle - 2]
                rm[0][middle] = rm[1][middle]
                rm[0][middle + 1] = 27
            elif location == 'left':
                middle = room_height // 2
                rm[middle - 2][0] = 29
                rm[middle - 1][0] = rm[middle - 1][1]
                rm[middle][0] = rm[middle][1]
                rm[middle + 1][0] = 11
            elif location == 'down':
                middle = room_width // 2
                rm[room_height - 1][middle - 2] = 11
                rm[room_height - 1][middle - 1] = rm[room_height - 2][middle - 1]
                rm[room_height - 1][middle] = rm[room_height - 2][middle]
                rm[room_height - 1][middle + 1] = 9
    
        return rm

class room():
    # a room class containing its category, position in the maze, its 
    # tilemap and maybe some other things in the future (objects, flags etc.)
    def __init__(self, cat='empty', pos=(0, 0)):
        self.cat = cat
        self.pos = pos
        self.map = room_dict[cat]
        # some examples for additional variables (not used yet)
        self.visited = False
        self.enemies = 0
        self.clear = False
        self.dark = False
        self.color_palette = 'grey_dungeon'


""" # test
test_maze = maze(4, 4)

for i in range(len(test_maze.layout)):
            for rm in test_maze.layout[i]:
                
                print(rm.map) """