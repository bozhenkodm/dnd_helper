from base.constants.constants import (
    NPCClassIntEnum,
    ShieldTypeEnum,
    WeaponCategoryIntEnum,
)
from base.constants.subclass import FighterSubclass

INITIAL_DEFENCE_VALUE = 10


class DefenceMixin:
    @property
    def _shield_bonus(self):
        if self.shield and self.shield in self.klass.available_shield_types:
            if self.shield == ShieldTypeEnum.LIGHT.name:
                return 1
            return 2
        return 0

    @property
    def _defence_level_bonus(self):
        return INITIAL_DEFENCE_VALUE + self.half_level + self._level_bonus

    @property
    def armor_class(self):
        result = self._defence_level_bonus + self.race.data_instance.armor_class
        result += (
            self.functional_template.armor_class_bonus
            if self.functional_template
            else 0
        )
        if self.armor:
            if self.armor.armor_type in map(int, self.klass.available_armor_types):
                result += self.armor.armor_class
            result += min(self.armor.enchantment, self._magic_threshold)
        if not self.armor or self.armor.is_light:
            result += self.klass.data_instance.armor_class_bonus(npc=self)
        result += self._shield_bonus
        if self.klass.name == NPCClassIntEnum.FIGHTER:
            if (
                self.subclass == FighterSubclass.BRAWLER
                and self.weapons.filter(
                    weapon_type__category__in=(
                        WeaponCategoryIntEnum.SIMPLE,
                        WeaponCategoryIntEnum.MILITARY,
                        WeaponCategoryIntEnum.SUPERIOR,
                    )
                ).count()
                == 1
                and not self.shield
            ):
                result += 1

        return result

    @property
    def fortitude(self):
        result = (
            self._defence_level_bonus
            + max(self._modifier(self.strength), self._modifier(self.constitution))
            + (
                self.functional_template.fortitude_bonus
                if self.functional_template
                else 0
            )
            + self.race.data_instance.fortitude
            + self.klass.data_instance.fortitude
        )
        if self.klass.name == NPCClassIntEnum.FIGHTER:
            if (
                self.subclass == FighterSubclass.BRAWLER
                and self.weapons.filter(
                    weapon_type__category__in=(
                        WeaponCategoryIntEnum.SIMPLE,
                        WeaponCategoryIntEnum.MILITARY,
                        WeaponCategoryIntEnum.SUPERIOR,
                    )
                ).count()
                == 1
                and not self.shield
            ):
                result += 2
        return result

    @property
    def reflex(self):
        result = (
            self._defence_level_bonus
            + max(self._modifier(self.dexterity), self._modifier(self.intelligence))
            + (self.functional_template.reflex_bonus if self.functional_template else 0)
            + self.race.data_instance.reflex
            + self.klass.data_instance.reflex
        )
        result += self._shield_bonus
        if self.klass.name == NPCClassIntEnum.BARBARIAN:
            if not self.shield and self.armor.is_light:
                result += self._tier + 1
        return result

    @property
    def will(self):
        return (
            self._defence_level_bonus
            + max(self._modifier(self.wisdom), self._modifier(self.charisma))
            + (self.functional_template.will_bonus if self.functional_template else 0)
            + self.race.data_instance.will
            + self.klass.data_instance.will
        )
