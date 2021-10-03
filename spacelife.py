import argparse
from ursina import *
from ursina.prefabs.health_bar import HealthBar

from infoBox import *   #vclean up to make logic followup more easy
from util import updateHealthBarColor

parser = argparse.ArgumentParser(description='Spacelife - a NASA SpaceApps Challenge 2021')

parser.add_argument('-w', dest='warning_time', type=float, default=0.5, help='Set the alarm time before the flare event occurs')
parser.add_argument('-v', dest='volume', type=float, default=1.0, help='Set the warning siren volume')

parser.add_argument('-ft', dest='flare_start', type=float, default=2.5, help='Set the time the flare event occurs')
parser.add_argument('-fd', dest='flare_duration', type=float, default=0.8, help='Set how long the flare event occurs')
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
camera.x = 25# start centered

# texture from https://www.flickr.com/photos/webtreatsetc/5436446554/in/photostream/
texture_offset = 50.0
background = Entity(model="quad", texture="assets/space2", x=+5, scale=100)
background.texture_scale = (10, 10) # Change the camera fov to debug tiling

ares = Spaceship()
ares.siren.volume = args.volume
ares.mission_duration = args.time

engine = ares.make_room("engine", parent= 'spaceship')
engine.add_crew("engineer")
engine.add_motor("motor", x=-1.5)
engine.add_engine("nozzle", x=-4.5, y=-0.1)

store_room = ares.make_room("store_room", x = 5, parent= 'spaceship')
store_room.add_box("box1", x=-1, y=-0.3)
store_room.add_box("box2", x=-1.5, y=-0.3)
store_room.add_crew("electrician")

safe_room = ares.make_room("safe_room", x = 10, parent= 'spaceship')
safe_room.add_chair("chair1", x=0.5, y=0.5)
safe_room.add_chair("chair2", x=1.5, y=0.5)
safe_room.add_chair("chair3", x=-0.5, y=0.5)
safe_room.add_chair("chair4", x=-1.5, y=0.5)
safe_room.add_chair("chair5", x=0.5, y=-0.3)
safe_room.add_chair("chair6", x=1.5, y=-0.3)
safe_room.add_chair("chair7", x=-0.5, y=-0.3)
safe_room.add_chair("chair8", x=-1.5, y=-0.3)

centrifuge = ares.make_room("centrifuge", rotation=90, length=12, x = 13, parent= 'spaceship')

med_bay = ares.make_room("med_bay", x = 16, parent= 'spaceship')
med_bay.add_crew("doctor", y=0.5)
med_bay.add_medicalbed("bed1", x=-1, y=0.5, scale_x=0.3, scale_y=0.3)
med_bay.add_medicalbed("bed2", x=1, y=0.5, scale_x=0.3, scale_y=0.3)
med_bay.add_medicalbed("bed3", x=-1, y=-0.3, scale_x=0.3, scale_y=0.3)
med_bay.add_medicalbed("bed4", x=1, y=-0.3, scale_x=0.3, scale_y=0.3)

greenhouse = ares.make_room("greenhouse", x = 21, parent= 'spaceship')
greenhouse.add_crew("biologist", y=-0.5)
greenhouse.add_plant("plant1", x=1, y=-0.3)
greenhouse.add_plant("plant2", x=1.5, y=-0.3)

cafeteria = ares.make_room("cafeteria", x = 26, parent= 'spaceship')
cafeteria.add_sofa("sofa1", x=1.5)
cafeteria.add_table("table1")
cafeteria.add_stool("stool1", x=-0.5, y=0.2)
cafeteria.add_stool("stool2", x=0.5, y=-0.2)
cafeteria.add_stool("stool3", x=0.5, y=0.2)
cafeteria.add_stool("stool4", x=-0.5, y=-0.2)
cafeteria.add_crew("security")

bridge_top = ares.make_room("bridge_top", x=26, y=1.7, parent= 'spaceship')
bridge_top.add_chair("commanders_chair")
bridge_top.add_crew("commander")
bridge_top.add_crew("radio_operator", y=-0.5)

bridge_bottom = ares.make_room("bridge_bottom", x=26, y=- 1.7, parent= 'spaceship')
bridge_bottom.add_chair("pilot_chair")
bridge_bottom.add_crew("pilot")

sleeping = ares.make_room("sleeping", x = 13, y=7, parent= 'spaceship')
sleeping.add_bed("bed1", x=-1.5, y=0.5)
sleeping.add_bed("bed2", x=0, y=0.5)
sleeping.add_bed("bed3", x=1.5, y=0.5)

gym = ares.make_room("gym", y=-7, x = 13, parent= 'spaceship')
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

ares.crew["engineer"].stress = 2
ares.crew["engineer"].fatigue = 2

ares.crew["electrician"].stress = 2
ares.crew["electrician"].fatigue = 2

ares.crew["security"].stress = 2
ares.crew["security"].fatigue = 2

ares.crew["radio_operator"].stress = 2
ares.crew["radio_operator"].fatigue = 2

ares.make_active("commander")



####################################
# InfoBox

info_box = Text(intro, x= 0.05, y=0.48)#, background=True)


####################################
# # Text setup for statistics
Text.default_resolution = 768 * Text.size

stats_ship_x = -0.85
stats_crew_x = -0.45
stats_x_space = 0.17
stats_y_space = 0.03
stats_y_top = 0.44
stats_round = 0

# Travel duration

