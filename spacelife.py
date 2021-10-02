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

window.title = 'Spacelife'                # The window title
window.borderless = False                 # Show a border
window.fullscreen = False                 # Go Fullscreen
window.exit_button.visible = False        # Show close button  (not needed with a border managed by the window manager)

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
engine.add_motor("motor", x=-1.5)
engine.add_engine("nozzle", x=-4.5, y=-0.1)

store_room = ares.make_room("store_room")
store_room.add_box("box1", x=-1, y=-0.3)
store_room.add_box("box2", x=-1.5, y=-0.3)
store_room.add_crew("electrician")

safe_room = ares.make_room("safe_room")
safe_room.add_chair("chair1", x=0.5, y=0.5)
safe_room.add_chair("chair2", x=1.5, y=0.5)
safe_room.add_chair("chair3", x=-0.5, y=0.5)
safe_room.add_chair("chair4", x=-1.5, y=0.5)
safe_room.add_chair("chair5", x=0.5, y=-0.3)
safe_room.add_chair("chair6", x=1.5, y=-0.3)
safe_room.add_chair("chair7", x=-0.5, y=-0.3)
safe_room.add_chair("chair8", x=-1.5, y=-0.3)

centrifuge = ares.make_room("centrifuge", rotation=90, length=10)

med_bay = ares.make_room("med_bay")
med_bay.add_crew("doctor", y=0.5)
med_bay.add_medicalbed("bed1", x=-1, y=0.5)
med_bay.add_medicalbed("bed2", x=1, y=0.5)
med_bay.add_medicalbed("bed3", x=-1, y=-0.3)
med_bay.add_medicalbed("bed4", x=1, y=-0.3)

greenhouse = ares.make_room("greenhouse")
greenhouse.add_crew("biologist", y=-0.5)
greenhouse.add_plant("plant1", x=1, y=-0.3)
greenhouse.add_plant("plant2", x=1.5, y=-0.3)

cafeteria = ares.make_room("cafeteria")
cafeteria.add_sofa("sofa1", x=1.5)
cafeteria.add_table("table1")
cafeteria.add_stool("stool1", x=-0.5, y=0.2)
cafeteria.add_stool("stool2", x=0.5, y=-0.2)
cafeteria.add_stool("stool3", x=0.5, y=0.2)
cafeteria.add_stool("stool4", x=-0.5, y=-0.2)

bridge_top = ares.make_room("bridge_top", y=1.7, parent=cafeteria)
bridge_top.add_chair("commanders_chair")
bridge_top.add_crew("commander")

bridge_bottom = ares.make_room("bridge_bottom", y=-1.7, parent=cafeteria)
bridge_bottom.add_chair("pilot_chair")
bridge_bottom.add_crew("pilot")

sleeping = ares.make_room("sleeping", y=6, parent=centrifuge)
sleeping.add_bed("bed1", x=-1.5, y=0.5)
sleeping.add_bed("bed2", x=0, y=0.5)
sleeping.add_bed("bed3", x=1.5, y=0.5)

gym = ares.make_room("gym", y=-6, parent=centrifuge)
gym.add_treadmill("treadmill1", x=1, y=0)
gym.add_treadmill("treadmill2", x=0, y=0)
gym.add_treadmill("treadmill3", x=-1, y=0)

# setup crew
ares.crew["commander"].stress = 8
ares.crew["commander"].fatigue = 4

ares.crew["doctor"].stress = 6
ares.crew["doctor"].fatigue = 8

ares.crew["engineer"].stress = 3
ares.crew["engineer"].fatigue = 3 

ares.crew["biologist"].stress = 2
ares.crew["biologist"].fatigue = 2

ares.make_active("commander")

# Text setup for statistics
Text.default_resolution = 768 * Text.size

stats_ship_x = -0.85
stats_crew_x = -0.45
stats_x_space = 0.17
stats_y_space = 0.03
stats_y_top = 0.44
stats_round = 0

####################################
# InfoBox

intro = """
Welcome to the Ares - Space Apps Challenge 2021

Your job to to keep the crew alive and healthy on their 28 week 
mission to Mars.

Click on a health bar to get more information.
"""

