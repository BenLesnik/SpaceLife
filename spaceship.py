from ursina import *
from ursina.prefabs.sprite import Sprite

from crew import Crew
from equipment import Equipment

class Spaceship(object):

    def __init__(self):
        self.active = None
        self.crew = {}
        self.equipment = {}
    
    def make_room(x=0, y=0, rotation=0):
        parent = Entity(x=x, y=y, rotation_z=rotation)
        front_airlock = Entity(parent=parent, model='quad', color=color.gray, collider="box", x=2.6, scale_x=.2, scale_y=1.5)
        body = Entity(parent=parent, model='quad', color=color.white, collider="box", x=0, scale_x=5, scale_y=2)
        back_airlock = Entity(parent=parent, model='quad', color=color.gray, collider="box", x=-2.6, scale_x=.2, scale_y=1.5)

    def make_active(self, name):
        self.active = self.crew[name]
        self.active.active = True
        for c in self.crew.values():
            if c is not self.active:
                c.active = False

    def add_crew(self, name, x=0, y=0):
        self.crew[name] = Crew(name, x=x, y=y)

    def add_equipment(self, name, x=0, y=0):
        self.equipment[name] = Equipment(name, x=x, y=y)