# flake8: noqa
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Protocol, Sequence

from django.db.models import Manager, Q, QuerySet

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from base.constants.constants import (
        AbilityEnum,
        AccessoryTypeEnum,
        DefenceTypeEnum,
        NPCOtherProperties,
        SkillEnum,
    )
    from base.models.abilities import Ability
    from base.models.feats import Feat
    from base.models.items import (
        Armor,
        ArmsSlotItem,
        FeetSlotItem,
        HandsSlotItem,
        HeadSlotItem,
        ItemAbstract,
        NeckSlotItem,
        RingsSlotItem,
        WaistSlotItem,
        Weapon,
        WeaponType,
    )
    from base.models.klass import Class
    from base.models.models import FunctionalTemplate, ParagonPath, Race
    from base.models.powers import Power
    from base.models.skills import Skill
    from base.objects.dice import DiceRoll


class NPCProtocol(Protocol):
    id: int
    neck_slot: 'NeckSlotItem'
    head_slot: 'HeadSlotItem'
    feet_slot: 'FeetSlotItem'
    waist_slot: 'WaistSlotItem'
    gloves_slot: 'HandsSlotItem'
    left_ring_slot: 'RingsSlotItem'
    right_ring_slot: 'RingsSlotItem'
    arms_slot: 'ArmsSlotItem'
    base_strength: int
    base_constitution: int
    base_dexterity: int
    base_intelligence: int
    base_wisdom: int
    base_charisma: int
    var_bonus_ability: 'Ability'
    experience: int
    klass: 'Class'
    subclass_id: int
    owner: 'User'
    name: str
    description: str
    race: 'Race'
    functional_template: 'FunctionalTemplate'
    paragon_path: 'ParagonPath'
    sex: str
    level: int
    is_bonus_applied: bool
    armor: 'Armor'
    primary_hand: 'Weapon'
    secondary_hand: 'Weapon'
    no_hand: 'Weapon'
    feats: Manager['Feat']
    trained_weapons: Manager['WeaponType']
    level_ability_bonuses: Manager['Ability']
    trained_skills: Manager['Skill']
    powers: Manager['Power']

    @property
    def shield(self) -> Optional: ...
    @property
    def _shield_bonus(self) -> int: ...
    @property
    def _defence_level_bonus(self) -> int: ...
    @property
    def _necklace_defence_bonus(self) -> int: ...
    @property
    def _armor_class_ability_bonus(self) -> int: ...
    @property
    def armor_class_bonus(self) -> int: ...
    @property
    def armor_class(self) -> int: ...
    @property
    def fortitude(self) -> int: ...
    @property
    def reflex(self) -> int: ...
    @property
    def will(self) -> int: ...
    @property
    def _power_attrs(self) -> dict: ...
    @property
    def _is_no_hand_implement_ki_focus(self) -> bool: ...
    def _can_get_bonus_from_implement_to_weapon(
        self: NPCProtocol, accessory_type: AccessoryTypeEnum | None
    ): ...
    def _calculate_weapon_damage(
        self: NPCProtocol, weapon: Weapon, accessory_type: AccessoryTypeEnum | None
    ): ...
    def attack_bonus(
        self: NPCProtocol, weapon=None, is_implement: bool = False
    ) -> int: ...
    def _calculate_attack(
        self: NPCProtocol, weapon: Weapon, accessory_type: AccessoryTypeEnum | None
    ): ...
    def _calculate_damage_bonus(
        self: NPCProtocol, weapon: Weapon, accessory_type: AccessoryTypeEnum | None
    ): ...
    def calculate_token(
        self: NPCProtocol,
        token: str,
        accessory_type: AccessoryTypeEnum | None,
        weapon=None,
        secondary_weapon=None,
        item=None,
    ) -> int | DiceRoll: ...
    def enhancement_with_magic_threshold(
        self: NPCProtocol, enhancement: int
    ) -> int: ...
    def calculate_reverse_polish_notation(
        self: NPCProtocol,
        expression: str,
        accessory_type: AccessoryTypeEnum | None,
        weapon=None,
        secondary_weapon=None,
        item=None,
    ): ...
    def evaluate_power_expression(
        self: NPCProtocol,
        string: str,
        accessory_type: AccessoryTypeEnum | None = None,
        weapon=None,
        secondary_weapon=None,
        item=None,
    ): ...
    def valid_properties(self: NPCProtocol, power: 'Power'): ...
    def parse_string(
        self: NPCProtocol,
        accessory_type: AccessoryTypeEnum | None,
        string: str,
        weapons: Sequence = (),
        item: Optional['ItemAbstract'] = None,
    ): ...
    def get_power_display(
        self: NPCProtocol,
        power: 'Power',
        weapons: Sequence = (),
        item: Optional['ItemAbstract'] = None,
    ) -> dict: ...
    def magic_item_powers(self: NPCProtocol) -> QuerySet: ...
    @property
    def _powers_cache_key(self) -> str: ...
    def cache_powers(self: NPCProtocol): ...
    def get_power_feats_bonuses_query(self: NPCProtocol) -> Q: ...
    def calculate_bonuses(
        self: NPCProtocol,
        bonus_types: AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties,
        check_cache: bool = False,
    ) -> dict: ...
    def calculate_bonus(
        self: NPCProtocol,
        bonus_type: AbilityEnum | SkillEnum | DefenceTypeEnum | NPCOtherProperties,
    ) -> int: ...
    def cache_bonuses(self: NPCProtocol): ...
    @property
    def _bonus_cache_key(self) -> str: ...
