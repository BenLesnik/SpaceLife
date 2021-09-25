from ursina import *
from ursina.prefabs.sprite import Sprite

from crew import Crew
from equipment import Equipment

class Spaceship(object):

    def __init__(self):
        self.active = None
        self.rooms = {}
        self.crew = {}
        self.equipment = {}
    
    def make_room(self, name, x=0, y=0, rotation=0):
        offset = len(self.rooms) * 5.4
        parent = Entity(x=x-offset, y=y, rotation_z=rotation)
        front_airlock = Entity(parent=parent, model='quad', color=color.gray, collider="box", x=2.6, scale_x=.2, scale_y=1.5)
        body = Entity(parent=parent, model='quad', color=color.white, collider="box", x=0, scale_x=5, scale_y=2)
        back_airlock = Entity(parent=parent, model='quad', color=color.gray, collider="box", x=-2.6, scale_x=.2, scale_y=1.5)
        self.rooms[name] = parent

    def make_active(self, name):
        self.active = self.crew[name]
        self.active.active = True
        for c in self.crew.values():
            if c is not self.active:
                c.active = False

        for sf in camera.scripts:
            camera.scripts.remove(sf)
        camera.add_script(SmoothFollow(target=self.crew[name], offset=(0,0,-5)))

    def add_crew(self, name, x=0, y=0):
        self.crew[name] = Crew(name, ship=self, x=x, y=y)

    def add_equipment(self, name, x=0, y=0):
        self.equipment[name] = Equipment(name, x=x, y=y)