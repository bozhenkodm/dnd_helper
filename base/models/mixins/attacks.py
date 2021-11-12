class AttackMixin:
    def is_weapon_proficient(self, weapon) -> bool:
        data_instance = weapon.weapon_type.data_instance
        return any(
            (
                data_instance.category
                in map(int, self.klass.data_instance.available_weapon_categories),
                type(data_instance) in self.klass.data_instance.available_weapon_types,
                type(data_instance) in self.race.data_instance.available_weapon_types,
            )
        )

    def is_implement_proficient(self, implement):
        return implement.implement_type in self.klass.available_implement_types.all()
