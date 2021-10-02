import argparse
from ursina import *
from ursina.prefabs.health_bar import HealthBar

from util import updateHealthBarColor

parser = argparse.ArgumentParser(description='Spacelife - a NASA SpaceApps Challenge 2021')

parser.add_argument('-w', dest='warning_time', type=float, default=0.5, help='Set the alarm time before the flare event occurs')
parser.add_argument('-v', dest='volume', type=float, default=1.0, help='Set the warning siren volume')

parser.add_argument('-ft', dest='flare_start', type=float, default=2.5, help='Set the time the flare event occurs')
parser.add_argument('-fd', dest='flare_duration', type=float, default=0.5, help='Set how long the flare event occurs')
parser.add_argument('-nf', dest='flare', action='store_false', help='Disable the Solar flare event')

parser.add_argument('-t', dest='time', type=float, default=1.0, help='Set the current mission duration time')
args = parser.parse_args()

FLARE_WARNING_START = args.flare_start - args.warning_time
FLARE_START = args.flare_start
FLARE_END = args.flare_start + args.flare_duration

app = Ursina()

from spaceship import Spaceship

camera.orthographic = True
camera.fov = 10

# texture from https://www.flickr.com/photos/webtreatsetc/5436446554/in/photostream/
texture_offset = 0.0
background = Entity(model="quad", texture="assets/space2", x=-15, scale=100)
background.texture_scale = (10, 10) # Change the camera fov to debug tiling

ares = Spaceship()
ares.siren.volume = args.volume
ares.mission_duration = args.time

engine = ares.make_room("engine")
engine.add_crew("engineer")

store_room = ares.make_room("store_room")

safe_room = ares.make_room("safe_room")
safe_room.add_chair("chair1", x=1, y=0.6)
safe_room.add_chair("chair2", x=-1, y=0.6)
safe_room.add_chair("chair3", x=1, y=-0.6)
safe_room.add_chair("chair4", x=-1, y=-0.6)

centrifuge = ares.make_room("centrifuge", rotation=90, length=10)

med_bay = ares.make_room("med_bay")
med_bay.add_crew("doctor", y=0.5)
med_bay.add_bed("bed1", x=-1, y=0.5)
med_bay.add_bed("bed2", x=1, y=0.5)

greenhouse = ares.make_room("greenhouse")
greenhouse.add_crew("biologist", y=-0.5)

cafeteria = ares.make_room("cafeteria")

bridge_top = ares.make_room("bridge_top", y=1.9, parent=cafeteria)
bridge_top.add_crew("captain",  y=0.5)

bridge_bottom = ares.make_room("bridge_bottom", y=-1.9, parent=cafeteria)
bridge_bottom.add_crew("pilot",  y=0.5)

sleeping = ares.make_room("sleeping", y=6, parent=centrifuge)
gym = ares.make_room("gym", y=-6, parent=centrifuge)

# setup crew
ares.crew["captain"].stress = 8
ares.crew["captain"].tiredness = 4

ares.crew["doctor"].stress = 6
ares.crew["doctor"].tiredness = 8

ares.crew["engineer"].stress = 3
ares.crew["engineer"].tiredness = 3

ares.crew["biologist"].stress = 2
ares.crew["biologist"].tiredness = 2

ares.make_active("captain")

# Ship statistics
Text(text="ARES", x=-0.75, y=0.45)

Text(text="Oxygen", x=-0.85, y=0.40)
oxygen = HealthBar(x=-0.7, y=0.40)
oxygen.tooltip = Tooltip('oxygen')

Text(text="Fuel", x=-0.85, y=0.35)
fuel = HealthBar(x=-0.7, y=0.35)
fuel.tooltip = Tooltip('fuel')

Text(text="Food", x=-0.85, y=0.30)
food = HealthBar(x=-0.7, y=0.30)
food.tooltip = Tooltip('food')

Text(text="Damage", x=-0.85, y=0.25)
damage = HealthBar(x=-0.7, y=0.25)
damage.tooltip = Tooltip('damage')

Text(text="Radiation", x=-0.85, y=0.20)
ship_radiation = HealthBar(x=-0.7, y=0.20)
ship_radiation.tooltip = Tooltip('radiation')

# Crew statistics
crew_label = Text(text="CAPTAIN", x=0.35, y=0.45)

Text(text="Stress", x=0.15, y=0.40)
stress = HealthBar(x=0.35, y=0.40)
stress.tooltip = Tooltip('stress')

Text(text="Tiredness", x=0.15, y=0.35)
tiredness = HealthBar(x=0.35, y=0.35)
tiredness.tooltip = Tooltip('tiredness')

Text(text="Bone Density", x=0.15, y=0.30)
bone_density = HealthBar(x=0.35, y=0.30)
bone_density.tooltip = Tooltip('bone density')

# Text(text="Sanity", x=0.15, y=0.25)
# sanity = HealthBar(x=0.35, y=0.25, bar_color=color.red, roundness=.5)
# sanity.tooltip = Tooltip('sanity')
# sanity.value=15

Text(text="Radiation", x=0.15, y=0.25)
radiation = HealthBar(x=0.35, y=0.25)
radiation.tooltip = Tooltip('radiation')

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
        
        # flare warning
        if ares.mission_duration > FLARE_WARNING_START and ares.mission_duration < FLARE_START:
            ares.sound_warning(True)
        else:
            ares.sound_warning(False)

        if ares.mission_duration > FLARE_START and ares.mission_duration < FLARE_END:
            if not ares.shaking:
                ares.shaking = ares.shake(duration=FLARE_END-FLARE_START)
            ares.radiation = 93.0
        else:
            ares.radiation = 11.0

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
    oxygen_int = int(ares.oxygen)
    if oxygen.value != oxygen_int:
        oxygen.value = oxygen_int
    updateHealthBarColor(oxygen, good_level = 70.0, bad_level = 30.0)

    fuel_int = int(ares.fuel)
    if fuel.value != fuel_int:
        fuel.value = fuel_int
    updateHealthBarColor(fuel, good_level = 70.0, bad_level = 30.0)

    food_int = int(ares.food)
    if food.value != food_int:
        food.value = food_int
    updateHealthBarColor(food, good_level = 70.0, bad_level = 30.0)

    damage_int = int(ares.damage)
    if damage.value != damage_int:
        damage.value = damage_int
    updateHealthBarColor(damage, good_level = 30.0, bad_level = 70.0, high="bad")

    ship_radiation_int = int(ares.radiation)
    if ship_radiation.value != ship_radiation_int:
        ship_radiation.value = ship_radiation_int
    updateHealthBarColor(ship_radiation, good_level = 12.0, bad_level = 30.0, high="bad")

    # update character detail health bars
    if crew_label.text != ares.active.name.upper():
        crew_label.text = ares.active.name.upper()

    if stress.value != ares.active.stress:
        stress.value = ares.active.stress
    updateHealthBarColor(stress, good_level = 10.0, bad_level = 40.0, high="bad")
    
    if tiredness.value != int(ares.active.tiredness):
        tiredness.value = int(ares.active.tiredness)
    updateHealthBarColor(tiredness, good_level = 10.0, bad_level = 40.0, high="bad")

    if bone_density.value != int(ares.active.bone_density):
        bone_density.value = int(ares.active.bone_density)
    updateHealthBarColor(bone_density, good_level = 10.0, bad_level = 40.0)

    if radiation.value != int(ares.active.radiation):
        radiation.value = int(ares.active.radiation)
    updateHealthBarColor(radiation, good_level = 10.0, bad_level = 40.0, high="bad")

app.run()

