from base.constants import AccessoryTypeEnum, AttributesEnum


class AttackMixin:
    def is_weapon_proficient(self, weapon) -> bool:
        return any(
            (
                weapon.weapon_type.category in self.klass.available_weapon_categories,
                weapon.weapon_type in self.klass.available_weapon_types.all(),
                weapon.weapon_type in self.race.available_weapon_types.all(),
            )
        )

    def is_implement_proficient(self, implement):
        return implement.implement_type in self.klass.available_implement_types.all()

    @property
    def attacks(self):
        """Бонусы атаки"""
        result = []
        for weapon in self.weapons.all():
            enchantment = min(weapon.enchantment, self._magic_threshold)
            bonus = self._level_bonus + self.half_level + enchantment
            if self.is_weapon_proficient(weapon):
                bonus += weapon.weapon_type.prof_bonus
            for power in self.klass.powers.filter(
                accessory_type=AccessoryTypeEnum.WEAPON.name
            ):
                attr_modifier = self.modifier(
                    getattr(self, power.attack_attribute.lower())
                )
                result.append(
                    (
                        AttributesEnum[power.attack_attribute].value,
                        weapon,
                        bonus + attr_modifier,
                        f'{weapon.weapon_type.damage(power.dice_number)} + {attr_modifier + enchantment}',
                    )
                )
        for implement in self.implements.all():
            if not self.is_implement_proficient(implement):
                continue
            enchantment = min(implement.enchantment, self._magic_threshold)
            bonus = self._level_bonus + self.half_level + enchantment
            for power in self.klass.powers.filter(
                accessory_type=AccessoryTypeEnum.IMPLEMENT.name
            ):
                attr_modifier = self.modifier(
                    getattr(self, power.attack_attribute.lower())
                )
                result.append(
                    (
                        AttributesEnum[power.attack_attribute].value,
                        implement,
                        bonus + attr_modifier,
                        f'{power.damage} + {enchantment}',
                    )
                )
        for weapon in self.weapons.all():
            if not hasattr(weapon.weapon_type, 'implement_type'):
                continue
            enchantment = min(weapon.enchantment, self._magic_threshold)
            bonus = self._level_bonus + self.half_level + enchantment
            for power in self.klass.powers.filter(
                accessory_type=AccessoryTypeEnum.IMPLEMENT.name
            ):
                attr_modifier = self.modifier(
                    getattr(self, power.attack_attribute.lower())
                )
                result.append(
                    (
                        AttributesEnum[power.attack_attribute].value,
                        f'{weapon} (инструмент)',
                        bonus + attr_modifier,
                        f'{power.damage} + {enchantment}',
                    )
                )
        return result
