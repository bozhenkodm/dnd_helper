from dataclasses import asdict

from base.constants.constants import SkillsEnum
from base.objects.skills import Skills


class SkillMixin:
    @property
    def _trained_skills_bonuses(self) -> Skills:
        # TODO refactor with Skills.intersect method
        return Skills(**{key.lower(): 5 for key in list(self.trained_skills)})

    def _calculate_skill(self, skill: SkillsEnum) -> int:
        attribute = getattr(self, skill.get_base_attribute().lname)
        result = (
            self.half_level
            + self._modifier(attribute)
            + getattr(self._trained_skills_bonuses, skill.lname)
        )
        if skill in (
            SkillsEnum.ACROBATICS,
            SkillsEnum.ATHLETICS,
            SkillsEnum.THIEVERY,
            SkillsEnum.ENDURANCE,
            SkillsEnum.STEALTH,
        ):
            result -= self.armor.skill_penalty
        return result

    @property
    def acrobatics(self):
        """Акробатика"""
        return self._calculate_skill(SkillsEnum.ACROBATICS)

    @property
    def arcana(self):
        """Магия"""
        return self._calculate_skill(SkillsEnum.ARCANA)

    @property
    def athletics(self):
        """Атлетика"""
        return self._calculate_skill(SkillsEnum.ATHLETICS)

    @property
    def bluff(self):
        """Обман"""
        return self._calculate_skill(SkillsEnum.BLUFF)

    @property
    def diplomacy(self):
        """Переговоры"""
        return self._calculate_skill(SkillsEnum.DIPLOMACY)

    @property
    def dungeoneering(self):
        """Подземелья"""
        return self._calculate_skill(SkillsEnum.DUNGEONEERING)

    @property
    def endurance(self):
        """Выносливость"""
        return self._calculate_skill(SkillsEnum.ENDURANCE)

    @property
    def heal(self):
        """Целительство"""
        return self._calculate_skill(SkillsEnum.HEAL)

    @property
    def history(self):
        """История"""
        return self._calculate_skill(SkillsEnum.HISTORY)

    @property
    def insight(self):
        """Проницательность"""
        return self._calculate_skill(SkillsEnum.INSIGHT)

    @property
    def intimidate(self):
        """Запугивание"""
        return self._calculate_skill(SkillsEnum.INTIMIDATE)

    @property
    def nature(self):
        """Природа"""
        return self._calculate_skill(SkillsEnum.NATURE)

    @property
    def perception(self):
        """Внимательность"""
        return self._calculate_skill(SkillsEnum.PERCEPTION)

    @property
    def religion(self):
        """Религия"""
        return self._calculate_skill(SkillsEnum.RELIGION)

    @property
    def stealth(self):
        """Скрытность"""
        return self._calculate_skill(SkillsEnum.STEALTH)

    @property
    def streetwise(self):
        """Знание_улиц"""
        return self._calculate_skill(SkillsEnum.STREETWISE)

    @property
    def thievery(self):
        """Воровство"""
        return self._calculate_skill(SkillsEnum.THIEVERY)

    @property
    def trained_skills_text(self):
        return list(
            f'{SkillsEnum[skill].value} +{self._calculate_skill(SkillsEnum[skill])}'
            for skill in self.trained_skills
            + [
                key.upper()
                for key, value in asdict(
                    self.klass_data_instance.mandatory_skills
                ).items()
                if value
            ]
        )

    # SkillsEnum[key.upper()]
    # for key, value in asdict(obj.klass_data_instance.mandatory_skills).items()
    #     if value

    @property
    def skills_text(self):
        return list(
            f'{skill.value} +{self._calculate_skill(skill)}' for skill in SkillsEnum
        )
