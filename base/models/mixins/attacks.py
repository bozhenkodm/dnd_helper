from base.constants.constants import (
    NPCClassIntEnum,
    WeaponCategoryIntEnum,
    WeaponHandednessEnum,
    WeaponPropertyEnum,
)
from base.constants.subclass import FighterSubclass, SeekerSubclass, SorcererSubclass


class AttackMixin:
    def is_weapon_proficient(self, weapon) -> bool:
        return any(
            (
                weapon.weapon_type.category
                in map(int, self.klass.available_weapon_categories),
                weapon.weapon_type in self.klass.available_weapon_types.all(),
                weapon.weapon_type in self.race.available_weapon_types.all(),
            )
        )

    def is_implement_proficient(self, implement):
        return implement.implement_type in self.klass.available_implement_types.all()

    def subclass_attack_bonus(self, weapon):
        if self.klass.name == NPCClassIntEnum.FIGHTER:
            if (
                self.subclass == FighterSubclass.GREAT_WEAPON
                and weapon.weapon_type.handedness == WeaponHandednessEnum.TWO.name
            ):
                return 1
            if (
                self.subclass == FighterSubclass.GUARDIAN
                and weapon.weapon_type.handedness == WeaponHandednessEnum.ONE.name
            ):
                return 1
            if (
                self.subclass == FighterSubclass.TEMPPEST
                and self.weapons.filter(
                    weapon_type__category__in=(
                        WeaponCategoryIntEnum.SIMPLE,
                        WeaponCategoryIntEnum.MILITARY,
                        WeaponCategoryIntEnum.SUPERIOR,
                    )
                ).count()
                == 2
                and self.weapons.filter(
                    weapon_type__properties__contains=WeaponPropertyEnum.OFF_HAND.name
                ).count()
                > 0
            ):
                return 1
        if (
            self.klass.name == NPCClassIntEnum.SEEKER
            and self.subclass == SeekerSubclass.SPIRITBOND
            and set(weapon.weapon_type.properties)
            & {
                WeaponPropertyEnum.LIGHT_THROWN.name,
                WeaponPropertyEnum.HEAVY_THROWN.name,
            }
        ):
            # Свойство духовной связи ловчего
            return 1

        return 0

    @property
    def class_damage_bonus(self):
        # TODO finish it up
        if self.klass.name == NPCClassIntEnum.SORCERER:
            if self.subclass == SorcererSubclass.DRAGON_MAGIC:
                return self._modifier(self.strength) + 2 * self._tier
            if self.subclass == SorcererSubclass.WILD_MAGIC:
                return self._modifier(self.dexterity) + 2 * self._tier
        return 0