timeline = HealthBar(x=-0.85, y=0.48, scale_x=0.72, scale_y=.025, bar_color=color.lime.tint(-.25), roundness=0, max_value=28)
timeline.value=1
timeline.on_mouse_enter = Func(setattr, info_box, "text", intro)
timeline.on_mouse_exit = Func(setattr, info_box, "text", "")

#############################
# Ship statistics

Text(text="SHIP: ARES", x = stats_ship_x, y=stats_y_top,background=False)

Text(text="Oxygen", x= stats_ship_x, y=stats_y_top - stats_y_space, background=False)
ship_oxygen = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_oxygen.bar.color = color.lime.tint(-.25)
ship_oxygen.on_mouse_enter = Func(setattr, info_box, "text", ship_oxygen_info)
ship_oxygen.on_mouse_exit = Func(setattr, info_box, "text", "")

Text(text="Fuel", x= stats_ship_x , y=stats_y_top - 2*stats_y_space,background=False)
ship_fuel = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - 2*stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_fuel.on_mouse_enter = Func(setattr, info_box, "text", ship_fuel_info)
ship_fuel.on_mouse_exit = Func(setattr, info_box, "text", "")

Text(text="Food", x= stats_ship_x , y=stats_y_top - 3*stats_y_space,background=False)
ship_food = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - 3*stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_food.bar.color = color.lime.tint(-.25)
ship_food.on_mouse_enter = Func(setattr, info_box, "text", ship_food_info)
ship_food.on_mouse_exit = Func(setattr, info_box, "text", "")

Text(text="Damage",  x= stats_ship_x , y=stats_y_top - 4*stats_y_space,background=False)
ship_damage = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - 4*stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_damage.on_mouse_enter = Func(setattr, info_box, "text", ship_damage_info)
ship_damage.on_mouse_exit = Func(setattr, info_box, "text", "")

Text(text="Radiation",  x= stats_ship_x , y=stats_y_top - 5*stats_y_space,background=False)
ship_radiation = HealthBar(x=stats_ship_x + stats_x_space, y=stats_y_top - 5*stats_y_space, scale_x = 0.15, roundness=stats_round)
ship_radiation.on_mouse_enter = Func(setattr, info_box, "text", ship_radiation_info)
ship_radiation.on_mouse_exit = Func(setattr, info_box, "text", "")

######################
# Crew statistics
crew_label = Text(text="CREW: ", x = stats_crew_x, y=stats_y_top,background=False)

Text(text="Stress", x= stats_crew_x, y=stats_y_top - stats_y_space, background=False)
crew_stress = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_stress.on_mouse_enter = Func(setattr, info_box, "text", crew_stress_info)
crew_stress.on_mouse_exit = Func(setattr, info_box, "text", "")

Text(text="Fatigue",  x= stats_crew_x, y=stats_y_top - 2*stats_y_space, background=False)
crew_fatigue = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - 2*stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_fatigue.on_mouse_enter = Func(setattr, info_box, "text", crew_fatigue_info)
crew_fatigue.on_mouse_exit = Func(setattr, info_box, "text", "")

Text(text="Bone Density", x= stats_crew_x, y=stats_y_top - 3*stats_y_space, background=False)
crew_bone_density = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - 3*stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_bone_density.on_mouse_enter = Func(setattr, info_box, "text", crew_bone_density_info)
crew_bone_density.on_mouse_exit = Func(setattr, info_box, "text", "")

Text(text="Radiation", x= stats_crew_x, y=stats_y_top - 4 *stats_y_space, background=False)
crew_radiation = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - 4*stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_radiation.on_mouse_enter = Func(setattr, info_box, "text", crew_radiation_info)
crew_radiation.on_mouse_exit = Func(setattr, info_box, "text", "")

Text(text="Overview", x= stats_crew_x, y=stats_y_top - 5*stats_y_space, background=False)
crew_overview = HealthBar(x = stats_crew_x + stats_x_space, y=stats_y_top - 5*stats_y_space, scale_x = 0.15, roundness=stats_round)
crew_overview.on_mouse_enter = Func(setattr, info_box, "text", crew_overview_info)
crew_overview.on_mouse_exit = Func(setattr, info_box, "text", "")

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
    elif key == "5":
        ares.make_active("pilot")
    elif key == "6":
        ares.make_active("electrician")
    elif key == "7":
        ares.make_active("security")
    elif key == "8":
        ares.make_active("radio_operator")
    elif key == "+":
        camera.fov -= 1
    elif key == "-":
        camera.fov += 1
    elif key == "*":
        camera.fov = 10
    elif key == "=":
        camera.fov -= 1
    elif key == "9":
        camera.fov = 10    

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

    # stop camera moving beyond tiled te
    # xture background
    camera.x = clamp(camera.x, -10.0, 27.0)
    camera.y = clamp(camera.y, -11.0, 11.0)

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
        updateHealthBarColor(crew_fatigue, good_level = 20.0, bad_level = 60.0, high="bad")

    crew_bone_density_int = int(ares.active.bone_density)
    if crew_bone_density.value != crew_bone_density_int:
        crew_bone_density.value = crew_bone_density_int
        updateHealthBarColor(crew_bone_density, good_level = 80.0, bad_level = 40.0)

    crew_radiation_int = int(ares.active.radiation)
    if crew_radiation.value != crew_radiation_int:
        crew_radiation.value = crew_radiation_int
        updateHealthBarColor(crew_radiation, good_level = 10.0, bad_level = 40.0, high="bad")

    crew_overview_int = int(ares.active.health)
    if crew_overview.value != crew_overview_int:
        crew_overview.value = crew_overview_int
        updateHealthBarColor(crew_overview, good_level = 80.0, bad_level = 40.0)

app.run()   

