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

    def on_click(self):
        self.ship.make_active(self.name)

if __name__ == "__main__":

    from ursina import *
    app = Ursina()

    camera.orthographic = True
    camera.fov = 10

    Crew("captain")

    app.run()