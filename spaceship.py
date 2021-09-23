from ursina import color

from crew import Crew
from equipment import Equipment

class Spaceship(object):

    def __init__(self):
        self.active = None
        self.crew = {}
        self.equipment = {}

    def make_active(self, name):
        self.active = self.crew[name]

    def add_crew(self, name, col=color.random_color(), x=0, y=0):
        self.crew[name] = Crew(name, col=col, x=x, y=y)

    def add_equipment(self, name, col=color.gray, x=0, y=0):
        self.equipment[name] = Equipment(name, col=col, x=x, y=y)