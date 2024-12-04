from typing import ClassVar, Sequence, Type

from base.constants.constants import NPCRaceEnum, SizeEnum, VisionEnum
from base.objects.skills import Skills
from base.objects.weapon_types import (
    Longbow,
    LongSword,
    Shortbow,
    ThrowingHammer,
    Warhammer,
    WeaponType,
)


class Race:
    slug: ClassVar[NPCRaceEnum]
    speed: ClassVar[int] = 6
    skill_bonuses: ClassVar[Skills] = Skills()

    available_weapon_types: ClassVar[Sequence[Type[WeaponType]]] = ()
    vision: ClassVar[VisionEnum] = VisionEnum.NORMAL
    size: ClassVar[SizeEnum] = SizeEnum.AVERAGE

    fortitude: ClassVar[int] = 0
    reflex: ClassVar[int] = 0
    will: ClassVar[int] = 0

    surges_number_bonus: ClassVar[int] = 0

    initiative: ClassVar[int] = 0

    @property
    def heavy_armor_speed_penalty(self):
        return 1

    def __init__(self, npc):
        self.npc = npc


class DwarfRace(Race):
    slug = NPCRaceEnum.DWARF
    speed = 5
    vision = VisionEnum.TWILIGHT
    skill_bonuses = Skills(endurance=2, dungeoneering=2)
    available_weapon_types = (Warhammer, ThrowingHammer)

    @property
    def heavy_armor_speed_penalty(self):
        # dwarfs don't get speed penalty
        return 0


class DragonbornRace(Race):
    slug = NPCRaceEnum.DRAGONBORN
    skill_bonuses = Skills(intimidate=2, history=2)


class ShifterRace(Race):
    vision = VisionEnum.TWILIGHT


class ShifterRazorclawRace(ShifterRace):
    slug = NPCRaceEnum.SHIFTER_RAZORCLAW
    skill_bonuses = Skills(acrobatics=2, stealth=2)


class ShifterLongteethRace(ShifterRace):
    slug = NPCRaceEnum.SHIFTER_LONGTEETH
    skill_bonuses = Skills(athletics=2, endurance=2)


class EladrinRace(Race):
    slug = NPCRaceEnum.ELADRIN
    skill_bonuses = Skills(history=2, arcana=2)
    available_weapon_types = (LongSword,)
    vision = VisionEnum.TWILIGHT
    will = 1


class ElfRace(Race):
    slug = NPCRaceEnum.ELF
    skill_bonuses = Skills(perception=2, nature=2)
    available_weapon_types = (Longbow, Shortbow)
    vision = VisionEnum.TWILIGHT
    speed = 7


class VrylokaRace(Race):
    slug = NPCRaceEnum.VRYLOKA
    vision = VisionEnum.TWILIGHT
    skill_bonuses = Skills(perception=2, stealth=2)
    speed = 7


class HamadryadRace(Race):
    slug = NPCRaceEnum.HAMADRYAD
    skill_bonuses = Skills(diplomacy=2, nature=2)
    vision = VisionEnum.TWILIGHT


class GithzeraiRace(Race):
    slug = NPCRaceEnum.GITHZERAI
    skill_bonuses = Skills(acrobatics=2, athletics=2)
    initiative = 2


class GnomeRace(Race):
    slug = NPCRaceEnum.GNOME
    skill_bonuses = Skills(arcana=2, stealth=2)
    size = SizeEnum.SMALL
    speed = 5


class GnollRace(Race):
    slug = NPCRaceEnum.GNOLL
    skill_bonuses = Skills(intimidate=2, perception=2)
    vision = VisionEnum.TWILIGHT
    speed = 7


class GoblinRace(Race):
    slug = NPCRaceEnum.GOBLIN
    skill_bonuses = Skills(thievery=2, stealth=2)
    reflex = 1
    size = SizeEnum.SMALL
    vision = VisionEnum.TWILIGHT


class GoliathRace(Race):
    slug = NPCRaceEnum.GOLIATH
    skill_bonuses = Skills(athletics=2, nature=2)
    will = 1


class DevaRace(Race):
    slug = NPCRaceEnum.DEVA
    skill_bonuses = Skills(history=2, religion=2)


