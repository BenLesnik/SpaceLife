from ursina import *

class Equipment(Sprite):

    def __init__(self, name, ship=None, x=0, y=0):
        super().__init__("brick",
                        collider="box",
                        x=x, y=y, z=-1)
        self.name = name
        self.ship = ship
        self.wear = 0.0

    def on_click(self, post_walk=[]):
        return self.ship.active.move_to(self.world_position, post_walk)

class Bed(Equipment):

    def __init__(self, name, ship=None, x=0, y=0):

        super().__init__(name, ship=ship, x=x, y=y)
        self.texture = "bed"
        self.scale = 1

    def on_click(self):
        set_tiredness = [Wait(2.5), Func(setattr, self.ship.active, "tiredness", 0.0)]
        super().on_click(post_walk=set_tiredness)

class Chair(Equipment):

    def __init__(self, name, ship=None, x=0, y=0):

        super().__init__(name, ship=ship, x=x, y=y)
        self.texture = "chair"
        self.scale = 1

    def on_click(self):
        set_tiredness = [Wait(2.5), Func(setattr, self.ship.active, "tiredness", 0.0)]
        super().on_click(post_walk=set_tiredness)