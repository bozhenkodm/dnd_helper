from typing import ClassVar, Sequence, Type

from base.constants.constants import NPCRaceEnum
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

    available_weapon_types: ClassVar[Sequence[Type[WeaponType]]] = ()

    @property
    def heavy_armor_speed_penalty(self):
        return 1

    def __init__(self, npc):
        self.npc = npc


class DwarfRace(Race):
    slug = NPCRaceEnum.DWARF
    available_weapon_types = (Warhammer, ThrowingHammer)

    @property
    def heavy_armor_speed_penalty(self):
        # dwarfs don't get speed penalty
        return 0


class DragonbornRace(Race):
    slug = NPCRaceEnum.DRAGONBORN


class ShifterRace(Race):
    pass


class ShifterRazorclawRace(ShifterRace):
    slug = NPCRaceEnum.SHIFTER_RAZORCLAW


class ShifterLongteethRace(ShifterRace):
    slug = NPCRaceEnum.SHIFTER_LONGTEETH


class EladrinRace(Race):
    slug = NPCRaceEnum.ELADRIN
    available_weapon_types = (LongSword,)


class ElfRace(Race):
    slug = NPCRaceEnum.ELF
    available_weapon_types = (Longbow, Shortbow)


class VrylokaRace(Race):
    slug = NPCRaceEnum.VRYLOKA


class HamadryadRace(Race):
    slug = NPCRaceEnum.HAMADRYAD


class GithzeraiRace(Race):
    slug = NPCRaceEnum.GITHZERAI


class GnomeRace(Race):
    slug = NPCRaceEnum.GNOME


class GnollRace(Race):
    slug = NPCRaceEnum.GNOLL


class GoblinRace(Race):
    slug = NPCRaceEnum.GOBLIN


class GoliathRace(Race):
    slug = NPCRaceEnum.GOLIATH


class DevaRace(Race):
    slug = NPCRaceEnum.DEVA


class GenasiRace(Race):
    pass


class GenasiEarthsoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_EARTHSOUL


class GenasiFiresoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_FIRESOUL


class GenasiStormsoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_STORMSOUL


class GenasiWatersoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_WATERSOUL


class GenasiWindsoulRace(GenasiRace):
    slug = NPCRaceEnum.GENASI_WINDSOUL


class WildenRace(Race):
    slug = NPCRaceEnum.WILDEN


class DoppelgangerRace(Race):
    slug = NPCRaceEnum.DOPPELGANGER


class DrowRace(Race):
    slug = NPCRaceEnum.DROW


class DuergarRace(Race):
    slug = NPCRaceEnum.DUERGAR


class KalashtarRace(Race):
    slug = NPCRaceEnum.KALASHTAR


class KenkuRace(Race):
    slug = NPCRaceEnum.KENKU


class KoboldRace(Race):
    slug = NPCRaceEnum.KOBOLD


class WarforgedRace(Race):
    slug = NPCRaceEnum.WARFORGED


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


class HalflingRace(Race):
    slug = NPCRaceEnum.HALFLING


class HalforcRace(Race):
    slug = NPCRaceEnum.HALFORC


class PixieRace(Race):
    slug = NPCRaceEnum.PIXIE


class SatyrRace(Race):
    slug = NPCRaceEnum.SATYR


class TieflingRace(Race):
    slug = NPCRaceEnum.TIEFLING


class ThriKreenRace(Race):
    slug = NPCRaceEnum.THRI_KREEN


class HumanRace(Race):
    slug = NPCRaceEnum.HUMAN


class ShadarKaiRace(Race):
    slug = NPCRaceEnum.SHADAR_KAI


class HobgoblinRace(Race):
    slug = NPCRaceEnum.HOBGOBLIN


class BugbearRace(Race):
    slug = NPCRaceEnum.BUGBEAR
