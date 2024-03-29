from dataclasses import asdict

from django.db import models

from base.constants.constants import SkillEnum
from base.models.abilities import Ability
from base.objects.npc_classes import NPCClass
from base.objects.races import Race
from base.objects.skills import Skills


class Skill(models.Model):
    class Meta:
        ordering = ('ordering',)

    title = models.CharField(
        choices=SkillEnum.generate_choices(),
        max_length=SkillEnum.max_length(),
        primary_key=True,
    )
    based_on = models.ForeignKey(Ability, on_delete=models.CASCADE, null=False)
    ordering = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.get_title_display()


class NPCSkillMixin:
    race_data_instance: Race
    klass_data_instance: NPCClass
    half_level: int

    @property
    def skill_mod_bonus(self) -> Skills:
        """
        Getting skill base ability modifier for every skill
        """
        return Skills(
            **{
                skill.value: getattr(self, f'{skill.get_base_ability()[:3]}_mod')
                for skill in SkillEnum
            }
        )

    @property
    def skills(self) -> Skills:
        half_level = Skills.init_with_const(SkillEnum.sequence(), self.half_level)
        trained_skills = Skills.init_with_const(
            [
                SkillEnum[trained_skill.title.upper()]
                for trained_skill in self.trained_skills.all()  # type: ignore
            ],
            5,
        )
        race_bonus = self.race_data_instance.skill_bonuses
        mandatory_skills = self.klass_data_instance.mandatory_skills
        penalty = Skills.init_with_const(
            (
                SkillEnum.ACROBATICS,
                SkillEnum.ATHLETICS,
                SkillEnum.THIEVERY,
                SkillEnum.ENDURANCE,
                SkillEnum.STEALTH,
            ),
            value=self.armor.skill_penalty + self.shield.skill_penalty,  # type: ignore
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
    def acrobatics(self) -> int:
        """Акробатика"""
        return self.skills.acrobatics

    @property
    def arcana(self) -> int:
        """Магия"""
        return self.skills.arcana

    @property
    def athletics(self) -> int:
        """Атлетика"""
        return self.skills.athletics

    @property
    def bluff(self) -> int:
        """Обман"""
        return self.skills.bluff

    @property
    def diplomacy(self) -> int:
        """Переговоры"""
        return self.skills.diplomacy

    @property
    def dungeoneering(self) -> int:
        """Подземелья"""
        return self.skills.dungeoneering

    @property
    def endurance(self) -> int:
        """Выносливость"""
        return self.skills.endurance

    @property
    def heal(self) -> int:
        """Целительство"""
        return self.skills.heal

    @property
    def history(self) -> int:
        """История"""
        return self.skills.history

    @property
    def insight(self) -> int:
        """Проницательность"""
        return self.skills.insight

    @property
    def intimidate(self) -> int:
        """Запугивание"""
        return self.skills.intimidate

    @property
    def nature(self) -> int:
        """Природа"""
        return self.skills.nature

    @property
    def perception(self) -> int:
        """Внимательность"""
        return self.skills.perception

    @property
    def religion(self) -> int:
        """Религия"""
        return self.skills.religion

    @property
    def stealth(self) -> int:
        """Скрытность"""
        return self.skills.stealth

    @property
    def streetwise(self) -> int:
        """Знание_улиц"""
        return self.skills.streetwise

    @property
    def thievery(self) -> int:
        """Воровство"""
        return self.skills.thievery

    @property
    def skills_text(self) -> list[str]:
        result = []
        ordinary_skills = self.skill_mod_bonus + Skills.init_with_const(
            SkillEnum.sequence(), self.half_level
        )
        for skill, value in asdict(self.skills).items():
            if getattr(ordinary_skills, skill) != value:
                description = SkillEnum[
                    skill.upper()
                ].description  # type: ignore[attr-defined]
                result.append(f'{description}' f' +{value}')
        return sorted(result)
