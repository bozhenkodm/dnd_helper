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
