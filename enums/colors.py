from enum import Enum

class Color(Enum):
    R = ('r', 'red')
    G = ('g', 'green')
    B = ('b', 'blue')
    GRAY = ('black', 'gray')

    def brush(self):

        return self.value[0]

    def name(self):
        return self.value[1]