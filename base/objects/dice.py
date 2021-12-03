import re
from dataclasses import dataclass

from base.constants.constants import DiceIntEnum


@dataclass
class DiceRoll:
    rolls: int
    dice: DiceIntEnum
    addendant: int

    def __str__(self):
        return f'{self.rolls}{self.dice.description}+{self.addendant}'

    def __add__(self, other):
        if not isinstance(other, int):
            raise TypeError('should add only ints to dice rolls')
        return DiceRoll(
            rolls=self.rolls, dice=self.dice, addendant=self.addendant + other
        )

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError('should multiply only by int')
        # 1d6+4 * 2 = 2d6+4.  Addendants don't multiply
        return DiceRoll(
            rolls=self.rolls * other, dice=self.dice, addendant=self.addendant
        )

    def __imul__(self, other):
        if not isinstance(other, int):
            raise TypeError('should multiply only by int')
        return DiceRoll(
            rolls=self.rolls * other, dice=self.dice, addendant=self.addendant
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def roll(self):
        self.dice.roll(self.rolls) + self.addendant

    def treshhold(self, value):
        self.addendant = min(self.addendant, value)
        return self

    @classmethod
    def from_str(cls, string):
        # TODO fix d100 match. now it gets d10.
        parsed_str = re.findall(
            r'([0-9]{1,2})([dkдк](?:[468]|1[02]|20|100))(?:\+(\d{1,2}))?', string
        )
        if parsed_str:
            rolls, dice, addendant = parsed_str[0]
            dice.replace('к', 'd').replace('д', 'd')
            addendant = int(addendant) if addendant else 0
            return DiceRoll(
                dice=DiceIntEnum[dice.upper()], rolls=rolls, addendant=addendant
            )
        raise ValueError('Not valid DiceRoll')