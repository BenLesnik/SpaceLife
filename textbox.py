from ursina import *

class Textbox(Entity):
    def __init__(self, text = "Orem Lipsum", parent=None):
        self = Text(text= text, x= 0.05, y=0.48, width = 0.2)#, height = 0.3, wordwrap = 0.7)