from ursina import *
app = Ursina()

camera.orthographic = True
camera.fov = 10

from spaceship import Spaceship
ares = Spaceship()

# setup spaceship
ares.add_crew("captain", x=4, y=1)
ares.add_crew("doctor", x=4)
ares.add_crew("engineer", x=4, y=-1)
ares.make_active("captain")

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

def update():
    global ares

    if held_keys["left arrow"]:
        ares.active.step_left()
    elif held_keys["right arrow"]:
        ares.active.step_right()
    if held_keys["up arrow"]:
        ares.active.step_up()
    elif held_keys["down arrow"]:
        ares.active.step_down()
    else:
        ares.active.idle()

    # for obj in ares.equipment.values():

    #     # Update any equipment here - eg causing breakages


    #     assigned = False
    #     for crew in ares.crew.values():

    #         # update crew here - eg health bars


    #         if crew.intersects(obj).hit:
    #             obj.color = crew.color
    #             assigned = True
        
    #     if not assigned:
    #         obj.color = color.gray

app.run()
