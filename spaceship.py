from ursina import *
from ursina.prefabs.sprite import Sprite

from crew import Crew
from equipment import Bed

class Spaceship(Entity):

    def __init__(self):
        super().__init__()
        self.active = None
        self.warning_state = False
        self.rooms = {}
        self.crew = {}
        self.equipment = {}

        # siren from https://mixkit.co/free-sound-effects/siren/
        self.siren = Audio("assets/warning", loop=True, autoplay=False)
        self.alarms = []

        # ship statistics
        self.mission_duration = 1.0
        self.fuel = 100.0
    
    def make_room(self, name, x=0, y=0, rotation=0):
        offset = len(self.rooms) * 5.4
        parent = Entity(x=x-offset, y=y, rotation_z=rotation)
        parent.label = Text(name.replace("_", " ").upper(), scale=20, z=-0.1, color=color.gray, origin = (0.0, 0.0), parent=parent)
        parent.top = Entity(parent=parent, model='quad', color=color.gray, collider="box", x=2.6, scale_x=.2, scale_y=1.5)
        parent.mid = Entity(parent=parent, model='quad', color=color.white, collider="box", x=0, scale_x=5, scale_y=2)
        parent.bottom = Entity(parent=parent, model='quad', color=color.red, collider="box", x=-2.6, scale_x=.2, scale_y=1.5)
        self.rooms[name] = parent
        return parent

    def make_centrifuge(self, name, x=3, y=0, rotation=90):
        # top = self.make_room("centrifuge_top", x=3, rotation=90)
        # bottom = self.make_room("centrifuge_bottom", x=-3, rotation=-90)
        offset = len(self.rooms) * 5.4
        parent = Entity(x=x-offset, y=y, rotation_z=rotation)
        parent.top = Entity(parent=parent, model='quad', color=color.blue, collider="box", x=5.1, scale_x=.2, scale_y=0.8)
        parent.mid = Entity(parent=parent, model='quad', color=color.white, collider="box", x=0, scale_x=10, scale_y=1)
        parent.bottom = Entity(parent=parent, model='quad', color=color.red, collider="box", x=-5.1, scale_x=.2, scale_y=0.8)
        self.rooms[name] = parent
        return parent

    def make_active(self, name):
        self.active = self.crew[name]
        self.active.active = True
        for c in self.crew.values():
            if c is not self.active:
                c.active = False

    def add_crew(self, name, x=0, y=0):
        self.crew[name] = Crew(name, ship=self, x=x, y=y)

    def add_bed(self, name, x=0, y=0):
        self.equipment[name] = Bed(name, ship=self, x=x, y=y)

    def sound_warning(self, state):

        if self.warning_state == state:
            return

        if state:
            self.siren.play()

            for room in self.rooms.values():
                self.alarms.append(room.mid.blink(color.red, loop=True, duration=.5))
        else:
            self.siren.pause()
            
            # pause all alarms
            for alarm in self.alarms:
                alarm.pause()
            
            # reset alarms
            self.alarms = []

            # set colour back on mid section
            for room in self.rooms.values():
                room.mid.color = color.white

        self.warning_state = state

    def update(self):

        self.mission_duration += (1.0/60.0) * time.dt
        self.fuel -= 0.1 * time.dt
