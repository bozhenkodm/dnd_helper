from dataclasses import dataclass

from base.constants import NPCClassEnum, NPCRaceEnum


@dataclass()
class Race:
    title: NPCRaceEnum
    speed: int

    fortitude_bonus: int = 0
    reflex_bonus: int = 0
    will_bonus: int = 0


@dataclass()
class Class:
    title: NPCClassEnum


@dataclass()
class NPC:
    name: str
    race: NPCRaceEnum
    klass: NPCClassEnum


class Warlord(Class):
    title = NPCClassEnum.WARLORD
