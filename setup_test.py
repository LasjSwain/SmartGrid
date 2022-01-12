# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper () & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA

class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y

house_1 = House(1, 1)

print(house_1.x)

class Cable_segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def talk(self):
        print("There is a cable segment on (x, y) = ({}, {})".format(self.x, self.y))

small_cable = Cable_segment(69, 69)

small_cable.talk()