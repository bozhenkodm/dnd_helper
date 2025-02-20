from dataclasses import asdict

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.constants.constants import NPCClassEnum, SkillEnum
from base.managers import SkillQuerySet
from base.models.abilities import Ability
from base.objects.skills import Skills


class Skill(models.Model):
    objects = SkillQuerySet.as_manager()

    title = models.CharField(
        choices=SkillEnum.generate_choices(),
        max_length=SkillEnum.max_length(),
        unique=True,
    )
    based_on = models.ForeignKey(Ability, on_delete=models.CASCADE)
    is_penalty_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.get_title_display()


class NPCSkillAbstract(models.Model):
    class Meta:
        abstract = True

    half_level: int

    trained_skills = models.ManyToManyField(
        Skill, verbose_name=_('Trained skills'), blank=True
    )

    @property
    def all_trained_skills(self) -> list[SkillEnum]:
        return [
            SkillEnum(skill.title)  # type: ignore
            for skill in self.klass.mandatory_skills.all()
        ] + [
            SkillEnum(skill.title)  # type: ignore
            for skill in self.trained_skills.all()
        ]

    @property
    def skill_mod_bonus(self) -> Skills:
        """
        Getting skill base ability modifier for every skill
        """
        return Skills(
            **{
                skill.title.lower(): getattr(self, skill.based_on.mod)
                for skill in Skill.objects.all()
            }
        )

    @property
    def skills(self) -> Skills:
        half_level = Skills.init_with_const(*SkillEnum, value=self.half_level)
        trained_skills = Skills.init_with_const(
            *[
                SkillEnum[trained_skill.title]
                for trained_skill in self.trained_skills.all()  # type: ignore
            ],
            value=5,
        )
        if self.klass.name == NPCClassEnum.BARD:
            # TODO figure out how to move this logic to common bonus logic
            trained_skills += Skills.max(
                trained_skills,
                Skills.init_with_const(*SkillEnum, value=1),
            )

        bonus_skills = Skills(
            **{k.lower(): v for k, v in self.calculate_bonuses(*SkillEnum).items()}
        )
        mandatory_skills = self.klass.mandatory_skills.obj(value=5)
        armor_skill_penalty = (
            self.armor.skill_penalty if self.armor else 0  # type: ignore
        )
        shield_skill_penalty = (
            self.arms_slot.skill_penalty if self.arms_slot else 0  # type: ignore
        )
        penalty = Skills.init_with_const(
            *(
                SkillEnum[s]
                for s in Skill.objects.filter(is_penalty_applied=True).values_list(
                    'title', flat=True
                )
            ),
            value=armor_skill_penalty + shield_skill_penalty,
        )
        return (
            half_level
            + trained_skills
            + mandatory_skills
            + bonus_skills
            + penalty
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
            *SkillEnum, value=self.half_level
        )
        for skill, value in asdict(self.skills).items():
            if getattr(ordinary_skills, skill) != value:
                description = SkillEnum[skill.upper()].description
                result.append(f'{description}' f' +{value}')
        return sorted(result)
