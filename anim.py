import pygame as pg

from pygame.math import *

class Anim:
    def __init__(self, sprite_sheet, sprite_size, animation_speed, start_index, end_index):
        self.sprite_sheet = sprite_sheet
        
        frames = []
        for i in range(start_index, end_index):
            frames.append(self.get_sprite_at(i, sprite_size))

        self.frames = frames
        self.current_frame = 0
        self.max_frame = len(self.frames)
        
        self.time_counter = 0
        self.speed = animation_speed

    def get_frame(self):
        self.time_counter+=1
        if self.time_counter%self.speed==0:
            self.current_frame = ((self.current_frame+1)%self.max_frame)
        return self.frames[self.current_frame]

    def get_sprite_at(self, position, size):
        # Returns the image at position (px, py) with size s in the sprite sheet ss
        image_rect = pg.Rect(size[0]*position, 0, size[0], size[1])
        subimage = self.sprite_sheet.subsurface(image_rect)
        
        return subimage