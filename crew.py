from ursina import *
from ursina.prefabs.animation import Animation
from ursina.prefabs.animator import Animator

class Crew(Entity):

    def __init__(self, name, ship=None, active=True, x=0, y=0):
        super().__init__(x=x, y=y, always_on_top=True)
        self.name = name
        self.active = active
        self.ship = ship

        self.collider = SphereCollider(self, center=(0,0,0), radius=.1)

        # health bar states
        self.fatigue = 0.0
        self.hunger = 0.0
        self.mental_state = 1.0
        self.bone_density = 1.0

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

    def inside(self):
        inside = True
        if not self.intersects(ignore=(self.ship.crew.values(), self.ship.equipment.values())):
            inside = False
        return inside

    def step_left(self):
        self.collider.shape.setCenter(-.25, 0, 0)
        if self.inside():
            self.animator.state = "left"
            self.animation.start()
            self.x -= time.dt * 2

    def step_right(self):
        self.collider.shape.setCenter(.25, 0, 0)
        if self.inside():
            self.animator.state = "right"
            self.animation.start()
            self.x += time.dt * 2

    def step_up(self):
        self.collider.shape.setCenter(0, .45, 0)
        if self.inside():
            self.animator.state = "up"
            self.animation.start()
            self.y += time.dt * 2

    def step_down(self):
        self.collider.shape.setCenter(0, -.45, 0)
        if self.inside():
            self.animator.state = "down"
            self.animation.start()
            self.y -= time.dt * 2

    def update(self):

        if self.active:
            if held_keys["left arrow"]:
                self.step_left()
            elif held_keys["right arrow"]:
                self.step_right()
            if held_keys["up arrow"]:
                self.step_up()
            elif held_keys["down arrow"]:
                self.step_down()
            else:
                self.animation.pause()


if __name__ == "__main__":

    from ursina import *
    app = Ursina()

    camera.orthographic = True
    camera.fov = 10

    Crew("captain")

    app.run()