from ursina import time
from ursina.prefabs.animation import Animation
from ursina.prefabs.animator import Animator

class Crew(Animator):

    def __init__(self, name, x=0, y=0):
        super().__init__(
            animations = {
            "left"  : Animation("assets/left", collider="box"),
            "right" : Animation("assets/right", collider="box"),
            "up"    : Animation("assets/up", collider="box"),
            "down"  : Animation("assets/down", collider="box"),
            })

        self.name = name

        # health bar states
        self.fatigue = 0.0
        self.hunger = 0.0
        self.mental_state = 1.0
        self.bone_density = 1.0

        # positions
        self.idle()
        self.sprite.x = x
        self.sprite.y = y
        self.update_sprites()

    @property
    def sprite(self):
        return self.animations[self.state]

    def update_sprites(self):
        """Update the positions of all the Animation Sprites
        so they stay on top of each other"""
        for state, anim in self.animations.items():
            if state != self.state:
                anim.x = self.sprite.x
                anim.y = self.sprite.y

    def idle(self):
        self.sprite.pause()

    def step_left(self):
        self.state = "left"
        self.sprite.resume()
        self.sprite.x -= time.dt * 2
        self.update_sprites()

    def step_right(self):
        self.state = "right"
        self.sprite.resume()
        self.sprite.x += time.dt * 2
        self.update_sprites()

    def step_up(self):
        self.state = "up"
        self.sprite.resume()
        self.sprite.y += time.dt * 2
        self.update_sprites()

    def step_down(self):
        self.state = "down"
        self.sprite.resume()
        self.sprite.y -= time.dt * 2
        self.update_sprites()

if __name__ == "__main__":

    from ursina import *
    app = Ursina()

    camera.orthographic = True
    camera.fov = 10

    bob = Crew("bob")

    def update():

        if held_keys["left arrow"]:
            bob.step_left()
        elif held_keys["right arrow"]:
            bob.step_right()
        if held_keys["up arrow"]:
            bob.step_up()
        elif held_keys["down arrow"]:
            bob.step_down()
        else:
            bob.idle()

    app.run()