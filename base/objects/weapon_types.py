from dataclasses import dataclass

from base.constants.constants import (
    DiceIntEnum,
    WeaponCategoryIntEnum,
    WeaponGroupEnum,
    WeaponHandednessEnum,
    WeaponPropertyEnum,
)


@dataclass
class WeaponType:
    group: WeaponGroupEnum
    category: WeaponCategoryIntEnum
    damage_dice: DiceIntEnum
    properties: set[WeaponPropertyEnum]
    handedness: WeaponHandednessEnum
    name: str = None
    prof_bonus: int = 2
    dice_number: int = 1
    range: int = 0

    # def __post_init__(self):
    #     self.handedness

    @property
    def max_range(self):
        return self.range * 2

    def damage(self, weapon_number=1):
        return f'{self.dice_number*weapon_number}{self.damage_dice.description}'
