# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# classes defines the different classes we have, used in the other files

# registry part is necessary to easily loop over all instances of the object later

# a class that represents a House object
class House():
    _registry = []

    def __init__(self, x, y, maxoutput, cable):
        self._registry.append(self)
        self.x = x
        self.y = y
        self.maxoutput = maxoutput
        self.connected = False
        self.cable = cable

# a class that represents a Battery object
class Battery:
    _registry = []

    def __init__(self, x, y, capacity):
        self._registry.append(self)
        self.x = x
        self.y = y
        self.capacity = capacity
        self.av_cap = capacity
        self.connected_to = []
        self.cables = []

# a class that represents a Cable object
class Cable:
    _registry = []

    def __init__(self, x_coords, y_coords, length):
        self._registry.append(self)
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.length = length