# Ship Info

ship_oxygen_info = """
Oxygen is vital for the crew to breath, but
as there is no oxygen in space, the crew need
to bring it with them.
"""
ship_fuel_info = """
Fuel is needed to leave orbit around the Earth
and for decellerating once the ship arrives at
Mars to put it into orbit.
"""
ship_food_info = """
The crew need to bring all of the food with them
except what they can grow in the greenhouse.

Click on a plant in the greenhouse to start
harvesting vegetables they have grown (food will increase).
"""
ship_damage_info = """
The ship can be damaged by micrometeorites and 
from gamma radiation as it will be travelling outside the
Earth's protective magnetosphere.
"""
ship_radiation_info = """
There are many sources of radiation in space, such as
gamma rays and solar flare events.

The ship has a warning alarm to inform the crew of incoming
dangerous solar flares, but it can only give them a few 
minutes warning.
"""
ship_mission_duration_info = """
This shows the duration of the mission in weeks.
"""

# Crew Info

crew_stress_info = """
 Space is a dangerous environment and travelling through it
can be a stressful experience.

To reduce stress make sure your crew regularly eat and relax
in the cafeteria.
"""
crew_fatigue_info = """
Earth and Mars are a long distance apart. Make sure that 
the crew is well rested during the long journey.

Send a crew member to bed in the sleeping quarters to reduce
their fatigue.
"""
crew_bone_density_info = """"
The zero-G environment of deep space can cause bone
and muscle wastage.

To compensate make sure that your crew members exercise
regularly in the gym.

But do not leave them too long or they will get fatigued!
"""
crew_mood_info = """

"""
crew_radiation_info = """
During a solar flare the crew needs to shelter in the
Safe Room to avoid high radiation exposure.

They can reduce their exposure by visiting the medical bay
for anti-radiation drugs.
"""

info_box = Text(intro, x= 0.05, y=0.48, background=True)

####################################
# Travel duration

timeline = HealthBar(x=-0.85, y=0.48, scale_x=0.72, scale_y=.025, bar_color=color.lime.tint(-.25), roundness=0, max_value=28)
timeline.value=1


#############################
# Ship statistics

Text(text="SHIP: ARES", x = stats_ship_x, y=stats_y_top,background=False)

Text(text="Oxygen", x= stats_ship_x, y=stats_y_top - stats_y_space, background=False)
ship_oxygen = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_oxygen.tooltip = Tooltip('oxygen')
ship_oxygen.on_click = Func(setattr, info_box, "text", ship_oxygen_info)

Text(text="Fuel", x= stats_ship_x , y=stats_y_top - 2*stats_y_space,background=False)
ship_fuel = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - 2*stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_fuel.tooltip = Tooltip('fuel')
ship_fuel.on_click = Func(setattr, info_box, "text", ship_fuel_info)

Text(text="Food", x= stats_ship_x , y=stats_y_top - 3*stats_y_space,background=False)
ship_food = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - 3*stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_food.tooltip = Tooltip('food')
ship_food.on_click = Func(setattr, info_box, "text", ship_food_info)

Text(text="Damage",  x= stats_ship_x , y=stats_y_top - 4*stats_y_space,background=False)
ship_damage = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - 4*stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_damage.tooltip = Tooltip('damage')
ship_damage.on_click = Func(setattr, info_box, "text", ship_damage_info)

Text(text="Radiation",  x= stats_ship_x , y=stats_y_top - 5*stats_y_space,background=False)
ship_radiation = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - 5*stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_radiation.tooltip = Tooltip('radiation')
ship_radiation.on_click = Func(setattr, info_box, "text", ship_radiation_info)

######################
# Crew statistics
crew_label = Text(text="CREW: ", x = stats_crew_x, y=stats_y_top,background=False)

Text(text="Stress", x= stats_crew_x, y=stats_y_top - stats_y_space, background=False)
crew_stress = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_stress.tooltip = Tooltip('stress')
crew_stress.on_click = Func(setattr, info_box, "text", crew_stress_info)

