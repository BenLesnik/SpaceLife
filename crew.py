from ursina import Entity, color

class Crew(Entity):

    def __init__(self, name, col=color.random_color(), x=0, y=0):
        super().__init__(model='sphere',
                        color=col,
                        collider='box',
                        x=x, y=y, z=0,
                        scale=0.3)
        self.name = name
        self.fatigue = 0.0
        self.hunger = 0.0
        self.mental = 1.0
        self.bones = 1.0
