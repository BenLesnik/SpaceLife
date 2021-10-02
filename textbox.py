from ursina import *


def auto_line_break(str, length = 20):
        rtr = ""
        for int, char in enumerate(str):
            if (int % length == 0):
                rtr += ("\n")           
            rtr += (char)
        return(rtr)


class Textbox(Entity):
    def __init__(self, text = "Lorem Lipsum", parent=None):
        self = Text(text= auto_line_break(text,30), x= 0.05, y=0.48, width = 0.2)#, height = 0.3, wordwrap = 0.7)



if __name__ == '__main__':
    print("kjhkjhk")
    print(auto_line_break("Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum",30))