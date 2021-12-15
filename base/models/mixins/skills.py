from dataclasses import asdict

from base.constants.constants import SkillsEnum
from base.objects.skills import Skills


class SkillMixin:
    @property
    def skill_mod_bonus(self):
        return Skills(
            **{
                skill.lname: getattr(
                    self, f'{skill.get_base_attribute().name.lower()[:3]}_mod'
                )
                for skill in SkillsEnum
            }
        )

    @property
    def skills(self) -> Skills:
        half_level = Skills.init_with_const(SkillsEnum, self.half_level)
        trained_skills = Skills.init_with_const(
            [SkillsEnum[trained_skill] for trained_skill in self.trained_skills], 5
        )
        race_bonus = self.race_data_instance.skill_bonuses
        mandatory_skills = self.klass_data_instance.mandatory_skills
        penalty = Skills.init_with_const(
            (
                SkillsEnum.ACROBATICS,
                SkillsEnum.ATHLETICS,
                SkillsEnum.THIEVERY,
                SkillsEnum.ENDURANCE,
                SkillsEnum.STEALTH,
            ),
            value=1,
        )
        return (
            half_level
            + trained_skills
            + mandatory_skills
            + race_bonus
            - penalty
            + self.skill_mod_bonus
        )

    @property
    def acrobatics(self):
        """Акробатика"""
        return self.skills.acrobatics

    @property
    def arcana(self):
        """Магия"""
        return self.skills.arcana

    @property
    def athletics(self):
        """Атлетика"""
        return self.skills.athletics

    @property
    def bluff(self):
        """Обман"""
        return self.skills.bluff

    @property
    def diplomacy(self):
        """Переговоры"""
        return self.skills.diplomacy

    @property
    def dungeoneering(self):
        """Подземелья"""
        return self.skills.dungeoneering

    @property
    def endurance(self):
        """Выносливость"""
        return self.skills.endurance

    @property
    def heal(self):
        """Целительство"""
        return self.skills.heal

    @property
    def history(self):
        """История"""
        return self.skills.history

    @property
    def insight(self):
        """Проницательность"""
        return self.skills.insight

    @property
    def intimidate(self):
        """Запугивание"""
        return self.skills.intimidate

    @property
    def nature(self):
        """Природа"""
        return self.skills.nature

    @property
    def perception(self):
        """Внимательность"""
        return self.skills.perception

    @property
    def religion(self):
        """Религия"""
        return self.skills.religion

    @property
    def stealth(self):
        """Скрытность"""
        return self.skills.stealth

    @property
    def streetwise(self):
        """Знание_улиц"""
        return self.skills.streetwise

    @property
    def thievery(self):
        """Воровство"""
        return self.skills.thievery

    @property
    def skills_text(self):
        result = []
        ordinary_skills = self.skill_mod_bonus + Skills.init_with_const(
            SkillsEnum, self.half_level
        )
        for skill, value in asdict(self.skills).items():
            if getattr(ordinary_skills, skill) != value:
                result.append(f'{SkillsEnum[skill.upper()].value} +{value}')
        return sorted(result)
