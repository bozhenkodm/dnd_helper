from dataclasses import dataclass

from base.constants.constants import AbilityEnum


@dataclass
class Abilities:
    strength: int = 0
    constitution: int = 0
    dexterity: int = 0
    intelligence: int = 0
    wisdom: int = 0
    charisma: int = 0

    def __add__(self, other) -> 'Abilities':
        return Abilities(
            strength=self.strength + other.strength,
            constitution=self.constitution + other.constitution,
            dexterity=self.dexterity + other.dexterity,
            intelligence=self.intelligence + other.intelligence,
            wisdom=self.wisdom + other.wisdom,
            charisma=self.charisma + other.charisma,
        )

    @classmethod
    def init_with_const(cls, *abilities: AbilityEnum, value: int) -> "Abilities":
        return Abilities(**{ability.lvalue: value for ability in abilities})
