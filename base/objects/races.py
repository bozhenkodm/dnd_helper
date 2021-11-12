from typing import ClassVar, Sequence

from base.constants.constants import NPCRaceEnum, SizeEnum, VisionEnum
from base.objects.abilities import Abilities
from base.objects.skills import Skills
from base.objects.weapon_types import (
    Longbow,
    LongSword,
    Shortbow,
    ThrowingHammer,
    Warhammer,
    WeaponType,
)

# TODO add the rest of race properties


class Race:
    slug: ClassVar[NPCRaceEnum] = None
    speed: ClassVar[int] = 6
    const_ability_bonus: ClassVar[Abilities] = Abilities()
    var_ability_bonus: ClassVar[Abilities] = Abilities()
    fortitude_bonus: ClassVar[int] = 0
    reflex_bonus: ClassVar[int] = 0
    will_bonus: ClassVar[int] = 0

    skill_bonuses: ClassVar[Skills] = Skills()

    available_weapon_types: ClassVar[Sequence[WeaponType]] = frozenset()
    vision: ClassVar[VisionEnum] = VisionEnum.NORMAL
    size: ClassVar[SizeEnum] = SizeEnum.AVERAGE

    armor_class: ClassVar[int] = 0
    fortitude: ClassVar[int] = 0
    reflex: ClassVar[int] = 0
    will: ClassVar[int] = 0

    @property
    def healing_surge_bonus(self):
        return 0

    @property
    def heavy_armor_speed_penalty(self):
        return 1

    @property
    def initiative(self):
        return 0

    def __init__(self, npc):
        self.npc = npc


class DwarfRace(Race):
    slug = NPCRaceEnum.DWARF
    const_ability_bonus = Abilities(constitution=2)
    var_ability_bonus = Abilities(strength=2, wisdom=2)
    speed = 5
    vision = VisionEnum.TWILIGHT
    skill_bonuses = Skills(endurance=2, dungeoneering=2)
    available_weapon_types = {Warhammer, ThrowingHammer}

    @property
    def heavy_armor_speed_penalty(self):
        return 0


class DragonbornRace(Race):
    slug = NPCRaceEnum.DRAGONBORN
    const_ability_bonus = Abilities(charisma=2)
    var_ability_bonus = Abilities(strength=2, constitution=2)
    skill_bonuses = Skills(intimidate=2, history=2)

    @property
    def healing_surge_bonus(self):
        # У драконорождённых исцеление увеличено
        return self.npc.constitution


class ShifterRace(Race):
    vision = VisionEnum.TWILIGHT


class ShifterRazorclawRace(ShifterRace):
    slug = NPCRaceEnum.SHIFTER_RAZORCLAW
    const_ability_bonus = Abilities(dexterity=2, wisdom=2)
    skill_bonuses = Skills(acrobatics=2, stealth=2)


class ShifterLongteethRace(ShifterRace):
    slug = NPCRaceEnum.SHIFTER_LONGTEETH
    const_ability_bonus = Abilities(strength=2, wisdom=2)
    skill_bonuses = Skills(athletics=2, endurance=2)


class EladrinRace(Race):
    slug = NPCRaceEnum.ELADRIN
    const_ability_bonus = Abilities(intelligence=2)
    var_ability_bonus = Abilities(dexterity=2, charisma=2)
    skill_bonuses = Skills(history=2, arcana=2)
    available_weapon_types = (LongSword,)
    vision = VisionEnum.TWILIGHT
    will = 1


class ElfRace(Race):
    slug = NPCRaceEnum.ELF
    const_ability_bonus = Abilities(dexterity=2)
    var_ability_bonus = Abilities(wisdom=2, intelligence=2)
    skill_bonuses = Skills(perception=2, nature=2)
    available_weapon_types = (Longbow, Shortbow)
    vision = VisionEnum.TWILIGHT
    speed = 7


class VrylokaRace(Race):
    slug = NPCRaceEnum.VRYLOKA
    const_ability_bonus = Abilities(charisma=2)
    var_ability_bonus = Abilities(strength=2, dexterity=2)
    vision = VisionEnum.TWILIGHT
    skill_bonuses = Skills(perception=2, stealth=2)
    speed = 7


class HamadryadRace(Race):
    slug = NPCRaceEnum.HAMADRYAD


class GithzeraiRace(Race):
    slug = NPCRaceEnum.GITHZERAI


class GnomeRace(Race):
    slug = NPCRaceEnum.GNOME
    const_ability_bonus = Abilities(intelligence=2)
    var_ability_bonus = Abilities(dexterity=2, charisma=2)
    skill_bonuses = Skills(arcana=2, stealth=2)
    size = SizeEnum.SMALL
    speed = 5


class GnollRace(Race):
    slug = NPCRaceEnum.GNOLL


class GoblinRace(Race):
    slug = NPCRaceEnum.GOBLIN
    const_ability_bonus = Abilities(dexterity=2)
    var_ability_bonus = Abilities(wisdom=2, charisma=2)
    skill_bonuses = Skills(thievery=2, stealth=2)
    reflex = 1
    size = SizeEnum.SMALL
    vision = VisionEnum.TWILIGHT


