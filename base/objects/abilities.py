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
