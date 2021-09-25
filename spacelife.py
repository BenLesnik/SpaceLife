from ursina import *
from ursina.prefabs.health_bar import HealthBar
app = Ursina()

from spaceship import Spaceship

camera.orthographic = True
camera.fov = 10

ares = Spaceship()

ares.add_crew("captain")

ares.crew["captain"].stress = 80
ares.crew["captain"].tiredness = 90
ares.crew["captain"].bone_density = 90

ares.add_crew("doctor", y=0.5)

ares.crew["doctor"].stress = 20
ares.crew["doctor"].tiredness = 10
ares.crew["doctor"].bone_density = 100

ares.add_crew("engineer", y=-0.5)

ares.crew["engineer"].stress = 30
ares.crew["engineer"].tiredness = 50
ares.crew["engineer"].bone_density = 60

ares.make_active("captain")

ares.make_room("bridge")
ares.make_room("science")
ares.make_room("safe room")
ares.make_room("engine room")

ares.add_bed("bed1", x=-10, y=0.5)
ares.add_bed("bed2", x=-12, y=0.5)

# Ship statistics
Text(text="Oxygen", x=-0.85, y=0.45)
oxygen = HealthBar(x=-0.75, y=0.45, bar_color=color.azure, roundness=.5)
oxygen.tooltip = Tooltip('oxygen')
oxygen.value=90

Text(text="Fuel", x=-0.85, y=0.4)
fuel = HealthBar(x=-0.75, y=0.4, bar_color=color.red, roundness=.5)
fuel.tooltip = Tooltip('fuel')
fuel.value=10


# Crew statistics
crew_label = Text(text="CAPTAIN", x=0.35, y=0.45)

Text(text="Stress", x=0.15, y=0.40)
stress = HealthBar(x=0.35, y=0.40, bar_color=color.yellow, roundness=.5)
stress.tooltip = Tooltip('stress')
stress.value=50

Text(text="Tiredness", x=0.15, y=0.35)
tiredness = HealthBar(x=0.35, y=0.35, bar_color=color.red, roundness=.5)
tiredness.tooltip = Tooltip('tiredness')
tiredness.value=80

Text(text="Bone Density", x=0.15, y=0.30)
bone_density = HealthBar(x=0.35, y=0.30, bar_color=color.blue, roundness=.5)
bone_density.tooltip = Tooltip('bone density')
bone_density.value=80


# Travel duration
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

def update():

    # camera movement
    if held_keys["left arrow"] or held_keys["a"]:
        camera.x -= time.dt * 4
    elif held_keys["right arrow"] or held_keys["d"]:
        camera.x += time.dt * 4
    if held_keys["up arrow"] or held_keys["w"]:
        camera.y += time.dt * 4
    elif held_keys["down arrow"] or held_keys["s"]:
        camera.y -= time.dt * 4

    # update character detail health bars
    if crew_label.text != ares.active.name.upper():
        crew_label.text = ares.active.name.upper()

    if stress.value != ares.active.stress:
        stress.value = ares.active.stress
    
    if tiredness.value != ares.active.tiredness:
        tiredness.value = ares.active.tiredness

    if bone_density.value != ares.active.bone_density:
        bone_density.value = ares.active.bone_density

app.run()
