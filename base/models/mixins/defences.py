from base.constants import ArmorTypeEnum, NPCClassEnum, ShieldTypeEnum


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
        if self.armor:
            if self.armor.armor_type in self.klass.available_armor_types:
                result += self.armor.armor_class
            result += min(self.armor.enchantment, self._magic_threshold)
        if not self.armor or self.armor.is_light:
            result += max(
                self.modifier(self.dexterity), self.modifier(self.intelligence)
            )
        result += self._shield_bonus
        if self.klass.name == NPCClassEnum.BARBARIAN.name:
            if not self.shield and self.armor.is_light:
                result += self._tier + 1
        if self.klass.name == NPCClassEnum.AVENGER.name:
            if not self.shield and (
                not self.armor or self.armor.armor_type == ArmorTypeEnum.CLOTH.name
            ):
                result += 3
        return result

    @property
    def fortitude(self):
        return (
            10
            + self.half_level
            + self._level_bonus
            + max(self.modifier(self.strength), self.modifier(self.constitution))
        )

    @property
    def reflex(self):
        result = (
            10
            + self.half_level
            + self._level_bonus
            + max(self.modifier(self.dexterity), self.modifier(self.intelligence))
        )
        result += self._shield_bonus
        if self.klass.name == NPCClassEnum.BARBARIAN.name:
            if not self.shield and self.armor.is_light:
                result += self._tier + 1
        return result

    @property
    def will(self):
        return (
            10
            + self.half_level
            + self._level_bonus
            + max(self.modifier(self.wisdom), self.modifier(self.charisma))
        )
