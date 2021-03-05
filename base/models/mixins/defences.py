from base.constants.constants import (
    ArmorTypeIntEnum,
    NPCClassIntEnum,
    ShieldTypeEnum,
    WeaponCategoryIntEnum,
)
from base.constants.subclass import FighterSubclass, SeekerSubclass, WardenSubclass


class DefenceMixin:
    @property
    def _shield_bonus(self):
        if self.shield and self.shield in self.klass.available_shield_types:
            if self.shield == ShieldTypeEnum.LIGHT.name:
                return 1
            return 2
        return 0

    @property
    def armor_class(self):
        result = 10 + self.half_level + self._level_bonus
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
            armor_attributes = [self.dexterity, self.intelligence]
            if (
                self.klass.name == NPCClassIntEnum.SEEKER
                and self.subclass == SeekerSubclass.SPIRITBOND
            ):
                # Духовная связь искателя/ловца
                armor_attributes.append(self.strength)
            if self.klass.name == NPCClassIntEnum.WARDEN:
                # Страж силы хранителя
                if self.subclass == WardenSubclass.EARTHSTRENGTH:
                    armor_attributes.append(self.constitution)
                elif self.subclass == WardenSubclass.WILDBLOOD:
                    armor_attributes.append(self.wisdom)
            result += max(map(self._modifier, armor_attributes))
        result += self._shield_bonus
        if self.klass.name == NPCClassIntEnum.AVENGER:
            # Доспех веры карателя
            if not self.shield and (
                not self.armor or self.armor.armor_type == ArmorTypeIntEnum.CLOTH
            ):
                result += 3
        if self.klass.name == NPCClassIntEnum.BARBARIAN:
            # Проворство варвара
            if not self.shield and (not self.armor or self.armor.is_light):
                result += self._tier + 1
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

        if self.klass.name == NPCClassIntEnum.SWORDMAGE:
            # Защита мечника-мага
            if not self.shield:
                result += 3
            else:
                result += 1

        if (
            self.klass.name == NPCClassIntEnum.VAMPIRE
            and not self.shield
            and (not self.armor or self.armor.armor_type == ArmorTypeIntEnum.CLOTH)
        ):
            # Рефлексы вампира
            result += 2
        return result

    @property
    def fortitude(self):
        result = (
            10
            + self.half_level
            + self._level_bonus
            + max(self._modifier(self.strength), self._modifier(self.constitution))
            + (
                self.functional_template.fortitude_bonus
                if self.functional_template
                else 0
            )
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
            10
            + self.half_level
            + self._level_bonus
            + max(self._modifier(self.dexterity), self._modifier(self.intelligence))
            + (self.functional_template.reflex_bonus if self.functional_template else 0)
        )
        result += self._shield_bonus
        if self.klass.name == NPCClassIntEnum.BARBARIAN:
            if not self.shield and self.armor.is_light:
                result += self._tier + 1
        return result

    @property
    def will(self):
        return (
            10
            + self.half_level
            + self._level_bonus
            + max(self._modifier(self.wisdom), self._modifier(self.charisma))
            + (self.functional_template.will_bonus if self.functional_template else 0)
        )
