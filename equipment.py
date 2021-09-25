from ursina import *

class Equipment(Sprite):

    def __init__(self, name, ship=None, x=0, y=0):
        super().__init__("brick",
                        collider="box",
                        x=x, y=y, z=-1)
        self.name = name
        self.ship = ship
        self.wear = 0.0

    def on_click(self):
        self.ship.active.animate_x(self.world_x, duration=1, curve=curve.linear)
        invoke(setattr, self.ship.active, "tiredness", 0.0, delay=2.5)

class Bed(Equipment):

    def __init__(self, name, ship=None, x=0, y=0):

        super().__init__(name, ship=ship, x=x, y=y)
        self.texture = "bed"
        self.scale = 1