from static.constants import PUZZLE_KIT_RED_WIRE, PUZZLE_KIT_BLUE_WIRE
from random import choice

class Wires():
    def __init__(self):
        self.wireToCut = choice([PUZZLE_KIT_RED_WIRE, PUZZLE_KIT_BLUE_WIRE])

    def randomize_wire(self):
        """
        The purpose of this function is to select a random wire that
        the players will have to cut.
        """
        self.wireToCut = choice([PUZZLE_KIT_RED_WIRE, PUZZLE_KIT_BLUE_WIRE])
        return 0

    def check_wire(self, value):
        """
        Checks that the given data matches the correct wire
        """
        return self.wireToCut == value

    def getColor(self):
        """
        Returns what color was chosen
        """
        return self.wireToCut
