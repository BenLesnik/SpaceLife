import argparse
from ursina import *
from ursina.prefabs.health_bar import HealthBar
app = Ursina()

from spaceship import Spaceship

FLARE_WARNING_START = 1.2
FLARE_START = 1.5

parser = argparse.ArgumentParser(description='Spacelife - a NASA SpaceApps Challenge')
parser.add_argument('-nf', dest='flare', action='store_false', help='Disable the Solar flare event')
args = parser.parse_args()

camera.orthographic = True
camera.fov = 10

# texture from https://www.flickr.com/photos/webtreatsetc/5436446554/in/photostream/
texture_offset = 0.0
background = Entity(model="quad", texture="assets/space2", x=-15, scale=100)
background.texture_scale = (10, 10) # Change the camera fov to debug tiling

ares = Spaceship()

engine = ares.make_room("engine")
engine.add_crew("engineer", y=-0.2)

store_room = ares.make_room("store_room")

safe_room = ares.make_room("safe_room")
safe_room.add_chair("chair1", x=1, y=0.6)
safe_room.add_chair("chair2", x=-1, y=0.6)
safe_room.add_chair("chair3", x=1, y=-0.6)
safe_room.add_chair("chair4", x=-1, y=-0.6)

cenrifuge = ares.make_centrifuge("centrifuge")

med_bay = ares.make_room2("med_bay")
med_bay.add_crew("doctor", y=0.5)
med_bay.add_bed("bed1", x=-1, y=0.5)
med_bay.add_bed("bed2", x=1, y=0.5)

greenhouse = ares.make_room2("greenhouse")
greenhouse.add_crew("biologist", y=-0.5)

cafeteria = ares.make_room2("cafeteria")
cafeteria.add_crew("captain",  y=0.3)

bridge_top = ares.make_bridge_top("bridge_top")

bridge_bottom = ares.make_bridge_top("bridge_top")

# setup crew
ares.crew["captain"].stress = 80
ares.crew["captain"].tiredness = 90
ares.crew["captain"].bone_density = 0
ares.crew["captain"].sanity = 15

ares.crew["doctor"].stress = 20
ares.crew["doctor"].tiredness = 10
ares.crew["doctor"].bone_density = 100
ares.crew["doctor"].sanity = 50

ares.crew["engineer"].stress = 30
ares.crew["engineer"].tiredness = 50
ares.crew["engineer"].bone_density = 60
ares.crew["engineer"].sanity = 5

ares.crew["biologist"].stress = 2
ares.crew["biologist"].tiredness = 2
ares.crew["biologist"].bone_density = 100
ares.crew["biologist"].sanity = 60

ares.make_active("captain")

# Ship statistics
Text(text="ARES", x=-0.75, y=0.45)

Text(text="Oxygen", x=-0.85, y=0.40)
oxygen = HealthBar(x=-0.74, y=0.40, bar_color=color.azure, roundness=.5)
oxygen.tooltip = Tooltip('oxygen')
oxygen.value=90

Text(text="Fuel", x=-0.85, y=0.35)
fuel = HealthBar(x=-0.74, y=0.35, bar_color=color.red, roundness=.5)
fuel.tooltip = Tooltip('fuel')
#fuel.value=10

Text(text="Food", x=-0.85, y=0.30)
food = HealthBar(x=-0.74, y=0.30, bar_color=color.green, roundness=.5)
food.tooltip = Tooltip('food')
food.value=70

Text(text="Damage", x=-0.85, y=0.25)
repair = HealthBar(x=-0.74, y=0.25, bar_color=color.blue, roundness=.5)
repair.tooltip = Tooltip('repair')
repair.value=90

# Crew statistics
crew_label = Text(text="CAPTAIN", x=0.35, y=0.45)

Text(text="Stress", x=0.15, y=0.40)
stress = HealthBar(x=0.35, y=0.40, bar_color=color.yellow, roundness=.5)
stress.tooltip = Tooltip('stress')
stress.value=50

Text(text="Tiredness", x=0.15, y=0.35)
tiredness = HealthBar(x=0.35, y=0.35, bar_color=color.pink, roundness=.5)
tiredness.tooltip = Tooltip('tiredness')
tiredness.value=80

Text(text="Bone Density", x=0.15, y=0.30)
bone_density = HealthBar(x=0.35, y=0.30, bar_color=color.blue, roundness=.5)
bone_density.tooltip = Tooltip('bone density')
bone_density.value=80

Text(text="Sanity", x=0.15, y=0.25)
sanity = HealthBar(x=0.35, y=0.25, bar_color=color.red, roundness=.5)
sanity.tooltip = Tooltip('sanity')
sanity.value=15

# Travel duration
timeline = HealthBar(x=-.5, y=-.4, scale_x=1, scale_y=.05, bar_color=color.lime.tint(-.25), roundness=.5, max_value=28)
timeline.value=1

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
    elif key == "4":
        ares.make_active("biologist")

def update():
    global ares

    if args.flare:
        if ares.mission_duration > FLARE_WARNING_START and ares.mission_duration < FLARE_START:
            ares.sound_warning(True)
        else:
            ares.sound_warning(False)

    # scroll background
    global background, texture_offset
    texture_offset += time.dt * 0.02
    background.texture_offset = (texture_offset, 0)

    # camera movement
    if held_keys["left arrow"] or held_keys["a"]:
        camera.x -= time.dt * 4
    elif held_keys["right arrow"] or held_keys["d"]:
        camera.x += time.dt * 4
    if held_keys["up arrow"] or held_keys["w"]:
        camera.y += time.dt * 4
    elif held_keys["down arrow"] or held_keys["s"]:
        camera.y -= time.dt * 4

    # stop camera moving beyond tiled texture background
    camera.x = clamp(camera.x, -30.0, 10.0)
    camera.y = clamp(camera.y, -20.0, 20.0)

    if timeline.value != int(ares.mission_duration):
        timeline.value = int(ares.mission_duration)

    # update ship stats
    fuel_int = int(ares.fuel)
    if fuel.value != fuel_int:
        fuel.value = fuel_int

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

