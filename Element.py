from enum import Enum

class Element(Enum):
    # Element types
    WATER = "WATER"
    FIRE = "FIRE"
    AIR = "AIR"
    EARTH = "EARTH"

    def __str__(self):
        return self.name

    def get_strength(self):
        if self == Element.WATER:
            return Element.FIRE
        elif self == Element.FIRE:
            return Element.AIR
        elif self == Element.AIR:
            return Element.EARTH
        elif self == Element.EARTH:
            return Element.WATER
    
    def get_weakness(self):
        if self == Element.WATER:
            return Element.EARTH
        elif self == Element.FIRE:
            return Element.WATER
        elif self == Element.AIR:
            return Element.FIRE
        elif self == Element.EARTH:
            return Element.AIR

    @staticmethod
    def get_element_from_string(element):
        element = element.upper() 
        try:
            return Element[element]
        except KeyError:
            return None


    @staticmethod
    def get_element_stats(element):
        if element == Element.WATER:
            return 10, 9, 8, 7
        elif element == Element.FIRE:
            return 8, 10, 7, 9
        elif element == Element.AIR:
            return 7, 8, 9, 10
        elif element == Element.EARTH:
            return 9, 7, 10, 8