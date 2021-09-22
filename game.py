from ursina import *

class Spaceship(object):

    def __init__(self):
        self.active_crewmember = None
        self.crew = {}
        self.equipment = {}

    def add_crew(self, name, col=color.random_color(), x=0, y=0):
        self.crew[name] = Entity(model='sphere',
                                 color=col,
                                 collider='box',
                                 x=x, y=y, z=0,
                                 scale=0.3)

    def set_active_crewmember(self, name):
        self.active_crewmember = self.crew[name]

    def active_crewmember(self):
        return self.active_crewmember

    def add_equipment(self, name):
        self.equipment[name] = Entity(model='cube',
                                      color = color.gray,
                                      collider = 'box',
                                      scale=0.5)

app = Ursina()

ares = Spaceship()

ares.add_crew("captain", color.red, x=4, y=1)
ares.add_crew("doctor", color.green, x=4)
ares.add_crew("engineer", x=4, y=-1)
ares.set_active_crewmember("captain")

ares.add_equipment("engine")

def input(key):
    global ares

    if key == '1':
        ares.set_active_crewmember("captain")
    elif key == '2':
        ares.set_active_crewmember("doctor")
    elif key == '3':
        ares.set_active_crewmember("engineer")

    for obj in ares.equipment.values():
        assigned = False
        for crew in ares.crew.values():
            if crew.intersects(obj).hit:
                obj.color = crew.color
                assigned = True
        
        if not assigned:
            obj.color = color.gray

def update():
    global ares
    ares.active_crewmember.x += held_keys['right arrow'] * time.dt * 2
    ares.active_crewmember.x -= held_keys['left arrow'] * time.dt * 2
    ares.active_crewmember.y += held_keys['up arrow'] * time.dt * 2
    ares.active_crewmember.y -= held_keys['down arrow'] * time.dt * 2

app.run()
