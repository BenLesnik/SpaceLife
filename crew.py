from ursina import *
from ursina.prefabs.animation import Animation
from ursina.prefabs.animator import Animator
from ursina.prefabs.health_bar import HealthBar

class Crew(Entity):

    def __init__(self, name, ship=None, room=None, active=True, x=0, y=0):
        super().__init__(x=x, y=y, always_on_top=True, collider="box")
        self.z = -2
        self.name = name
        self.active = active
        self.ship = ship
        self.room = room

        # add to ship
        if self.ship:
            ship.crew[name] = self

        if self.room:
            room.crew[name] = self
            self.parent = room

        # health bar states
        self.speed = 2.0
        self.stress = 0.0
        self.tiredness = 0.0
        self.bone_density = 1.0

        overall_health = HealthBar(x=-0.2, y=0.27, bar_color=color.green, roundness=.5, scale_x=0.5, scale_y=0.1, parent=self)
        overall_health.show_text = False
        overall_health.value = 80

        self.animator = Animator(   animations = {
                                    "left"  : Animation("assets/left", parent=self),
                                    "right" : Animation("assets/right", parent=self),
                                    "up"    : Animation("assets/up", parent=self),
                                    "down"  : Animation("assets/down", parent=self),
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

    def update(self):

        self.tiredness += 0.1 * time.dt

    def move_to(self, equipment, post_walk=[]):

        # change space to the same room as the equipment
        if self.parent != equipment.room:
            wp = self.world_position
            self.parent = equipment.room
            self.world_position = wp

        s = Sequence()
        s.append(Func(self.start_all_animations))

        # move in y from current position to centre line
        distance_centre = -self.position.y
        distance_along = equipment.position.x - self.position.x
        distance_across = equipment.position.y

        duration = abs(distance_centre) / self.speed

        if duration != 0.0:
            if distance_centre < 0:
                s.append(Func(setattr, self.animator, "state", "down"))
            elif distance_centre > 0:
                s.append(Func(setattr, self.animator, "state", "up"))

            s.append(Func(self.animate_y, 0.0, duration=duration, curve=curve.linear))
            s.append(duration)

        # move x direction along ship
        # note that animate_x moves to this position in local space - it is not a distance
        duration = abs(distance_along) / self.speed
        
        if duration != 0.0:
            if distance_along < 0:
                s.append(Func(setattr, self.animator, "state", "left"))
            elif distance_along > 0:
                s.append(Func(setattr, self.animator, "state", "right"))

            s.append(Func(self.animate_x, equipment.position.x, duration=duration, curve=curve.linear))
            s.append(duration)

        # move in y to position
        # note that animate_y moves to this position in local space - it is not a distance
        duration = abs(distance_across) / self.speed

        if duration != 0.0:
            if distance_across > 0:
                s.append(Func(setattr, self.animator, "state", "up"))
            elif distance_across < 0:
                s.append(Func(setattr, self.animator, "state", "down"))

            s.append(Func(self.animate_y, equipment.position.y, duration=duration, curve=curve.linear))
            s.append(duration)

        s.append(Func(setattr, self.animator, "state", "left"))
        s.append(Func(self.pause_all_animations))

        for pw in post_walk:
            s.append(pw)

        s.start()

if __name__ == "__main__":

    from ursina import *
    app = Ursina()

    camera.orthographic = True
    camera.fov = 10

    Crew("captain")

    app.run()