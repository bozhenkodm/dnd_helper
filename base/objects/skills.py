from dataclasses import dataclass
from typing import Sequence

from base.constants.constants import SkillsEnum


@dataclass
class Skills:
    acrobatics: int = 0
    arcana: int = 0
    athletics: int = 0
    bluff: int = 0
    diplomacy: int = 0
    dungeoneering: int = 0
    endurance: int = 0
    heal: int = 0
    history: int = 0
    insight: int = 0
    intimidate: int = 0
    nature: int = 0
    perception: int = 0
    religion: int = 0
    stealth: int = 0
    streetwise: int = 0
    thievery: int = 0

    def __add__(self, other):
        return Skills(
            self.acrobatics + other.acrobatics,
            self.arcana + other.arcana,
            self.athletics + other.athletics,
            self.bluff + other.bluff,
            self.diplomacy + other.diplomacy,
            self.dungeoneering + other.dungeoneering,
            self.endurance + other.endurance,
            self.heal + other.heal,
            self.history + other.history,
            self.insight + other.insight,
            self.intimidate + other.intimidate,
            self.nature + other.nature,
            self.perception + other.perception,
            self.religion + other.religion,
            self.stealth + other.stealth,
            self.streetwise + other.streetwise,
            self.thievery + other.thievery,
        )

    def __sub__(self, other):
        return Skills(
            self.acrobatics - other.acrobatics,
            self.arcana - other.arcana,
            self.athletics - other.athletics,
            self.bluff - other.bluff,
            self.diplomacy - other.diplomacy,
            self.dungeoneering - other.dungeoneering,
            self.endurance - other.endurance,
            self.heal - other.heal,
            self.history - other.history,
            self.insight - other.insight,
            self.intimidate - other.intimidate,
            self.nature - other.nature,
            self.perception - other.perception,
            self.religion - other.religion,
            self.stealth - other.stealth,
            self.streetwise - other.streetwise,
            self.thievery - other.thievery,
        )

    @classmethod
    def init_with_const(cls, skills: Sequence[SkillsEnum], value: int) -> "Skills":
        return Skills(**{skill.lname: value for skill in skills})

    def intersect(self, skills: Sequence[SkillsEnum]) -> "Skills":
        # return new instance with items that only present in skills
        return Skills(
            **{skill.lname: getattr(self, skill.lname, 0) for skill in skills}
        )
