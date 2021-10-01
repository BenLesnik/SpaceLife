from ursina import *

def updateHealthBarColor(hb, good_level = 95.0, bad_level = 90.0, high="good"):

    bad = color.red
    moderate = color.yellow.tint(-.25)
    good = color.lime.tint(-.25)

    _value = hb.value
    _color = hb.bar.color

    if high == "bad":
        if _value <= good_level:
            if _color != good:
                hb.bar.color = good
        elif _value >= bad_level:
            if _color != bad:
                hb.bar.color = bad
        else:
            if _color != moderate:
                hb.bar.color = moderate
    else:
        if _value >= good_level:
            if _color != good:
                hb.bar.color = good
        elif _value <= bad_level:
            if _color != bad:
                hb.bar.color = bad
        else:
            if _color != moderate:
                hb.bar.color = moderate
