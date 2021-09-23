from ursina import *
from spaceship import Spaceship

app = Ursina()
ares = Spaceship()

# setup spaceship
ares.add_crew("captain", color.red, x=4, y=1)
ares.add_crew("doctor", color.green, x=4)
ares.add_crew("engineer", x=4, y=-1)
ares.make_active("captain")

ares.add_equipment("engine")

def input(key):
    global ares

    if key == '1':
        ares.make_active("captain")
    elif key == '2':
        ares.make_active("doctor")
    elif key == '3':
        ares.make_active("engineer")

def update():
    global ares

    ares.active.x += held_keys['right arrow'] * time.dt * 2
    ares.active.x -= held_keys['left arrow'] * time.dt * 2
    ares.active.y += held_keys['up arrow'] * time.dt * 2
    ares.active.y -= held_keys['down arrow'] * time.dt * 2

    for obj in ares.equipment.values():

        # Update any equipment here - eg causing breakages


        assigned = False
        for crew in ares.crew.values():

            # update crew here - eg health bars


            if crew.intersects(obj).hit:
                obj.color = crew.color
                assigned = True
        
        if not assigned:
            obj.color = color.gray

app.run()