class GoliathRace(Race):
    slug = NPCRaceEnum.GOLIATH
    const_ability_bonus = Abilities(strength=2)
    var_ability_bonus = Abilities(constitution=2, wisdom=2)
    skill_bonuses = Skills(athletics=2, nature=2)
    will = 1


class DevaRace(Race):
    slug = NPCRaceEnum.DEVA
    const_ability_bonus = Abilities(wisdom=2)
    var_ability_bonus = Abilities(intelligence=2, charisma=2)
    skill_bonuses = Skills(history=2, religion=2)


class GenasiRace(Race):
    const_ability_bonus = Abilities(intelligence=2)
    var_ability_bonus = Abilities(strength=2, constitution=2)
    skill_bonuses = Skills(endurance=2, nature=2)


class GenasiEarthsoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_EARTHSOUL
    fortitude = 1


class GenasiFiresoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_FIRESOUL
    reflex = 1


class GenasiStormsoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_STORMSOUL
    fortitude = 1


class GenasiWatersoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_WATERSOUL


class GenasiWindsoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_WINDSOUL


class WildenRace(Race):
    slug = NPCRaceEnum.WILDEN


class DoppelgangerRace(Race):
    slug = NPCRaceEnum.DOPPELGANGER
    const_ability_bonus = Abilities(charisma=2)
    var_ability_bonus = Abilities(dexterity=2, intelligence=2)
    skill_bonuses = Skills(bluff=2, insight=2)
    will = 1


class DrowRace(Race):
    slug = NPCRaceEnum.DROW
    const_ability_bonus = Abilities(dexterity=2)
    var_ability_bonus = Abilities(wisdom=2, charisma=2)
    skill_bonuses = Skills(intimidate=2, stealth=2)
    vision = VisionEnum.DARK


class DuergarRace(Race):
    slug = NPCRaceEnum.DUERGAR


class KalashtarRace(Race):
    slug = NPCRaceEnum.KALASHTAR
    const_ability_bonus = Abilities(charisma=2)
    var_ability_bonus = Abilities(intelligence=2, wisdom=2)
    skill_bonuses = Skills(insight=2)  # +1 skill of choice


class KenkuRace(Race):
    slug = NPCRaceEnum.KENKU


class KoboldRace(Race):
    slug = NPCRaceEnum.KOBOLD


class WarforgedRace(Race):
    slug = NPCRaceEnum.WARFORGED
    const_ability_bonus = Abilities(constitution=2)
    var_ability_bonus = Abilities(strength=2, intelligence=2)
    skill_bonuses = Skills(intimidate=2, endurance=2)


class BladelingRace(Race):
    slug = NPCRaceEnum.BLADELING


class MinotaurRace(Race):
    slug = NPCRaceEnum.MINOTAUR


class MulRace(Race):
    slug = NPCRaceEnum.MUL


class OrcRace(Race):
    slug = NPCRaceEnum.ORC


class HalfelfRace(Race):
    slug = NPCRaceEnum.HALFELF
    const_ability_bonus = Abilities(constitution=2)
    var_ability_bonus = Abilities(wisdom=2, charisma=2)
    skill_bonuses = Skills(diplomacy=2, insight=2)
    vision = VisionEnum.TWILIGHT


class HalflingRace(Race):
    slug = NPCRaceEnum.HALFLING
    const_ability_bonus = Abilities(dexterity=2)
    var_ability_bonus = Abilities(charisma=2, constitution=2)
    skill_bonuses = Skills(acrobatics=2, thievery=2)
    size = SizeEnum.SMALL


class HalforcRace(Race):
    slug = NPCRaceEnum.HALFORC
    const_ability_bonus = Abilities(dexterity=2)
    var_ability_bonus = Abilities(strength=2, constitution=2)
    skill_bonuses = Skills(endurance=2, intimidate=2)


class PixieRace(Race):
    slug = NPCRaceEnum.PIXIE
    size = SizeEnum.TINY


class SatyrRace(Race):
    slug = NPCRaceEnum.SATYR


class TieflingRace(Race):
    slug = NPCRaceEnum.TIEFLING
    const_ability_bonus = Abilities(charisma=2)
    var_ability_bonus = Abilities(constitution=2, intelligence=2)
    skill_bonuses = Skills(bluff=2, stealth=2)
    vision = VisionEnum.TWILIGHT


class ThriKreenRace(Race):
    slug = NPCRaceEnum.THRI_KREEN


class HumanRace(Race):
    slug = NPCRaceEnum.HUMAN
    var_ability_bonus = Abilities(
        strength=2, constitution=2, dexterity=2, intelligence=2, wisdom=2, charisma=2
    )
    fortitude = 1
    reflex = 1
    will = 1


class ShadarKaiRace(Race):
    slug = NPCRaceEnum.SHADAR_KAI


class HobgoblinRace(Race):
    slug = NPCRaceEnum.HOBGOBLIN
    const_ability_bonus = Abilities(constitution=2)
    var_ability_bonus = Abilities(intelligence=2, charisma=2)
    vision = VisionEnum.TWILIGHT
    skill_bonuses = Skills(athletics=2, history=2)

    @property
    def initiative(self):
        """Готовый к битве"""
        return 2


class BugbearRace(Race):
    slug = NPCRaceEnum.BUGBEAR
