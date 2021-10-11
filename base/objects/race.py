class RaceBase:
    name = None
    speed: int = 6
    # const_bonus_attrs
    # var_bonus_attrs
    fortitude_bonus: int = 0
    reflex_bonus: int = 0
    will_bonus: int = 0

    # skill_bonuses

    # available_weapon_types

    def __init__(self, npc):
        self.npc = npc

    @property
    def armor_class(self):
        return 0

    @property
    def fortitude(self):
        return 0

    @property
    def reflex(self):
        return 0

    @property
    def will(self):
        return 0
