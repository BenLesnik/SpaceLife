from ursina import *
from ursina.prefabs.animation import Animation
from ursina.prefabs.animator import Animator
from ursina.prefabs.health_bar import HealthBar

class Crew(Entity):

    def __init__(self, name, ship=None, active=True, x=0, y=0):
        super().__init__(x=x, y=y, always_on_top=True)
        self.name = name
        self.active = active
        self.ship = ship

        self.collider = SphereCollider(self, radius=.3)

        # health bar states
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

    def move_to(self, position, post_walk=[]):

        s = Sequence()
        s.append(Func(self.start_all_animations))

        # move in y from current position to centre line
        if self.world_position.y > 0:
            s.append(Func(setattr, self.animator, "state", "down"))
        elif self.world_position.y < 0:
            s.append(Func(setattr, self.animator, "state", "up"))

        s.append(Func(self.animate_y, 0.0, duration=self.world_position.y, curve=curve.linear))
        s.append(self.world_position.y)

        # move x direction along ship
        distance_along = self.world_position.x - position.x
        
        if distance_along > 0:
            s.append(Func(setattr, self.animator, "state", "left"))
        elif distance_along < 0:
            s.append(Func(setattr, self.animator, "state", "right"))

        distance_along = abs(distance_along) * 0.2 # make it a bit faster
        s.append(Func(self.animate_x, position.x, duration=distance_along, curve=curve.linear))
        s.append(distance_along)

        # move in y to position
        if position.y > 0:
            s.append(Func(setattr, self.animator, "state", "up"))
        elif position.y < 0:
            s.append(Func(setattr, self.animator, "state", "down"))

        s.append(Func(self.animate_y, position.y, duration=position.y, curve=curve.linear))
        s.append(position.y)

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