from ursina import Sprite

class Equipment(Sprite):

    def __init__(self, name, x=0, y=0):
        super().__init__("brick",
                        collider='box',
                        x=x, y=y, z=0)
        self.name = name
        self.wear = 0.0