Text(text="Fatigue",  x= stats_crew_x, y=stats_y_top - 2*stats_y_space, background=False)
crew_fatigue = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - 2*stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_fatigue.tooltip = Tooltip('fatigue')
crew_fatigue.on_click = Func(setattr, info_box, "text", crew_fatigue_info)

Text(text="Bone Density", x= stats_crew_x, y=stats_y_top - 3*stats_y_space, background=False)
crew_bone_density = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - 3*stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_bone_density.tooltip = Tooltip('bone density')
crew_bone_density.on_click = Func(setattr, info_box, "text", crew_bone_density_info)

Text(text="Mood", x= stats_crew_x, y=stats_y_top - 4*stats_y_space, background=False)
crew_mood = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - 4*stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_mood.tooltip = Tooltip('Mood')
crew_mood.value=15
crew_mood.on_click = Func(setattr, info_box, "text", crew_mood_info)

Text(text="Radiation", x= stats_crew_x, y=stats_y_top - 5 *stats_y_space, background=False)
crew_radiation = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - 5*stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_radiation.tooltip = Tooltip('radiation')
crew_radiation.on_click = Func(setattr, info_box, "text", crew_radiation_info)

# siren warning text
warning_text = """WARNING: SOLAR FLARE
ALL CREW TO SAFE ROOM"""

warning_text = Text(text=warning_text, x=-.3, y=-.3, background=True, scale=2)
warning_text.blink(color.red, loop=True, duration=.5)
warning_text.disable()

def input(key):
    global ares

    if key == "escape":
        quit()
    if key == "1":
        ares.make_active("commander")
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
            ares.sound_warning(True, warning_text)
        else:
            ares.sound_warning(False, warning_text)

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
    ship_oxygen_int = int(ares.oxygen)
    if ship_oxygen.value != ship_oxygen_int:
        ship_oxygen.value = ship_oxygen_int
        updateHealthBarColor(ship_oxygen, good_level = 70.0, bad_level = 30.0)

    ship_fuel_int = int(ares.fuel)
    if ship_fuel.value != ship_fuel_int:
        ship_fuel.value = ship_fuel_int
        updateHealthBarColor(ship_fuel, good_level = 70.0, bad_level = 30.0)

    ship_food_int = int(ares.food)
    if ship_food.value != ship_food_int:
        ship_food.value = ship_food_int
        updateHealthBarColor(ship_food, good_level = 70.0, bad_level = 30.0)

    ship_damage_int = int(ares.damage)
    if ship_damage.value != ship_damage_int:
        ship_damage.value = ship_damage_int
        updateHealthBarColor(ship_damage, good_level = 30.0, bad_level = 70.0, high="bad")

    ship_radiation_int = int(ares.radiation)
    if ship_radiation.value != ship_radiation_int:
        ship_radiation.value = ship_radiation_int
        updateHealthBarColor(ship_radiation, good_level = 12.0, bad_level = 30.0, high="bad")

    # update character detail health bars
    if crew_label.text != f"CREW: {ares.active.name.upper()}":
        crew_label.text = f"CREW: {ares.active.name.upper()}"

    crew_stress_int = int(ares.active.stress)
    if crew_stress.value != crew_stress_int:
        crew_stress.value = crew_stress_int
        updateHealthBarColor(crew_stress, good_level = 10.0, bad_level = 40.0, high="bad")
    
    crew_fatigue_int = int(ares.active.fatigue)
    if crew_fatigue.value != crew_fatigue_int:
        crew_fatigue.value = crew_fatigue_int
        updateHealthBarColor(crew_fatigue, good_level = 10.0, bad_level = 40.0, high="bad")

    crew_bone_density_int = int(ares.active.bone_density)
    if crew_bone_density.value != crew_bone_density_int:
        crew_bone_density.value = crew_bone_density_int
        updateHealthBarColor(crew_bone_density, good_level = 10.0, bad_level = 40.0)

    crew_radiation_int = int(ares.active.radiation)
    if crew_radiation.value != crew_radiation_int:
        crew_radiation.value = crew_radiation_int
        updateHealthBarColor(crew_radiation, good_level = 10.0, bad_level = 40.0, high="bad")

app.run()   

