from dataclasses import asdict, dataclass

from base.constants.constants import AbilitiesEnum


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

    @property
    def enum_objects(self) -> list[AbilitiesEnum]:
        return [
            AbilitiesEnum[ability_name.upper()]
            for ability_name, value in asdict(self).items()
            if value
        ]
