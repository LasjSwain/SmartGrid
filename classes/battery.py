# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# the classes directory defines the different classes we have
# they are subsequently used in the other files

# registry part is necessary to easily loop over
# all instances of the object later

# a class that represents a Battery object
class Battery:
    _registry = []

    def __init__(self, id, x, y, capacity):
        self._registry.append(self)
        self.id = id
        self.x = x
        self.y = y
        self.capacity = capacity
        self.av_cap = capacity
        self.connected_to = []
        self.cables = []
