from ursina import Entity, color

class Equipment(Entity):

    def __init__(self, name, col=color.gray, x=0, y=0):
        super().__init__(model='cube',
                        color=col,
                        collider='box',
                        x=x, y=y, z=0,
                        scale=0.3)
        self.name = name
        self.wear = 0.0