class GenasiRace(Race):
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
    skill_bonuses = Skills(nature=2, stealth=2)
    vision = VisionEnum.TWILIGHT


class DoppelgangerRace(Race):
    slug = NPCRaceEnum.DOPPELGANGER
    skill_bonuses = Skills(bluff=2, insight=2)
    will = 1


class DrowRace(Race):
    slug = NPCRaceEnum.DROW
    skill_bonuses = Skills(intimidate=2, stealth=2)
    vision = VisionEnum.DARK


class DuergarRace(Race):
    slug = NPCRaceEnum.DUERGAR
    skill_bonuses = Skills(dungeoneering=2)
    vision = VisionEnum.DARK


class KalashtarRace(Race):
    slug = NPCRaceEnum.KALASHTAR
    skill_bonuses = Skills(insight=2)  # +1 skill of choice


class KenkuRace(Race):
    slug = NPCRaceEnum.KENKU
    skill_bonuses = Skills(bluff=2, stealth=2)
    vision = VisionEnum.TWILIGHT


class KoboldRace(Race):
    slug = NPCRaceEnum.KOBOLD
    skill_bonuses = Skills(dungeoneering=2, thievery=2)
    size = SizeEnum.SMALL
    vision = VisionEnum.DARK


class WarforgedRace(Race):
    slug = NPCRaceEnum.WARFORGED
    skill_bonuses = Skills(intimidate=2, endurance=2)


class BladelingRace(Race):
    slug = NPCRaceEnum.BLADELING
    skill_bonuses = Skills(arcana=2, intimidate=2)


class MinotaurRace(Race):
    slug = NPCRaceEnum.MINOTAUR
    skill_bonuses = Skills(nature=2, perception=2)
    surges_number_bonus = 1


class MulRace(Race):
    slug = NPCRaceEnum.MUL
    skill_bonuses = Skills(endurance=2, streetwise=2)
    surges_number_bonus = 1


class OrcRace(Race):
    slug = NPCRaceEnum.ORC
    vision = VisionEnum.TWILIGHT


class HalfelfRace(Race):
    slug = NPCRaceEnum.HALFELF
    skill_bonuses = Skills(diplomacy=2, insight=2)
    vision = VisionEnum.TWILIGHT


class HalflingRace(Race):
    slug = NPCRaceEnum.HALFLING
    skill_bonuses = Skills(acrobatics=2, thievery=2)
    size = SizeEnum.SMALL


class HalforcRace(Race):
    slug = NPCRaceEnum.HALFORC
    skill_bonuses = Skills(endurance=2, intimidate=2)
    vision = VisionEnum.TWILIGHT


class PixieRace(Race):
    slug = NPCRaceEnum.PIXIE
    skill_bonuses = Skills(nature=2, stealth=2)
    size = SizeEnum.TINY
    vision = VisionEnum.TWILIGHT


class SatyrRace(Race):
    slug = NPCRaceEnum.SATYR
    skill_bonuses = Skills(nature=2, thievery=2)
    vision = VisionEnum.TWILIGHT


class TieflingRace(Race):
    slug = NPCRaceEnum.TIEFLING
    skill_bonuses = Skills(bluff=2, stealth=2)
    vision = VisionEnum.TWILIGHT


class ThriKreenRace(Race):
    slug = NPCRaceEnum.THRI_KREEN
    skill_bonuses = Skills(athletics=2, nature=2)
    speed = 7
    vision = VisionEnum.DARK


class HumanRace(Race):
    slug = NPCRaceEnum.HUMAN
    fortitude = 1
    reflex = 1
    will = 1


class ShadarKaiRace(Race):
    slug = NPCRaceEnum.SHADAR_KAI
    vision = VisionEnum.TWILIGHT
    skill_bonuses = Skills(acrobatics=2, stealth=2)
    fortitude = 1


class HobgoblinRace(Race):
    slug = NPCRaceEnum.HOBGOBLIN
    vision = VisionEnum.TWILIGHT
    skill_bonuses = Skills(athletics=2, history=2)
    initiative = 2


class BugbearRace(Race):
    slug = NPCRaceEnum.BUGBEAR
    skill_bonuses = Skills(intimidate=2, stealth=2)
    vision = VisionEnum.TWILIGHT
