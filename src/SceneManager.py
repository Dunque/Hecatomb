import pygame as pg
import sys
from .settings import *

class SceneManager:

    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.scenes = {}
        self.current_scene = None

    def get_scene(self, scene_id: int):
        return self.scenes.get(scene_id)

    def set_scene(self, scene, sc_id: int):
        self.scenes[sc_id] = scene

    def go_to(self, scene_id: int):
        last_scene = self.current_scene
        if last_scene:
            last_scene.on_scene_quit()

        self.current_scene = self.get_scene(scene_id)
        self.current_scene.on_scene_enter()

    def loop(self):
        time = self.clock.tick(FPS)
        while True:
            self.current_scene.handle_event(pg.event.get())
            self.current_scene.update(time)
            self.current_scene.render()

    def quit_program(self):
        pg.quit()
        sys.exit()