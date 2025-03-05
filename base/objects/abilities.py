from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.db.models import QuerySet

if TYPE_CHECKING:
    from base.models.abilities import Ability


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
    def init_with_const(cls, abilities: QuerySet['Ability'], value: int) -> 'Abilities':
        return Abilities(**{ability.name: value for ability in abilities})
