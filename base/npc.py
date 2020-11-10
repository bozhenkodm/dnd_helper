from dataclasses import dataclass

from base.constants import NPCClass, NPCRace


@dataclass()
class Race:
    title: NPCRace
    speed: int

    fortitude_bonus: int = 0
    reflex_bonus: int = 0
    will_bonus: int = 0


@dataclass()
class Class:
    title: NPCClass


@dataclass()
class NPC:
    name: str
    race: NPCRace
    klass: NPCClass


class Warlord(Class):
    title = NPCClass.WARLORD
