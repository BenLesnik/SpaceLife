from ursina import *


def auto_line_break(str, length = 60):
        rtr = ""
        for int, char in enumerate(str):
            if (int % length == 0):
                rtr += ("\n")           
            rtr += (char)
        return(rtr)


class Textbox(Entity):


    def __init__(self, text = "Lorem Lipsum", parent=None):
        self.text = auto_line_break(text)
        self.disp = Text(auto_line_break(self.text), x= 0.05, y=0.48, width = 0.2, background = True)
        

    def update(self, text = "new text"):
        self.disp.disable()
        self.text = auto_line_break(text)
        self.disp = Text(auto_line_break(self.text), x= 0.05, y=0.48, width = 0.2, background = True)
  
    

if __name__ == '__main__':
    print(auto_line_break("Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum",30))