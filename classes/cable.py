# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# the classes directory defines the different classes we have
# they are subsequently used in the other files

# registry part is necessary to easily loop over
# all instances of the object later

# a class that represents a Cable object
class Cable:
    _registry = []

    def __init__(self, x_coords, y_coords, length):
        self._registry.append(self)
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.length = length