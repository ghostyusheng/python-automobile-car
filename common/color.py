class Color:
    """
    priority sequence of the color
    """
    pass

class Blue(Color):
    _name = 'blue'
    hsvMin, hsvMax = (100 ,100, 46), (130, 255, 255)

class Red(Color):
    _name = 'red'
    hsvMin, hsvMax = (160,100, 50), (179, 255, 255)

class Purple(Color):
    _name = 'purple'
    hsvMin, hsvMax = (125,100, 46), (155, 255, 255)

class Green(Color):
    _name = 'green'
    hsvMin, hsvMax = (40,100, 46), (90, 255, 255)

class Yellow(Color):
    _name = 'yellow'
    hsvMin, hsvMax = (15,100, 20), (29, 255, 255)

color_stack = [Green, Purple, Blue, Yellow, Red]
color_sequence = [Red, Yellow, Blue, Purple, Green]
