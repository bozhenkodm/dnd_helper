from dataclasses import astuple, dataclass


@dataclass
class Abilities:
    strength: int = 0
    constitution: int = 0
    dexterity: int = 0
    intelligence: int = 0
    wisdom: int = 0
    charisma: int = 0

    def description(self):
        return astuple(self)

    def __add__(self, other):
        return Abilities(
            strength=self.strength + other.strength,
            constitution=self.constitution + other.constitution,
            dexterity=self.dexterity + other.dexterity,
            intelligence=self.intelligence + other.intelligence,
            wisdom=self.wisdom + other.wisdom,
            charisma=self.charisma + other.charisma,
        )
