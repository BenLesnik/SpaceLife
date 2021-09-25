from ursina import *
app = Ursina()

from spaceship import Spaceship

camera.orthographic = True
camera.fov = 10

ares = Spaceship()

ares.add_crew("captain", x=4, y=1)
ares.add_crew("doctor", x=4)
ares.add_crew("engineer", x=4, y=-1)

ares.make_active("captain")

ares.make_room()

ares.add_equipment("engine")

def input(key):
    global ares

    if key == "escape":
        quit()
    if key == "1":
        ares.make_active("captain")
    elif key == "2":
        ares.make_active("doctor")
    elif key == "3":
        ares.make_active("engineer")

    # for obj in ares.equipment.values():

    #     # Update any equipment here - eg causing breakages

    #     for crew in ares.crew.values():

    #         # update crew here - eg health bars
    
    #         if crew.intersects(obj).hit:
    #             obj.color = crew.color
    #             assigned = True

app.run()
