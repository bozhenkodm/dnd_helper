class AttackMixin:
    def is_weapon_proficient(self, weapon) -> bool:
        data_instance = weapon.weapon_type.data_instance
        return any(
            (
                data_instance.category
                in map(int, self.klass_data_instance.available_weapon_categories),
                type(data_instance) in self.klass_data_instance.available_weapon_types,
                type(data_instance) in self.race_data_instance.available_weapon_types,
            )
        )

    def is_implement_proficient(self, implement):
        return (
            type(implement.implement_type)
            in self.klass_data_instance.available_implement_types
        )
