import glob

from ursina import *
from ursina.prefabs.animation import Animation
from ursina.prefabs.animator import Animator
from ursina.prefabs.health_bar import HealthBar
from ursina.collider import BoxCollider

from util import updateHealthBarColor

class Crew(Entity):

    def __init__(self, name, ship=None, room=None, active=True, x=0, y=0):
        super().__init__(x=x, y=y, always_on_top=True)
        self.z = -2
        self.name = name
        self.active = active
        self.ship = ship
        self.room = room

        self.collider = BoxCollider(self, center=Vec3(0,0,0), size=Vec3(2,3,1))

        # add to ship
        if self.ship:
            ship.crew[name] = self

        if self.room:
            room.crew[name] = self
            self.parent = room

        self.speed = 2.0

        # health bar states
        self.stress = 0.0
        self.fatigue = 0.0
        self.bone_density = 100.0
        self.radiation = 0.0
        self.health = 100.0

        self.overall_health = HealthBar(x=-1.3, y=2.1, scale_x=2.5, scale_y=0.5, parent=self)
        self.overall_health.show_text = False

        left_images = "assets/left"
        right_images = "assets/right"
        up_images = "assets/up"
        down_images = "assets/down"

        if glob.glob(f"assets/{name}_left*"):
            self.scale = 0.18
            left_images = f"assets/{name}_left"

        if glob.glob(f"assets/{name}_right*"):
            right_images = f"assets/{name}_right"

        if glob.glob(f"assets/{name}_up*"):
            up_images = f"assets/{name}_up"

        if glob.glob(f"assets/{name}_down*"):
            down_images = f"assets/{name}_down"

        self.animator = Animator(   animations = {
                                    "right" : Animation(right_images, parent=self),
                                    "left"  : Animation(left_images, parent=self),
                                    "up"    : Animation(up_images, parent=self),
                                    "down"  : Animation(down_images, parent=self),
                                }
                            )

        self.animation.pause()

    @property
    def animation(self):
        return self.animator.animations[self.animator.state]

    def start_all_animations(self):
        for anim in self.animator.animations.values():
            anim.start()

    def pause_all_animations(self):
        for anim in self.animator.animations.values():
            anim.pause()

    def on_click(self):
        self.ship.make_active(self.name)

    def calculate_health(self):
        return (self.bone_density + (100.0 - self.stress)  + (100.0 - self.fatigue)  + (100.0 - self.radiation)) * 0.25

    def update(self):
        
        # going to the med bay reduces radiation from radiation pills
        if self.room.name == "med_bay":
            self.radiation -= 0.2 * time.dt

        # the crew get tired over time, unless they are in the sleeping quarters
        # where they can reduce their fatigue
        elif self.room.name == "sleeping":
            self.fatigue -= 0.1 * time.dt

        # the crew can increase their bone density by exercising in the gym
        # but their fatigue will increase faster
        elif self.room.name == "gym":
            self.bone_density += 0.4 *time.dt
            self.fatigue += 0.4 * time.dt

        # crew can relieve stress by relaxing in the cafeteria
        # but the ship food will decrease as they consume food
        elif self.room.name == "cafeteria":
            self.stress -= 0.1 * time.dt
            self.ship.food -= 0.1 * time.dt

        # going in the greenshouse increases the ships food as the crew
        # harvest the vegetables for food
        elif self.room.name == "greenhouse":
            #self.mood += 0.1 * time.dt
            self.ship.food += 0.1 * time.dt

        # Fatigue increases unless crew is sleeping
        if self.room.name != "sleeping":
            self.fatigue += 0.1 * time.dt

        # bone density decreases unless we are exercising
        if self.room.name != "gym":
            self.bone_density -= 0.1 * time.dt

        # crew radiation increases with the ship radiation
        # this means that when there is a solar flare the radiation increases quickly
        # unless they are in the safe room (does not increase) 
        # or getting treated in the med bay (radiation decreases)
        if self.room.name != "safe_room":
            self.radiation += 0.01 * self.ship.radiation * time.dt

        self.health = self.calculate_health()
        if self.overall_health.value != int(self.health):
            self.overall_health.value = int(self.health)

        updateHealthBarColor(self.overall_health, good_level = 80.0, bad_level = 20.0)

    def mv_y2ctr(self, equipment, s):
        distance_centre = self.world_position.y - self.ship.world_position.y
        duration = abs(distance_centre) / self.speed
        if duration != 0.0:
            if distance_centre > 0:
                s.append(Func(setattr, self.animator, "state", "down"))
            elif distance_centre < 0:
                s.append(Func(setattr, self.animator, "state", "up"))
            s.append(Func(self.animate_y, self.position.y - distance_centre, duration=duration, curve=curve.linear))
            s.append(duration)   

    def mv_alongx(self, equipment, s):
        # note that animate_x moves to this position in local space - it is not a distance
        distance_along = equipment.position.x - self.position.x
        duration = abs(distance_along) / self.speed
    
        if duration != 0.0:
            if distance_along < 0:
                s.append(Func(setattr, self.animator, "state", "left"))
            elif distance_along > 0:
                s.append(Func(setattr, self.animator, "state", "right"))
            s.append(Func(self.animate_x, equipment.position.x, duration=duration, curve=curve.linear))
            s.append(duration)
            self.position.x =  equipment.position.x  #######################################

    def mv_alongx_nexus_from(self, equipment, s):
        distance_along = self.ship.equipment["nexus"].get_position(relative_to=self.room).x - self.get_position(relative_to=self.room).x 
        duration = abs(distance_along) / self.speed
        print("####  nexus from   #########")
        print("distance" + str(distance_along))  #######TO FIX
        if duration != 0.0:
            if distance_along < 0:
                s.append(Func(setattr, self.animator, "state", "left"))
            elif distance_along > 0:
                s.append(Func(setattr, self.animator, "state", "right"))
            s.append(Func(self.animate_x, self.ship.equipment["nexus"].position.x, duration=duration, curve=curve.linear))
            s.append(duration)
            self.position.x = self.ship.equipment["nexus"].position.x  #######################################

    def mv_alongx_nexus_to(self , s):
        distance_along = self.ship.equipment["nexus"].position.x - self.position.x 
        duration = abs(distance_along) / self.speed
        print("####  nexus to   #########")
        print("from" + self.room.name)
        print(self.get_position(relative_to=self.room).x)
        print(self.position.x)
        print("to")
        print(self.ship.equipment["nexus"].get_position(relative_to=self.room).x)
        print(self.ship.equipment["nexus"].position.x)
        print("distance" + str(distance_along))  #######TO FIX
        if duration != 0.0:
            if distance_along < 0:
                s.append(Func(setattr, self.animator, "state", "left"))
            elif distance_along > 0:
                s.append(Func(setattr, self.animator, "state", "right"))
            s.append(Func(self.animate_x, self.ship.equipment["nexus"].position.x , duration=duration, curve=curve.linear))
            s.append(duration)
            self.position.x = self.ship.equipment["nexus"].position.x  #######################################
    

    def mv_ctr2y(self, equipment, s):
        # note that animate_y moves to this position in local space - it is not a distance
        distance_across = equipment.world_position.y  - self.ship.world_position.y
        duration = abs(distance_across) / self.speed
        if duration != 0.0:
            if distance_across > 0:
                s.append(Func(setattr, self.animator, "state", "up"))
            elif distance_across < 0:
                s.append(Func(setattr, self.animator, "state", "down"))
            s.append(Func(self.animate_y, equipment.position.y, duration=duration, curve=curve.linear))
            s.append(duration)



 
    def move_to(self, equipment, post_walk=[]):

        pos_old_room = self.position
        print("### main #########")
        print(pos_old_room)
        print("from" + self.room.name)
        print("to" + equipment.room.name)

        # change space to the same room as the equipment
        if self.parent != equipment.room:
            wp = self.world_position
            self.parent = equipment.room
            self.world_position = wp

        s = Sequence()
   
        # if in centirgufe (and out to somehwre else), first move along x to centrifuge
        if (self.room.name == "gym") or (self.room.name == "sleeping"):
            if (equipment.room.name != self.room.name):
                print("CENTRIFUGE")
                self.mv_alongx_nexus_from(equipment, s)
    
        #only if in different room
        # # move in y from current position to centre line
        if self.room != equipment.room:
            self.mv_y2ctr(equipment, s)       #original step 1
     
        if (equipment.room.name == "gym") or (equipment.room.name == "sleeping"): 
            if (equipment.room.name != self.room.name):
                #move along x to centrifuge
                self.mv_alongx_nexus_to(s)
                # move to equipement
                self.mv_ctr2y(equipment, s)
            self.mv_alongx(equipment, s)
        else:
            # move along x to equipment
            self.mv_alongx(equipment, s)     #original step 2
            # move from center to equipment
            self.mv_ctr2y(equipment, s)      #original step 3

        s.append(Func(setattr, self.animator, "state", "right"))
        s.append(Func(self.pause_all_animations))


        for pw in post_walk:
            s.append(pw)

        # set new room
        s.append(Func(setattr, self, "room", equipment.room))

        s.start()

if __name__ == "__main__":

    from ursina import *
    app = Ursina()


    camera.orthographic = True
    camera.fov = 10

    Crew("captain")

    app.run()