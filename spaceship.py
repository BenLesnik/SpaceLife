from ursina import *
from ursina.prefabs.sprite import Sprite

from crew import Crew
from equipment import Equipment


class Room(Entity):

    def __init__(self, name, ship, x=0, y=0, rotation=0):
        offset = len(ship.rooms) * 5.4
        super().__init__(x=x-offset, y=y, rotation_z=rotation)
        
        self.ship = ship
        self.parent=ship

        self.crew = {}
        self.equipment = {}
        
        self.label = Text(name.replace("_", " ").upper(), scale=20, z=-0.1, color=color.gray, origin = (0.0, 0.0), parent=self)
        self.top = Entity(parent=self, model='quad', color=color.gray, collider="box", x=2.6, scale_x=.2, scale_y=0.8)
        self.mid = Entity(parent=self, model='quad', color=color.light_gray, collider="box", x=0, scale_x=5, scale_y=2)
        self.mid.texture = "assets/medbay"
        self.bottom = Entity(parent=self, model='quad', color=color.gray, collider="box", x=-2.6, scale_x=.2, scale_y=0.8)

    def add_crew(self, name, x=0, y=0):
        return Crew(name, ship=self.ship, room=self, x=x, y=y)

    def add_bed(self, name, x=0, y=0):
        bed = Equipment(name, texture="assets/bed", ship=self.ship, room=self, x=x, y=y)
        bed.post_walk = [Wait(2.5), Func(bed.set_crew_attr, "tiredness", 0.0)]
        return bed
    
    def add_chair(self, name, x=0, y=0):
        return Equipment(name, texture="assets/chair", ship=self.ship, room=self, x=x, y=y)

class Spaceship(Entity):

    def __init__(self):
        super().__init__()
        self.active = None
        self.warning_state = False
        self.shaking = None
        self.rooms = {}
        self.crew = {}
        self.equipment = {}

        # siren from https://mixkit.co/free-sound-effects/siren/
        self.siren = Audio("assets/warning", loop=True, autoplay=False)
        self.siren.volume = 0.5
        self.alarms = []

        # ship statistics
        self.mission_duration = 1.0
        self.oxygen = 100.0
        self.fuel = 100.0
        self.food = 100.0
        self.damage = 0.0
        self.radiation = 0.0
    
    def make_room2(self, name, x=4.4, y=0, rotation=0):

        self.rooms[name] = Room(name, self, x, y, rotation)
        return self.rooms[name]

    def make_room(self, name, x=0, y=0, rotation=0):

        self.rooms[name] = Room(name, self, x, y, rotation)
        return self.rooms[name]

    def make_bridge_top(self, name, x=23.5, y=5.5, rotation=0):
        offset = len(self.rooms) * 5.4
        parent = Entity(x=x-offset, y=y, rotation_z=rotation)
        parent.top = Entity(parent=parent, model='quad', color=color.blue, collider="box", x=2.6, scale_x=.2, scale_y=0.8)
        parent.mid = Entity(parent=parent, model='quad', color=color.gray, collider="box", x=0, scale_x=5, scale_y=1)
        parent.bottom = Entity(parent=parent, model='quad', color=color.blue, collider="box", x=-2.6, scale_x=.2, scale_y=0.8)
        self.rooms[name] = parent
        return parent

    def make_bridge_bottom(self, name, x=31.5, y=-6, rotation=0):
        offset = len(self.rooms) * 5.4
        parent = Entity(x=x-offset, y=y, rotation_z=rotation)
        parent.top = Entity(parent=parent, model='quad', color=color.blue, collider="box", x=2.6, scale_x=.2, scale_y=0.8)
        parent.mid = Entity(parent=parent, model='quad', color=color.gray, collider="box", x=0, scale_x=5, scale_y=1)
        parent.bottom = Entity(parent=parent, model='quad', color=color.blue, collider="box", x=-2.6, scale_x=.2, scale_y=0.8)
        self.rooms[name] = parent
        return parent

    def make_centrifuge(self, name, x=2.2, y=0, rotation=90):
        offset = len(self.rooms) * 5.4
        parent = Entity(x=x-offset, y=y, rotation_z=rotation)
        parent.top = Entity(parent=parent, model='quad', color=color.blue, collider="box", x=5.1, scale_x=.2, scale_y=0.8)
        parent.mid = Entity(parent=parent, model='quad', color=color.light_gray, collider="box", x=0, scale_x=10, scale_y=1)
        parent.bottom = Entity(parent=parent, model='quad', color=color.red, collider="box", x=-5.1, scale_x=.2, scale_y=0.8)
        self.rooms[name] = parent
        return parent

    def make_active(self, name):
        self.active = self.crew[name]
        self.active.active = True
        for c in self.crew.values():
            if c is not self.active:
                c.active = False

    def sound_warning(self, state):

        if self.warning_state == state:
            return

        if state:
            self.siren.play()

            for room in self.rooms.values():
                self.alarms.append(room.mid.blink(color.red, loop=True, duration=.5))
        else:
            self.siren.fade_out(duration=1)
            
            # pause all alarms
            for alarm in self.alarms:
                alarm.pause()
            
            # reset alarms
            self.alarms = []

            # set colour back on mid section
            for room in self.rooms.values():
                room.mid.color = color.light_gray

        self.warning_state = state

    def update(self):

        self.mission_duration += (1.0/60.0) * time.dt
        self.fuel -= 0.1 * time.dt
