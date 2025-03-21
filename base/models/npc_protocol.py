from typing import Any, Iterable, Protocol, Sequence

from django.contrib.auth.models import User

from base.models.abilities import Ability
from base.models.items import (
    Armor,
    ArmsSlotItem,
    FeetSlotItem,
    HandsSlotItem,
    HeadSlotItem,
    NeckSlotItem,
    RingsSlotItem,
    WaistSlotItem,
    Weapon,
)
from base.models.klass import Class
from base.models.models import FunctionalTemplate, ParagonPath, Race
from base.models.powers import Power


class NPCProtocol(Protocol):
    id: int
    neck_slot: NeckSlotItem
    head_slot: HeadSlotItem
    feet_slot: FeetSlotItem
    waist_slot: WaistSlotItem
    gloves_slot: HandsSlotItem
    left_ring_slot: RingsSlotItem
    right_ring_slot: RingsSlotItem
    arms_slot: ArmsSlotItem
    base_strength: int
    base_constitution: int
    base_dexterity: int
    base_intelligence: int
    base_wisdom: int
    base_charisma: int
    var_bonus_ability: Ability
    experience: int
    klass: Class
    subclass_id: int
    owner: User
    name: str
    description: str
    race: Race
    functional_template: FunctionalTemplate
    paragon_path: ParagonPath
    sex: str
    level: int
    is_bonus_applied: bool
    armor: Armor
    primary_hand: Weapon
    secondary_hand: Weapon
    no_hand: Weapon
    feats: Any
    trained_weapons: Any
    level_ability_bonuses: Any
    trained_skills: Any
    powers: Any

    @property
    def full_class_name(self) -> str: ...
    @property
    def url(self) -> str: ...
    def get_absolute_url(self) -> str: ...
    @property
    def half_level(self) -> int: ...
    @property
    def _magic_threshold(self) -> int: ...
    @property
    def _level_bonus(self) -> int: ...
    @property
    def max_hit_points(self) -> int: ...
    @property
    def bloodied(self) -> int: ...
    @property
    def surge(self) -> int: ...
    @property
    def _tier(self) -> int: ...
    @property
    def surges(self) -> int: ...
    @property
    def damage_bonus(self) -> int: ...
    @property
    def initiative(self) -> int: ...
    @property
    def speed(self) -> int: ...
    @property
    def items(self) -> tuple: ...
    @property
    def magic_items(self) -> Sequence: ...
    @property
    def magic_item_types(self) -> Sequence: ...
    def is_weapon_proficient(self, weapon: Weapon) -> bool: ...
    def is_implement_proficient(self, weapon: Weapon) -> bool: ...
    def proper_weapons_for_power(self, power: Power) -> Sequence: ...
    @property
    def inventory_text(self) -> Iterable: ...
    def powers_calculate(self) -> Sequence: ...
    def powers_calculated(self) -> Sequence: ...
    def cache_all(self): ...
