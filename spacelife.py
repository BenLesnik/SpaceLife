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
ares.make_room("safe room")
ares.make_room("engine room")

ares.add_equipment("engine")

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
Text(text="Stress", x=0.15, y=0.45)
stress = HealthBar(x=0.35, y=0.45, bar_color=color.yellow, roundness=.5)
stress.tooltip = Tooltip('stress')
stress.value=50

Text(text="Tiredness", x=0.15, y=0.40)
tiredness = HealthBar(x=0.35, y=0.4, bar_color=color.red, roundness=.5)
tiredness.tooltip = Tooltip('tiredness')
tiredness.value=80

Text(text="Bone Density", x=0.15, y=0.35)
bone_density = HealthBar(x=0.35, y=0.35, bar_color=color.blue, roundness=.5)
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

app.run()
