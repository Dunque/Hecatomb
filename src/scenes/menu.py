import pygame as pg
from src.scenes.scene import Scene

class Menu(Scene):

    def __init__(self, scene_manager):
        self.screen = pg.display.get_surface()
        self.scene_manager = scene_manager

    def on_scene_enter(self):
        pass

    def on_scene_quit(self):
        pass

    def handle_event(self, *args):
        pass

    def update(self, *args):
        pass

    def render(self):
        pass