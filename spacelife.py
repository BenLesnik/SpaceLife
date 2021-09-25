from ursina import *
from ursina.prefabs.health_bar import HealthBar
app = Ursina()

from spaceship import Spaceship

camera.orthographic = True
camera.fov = 10

ares = Spaceship()

ares.add_crew("captain")
ares.add_crew("doctor", y=0.5)
ares.add_crew("engineer", y=-0.5)

ares.make_active("captain")

ares.make_room("bridge")
ares.make_room("science")

ares.add_equipment("engine")

timeline = HealthBar(x=-.5, y=-.4, scale_x=1, scale_y=.05, bar_color=color.lime.tint(-.25), roundness=.5, max_value=28)
timeline.value=14

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
