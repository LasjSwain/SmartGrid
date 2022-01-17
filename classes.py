# GENERAL CLASS COMMENT:
# registry part is necessary to easily loop over all instances of the object later

# a class that represents a House object
class House(object):
    _registry = []

    def __init__(self, x, y, maxoutput):
        self._registry.append(self)
        self.x = x
        self.y = y
        self.maxoutput = maxoutput
        self.connected = False

# a class that represents a Battery object
class Battery:
    _registry = []

    def __init__(self, x, y, capacity):
        self._registry.append(self)
        self.x = x
        self.y = y
        self.capacity = capacity
        self.av_cap = capacity

# a class that represents a Cable object
# havent done anything with this yet
class Cable:
    _registry = []

    def __init__(self, x_coords, y_coords, length):
        self._registry.append(self)
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.length = length