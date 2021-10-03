from ursina import *

class Equipment(Sprite):

    def __init__(self, name, texture="", ship=None, room=None, post_walk=[], scale_x=0.6, scale_y=0.6, **kwargs):
        super().__init__(texture, scale_x=scale_x, scale_y=scale_y, collider="box", **kwargs)
        self.z = -1
        self.name = name
        
        if ship:
            self.ship = ship
            self.ship.equipment[name] = self

        if room:
            self.room = room
            self.room.equipment[name] = self
            self.parent = room

        self.wear = 0.0
        self.post_walk = post_walk

    def on_click(self):
        self.ship.active.move_to(self, self.post_walk)

if __name__ == "__main__":
    app = Ursina()
    Equipment("test", texture="assets/chair")
    app.run()
