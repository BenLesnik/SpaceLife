from ursina import time
from ursina.prefabs.animation import Animation
from ursina.prefabs.animator import Animator

class moveableAnimation(Animation):

    def __init__(self, animator, name, fps=12, loop=True, autoplay=True, frame_times=None, **kwargs):
        super().__init__(name, fps=fps, loop=loop, autoplay=autoplay, frame_times=frame_times, **kwargs)
        self.animator = animator

    def step_left(self):
        self.animator.state = "left"
        self.resume()
        self.x -= time.dt * 2

    def step_right(self):
        self.animator.state = "right"
        self.resume()
        self.x += time.dt * 2

    def step_up(self):
        self.animator.state = "up"
        self.resume()
        self.y += time.dt * 2

    def step_down(self):
        self.animator.state = "down"
        self.resume()
        self.y -= time.dt * 2

    def update(self):

        if held_keys["left arrow"]:
            self.step_left()
        elif held_keys["right arrow"]:
            self.step_right()
        if held_keys["up arrow"]:
            self.step_up()
        elif held_keys["down arrow"]:
            self.step_down()
        else:
            self.pause()

        # update all other animations so they stay on top of each other
        for anim in self.animator.animations.values():
            if anim is not self:
                anim.x = self.x
                anim.y = self.y

class Crew(Animator):

    def __init__(self, name, x=0, y=0):
        super().__init__(
            animations = {
            "left"  : moveableAnimation(self, "assets/left", collider="box"),
            "right" : moveableAnimation(self, "assets/right", collider="box"),
            "up"    : moveableAnimation(self, "assets/up", collider="box"),
            "down"  : moveableAnimation(self, "assets/down", collider="box"),
            })

        self.name = name

        # health bar states
        self.fatigue = 0.0
        self.hunger = 0.0
        self.mental_state = 1.0
        self.bone_density = 1.0

    @property
    def animation(self):
        return self.animations[self.state]

if __name__ == "__main__":

    from ursina import *
    app = Ursina()

    camera.orthographic = True
    camera.fov = 10

    bob = Crew("bob")

    app.run()