import pytest

from base.constants.constants import LEVELS_WITH_ABILITY_BONUS, SexEnum
from base.models.abilities import AbilityLevelBonus
from base.models.models import NPC
from base.models.skills import Skill


@pytest.fixture(scope='session')
def django_db_setup():
    # Reuse the existing db.sqlite3 instead of creating an empty test DB:
    # the NPC fixture below depends on rows (races, classes, subclasses, weapons)
    # that the project does not ship as test fixtures. @pytest.mark.django_db wraps
    # each test in a transaction that is rolled back, so no data is persisted.
    pass


@pytest.fixture(scope='function')
def dummy_tiefling_bard(db) -> NPC:
    bard = NPC(
        name='dummy_bard',
        race_id=6,
        klass_id=11,
        subclass_id=1,
        sex=SexEnum.M,
        level=30,
        is_bonus_applied=False,
        primary_hand_id=2,
        secondary_hand_id=None,
        base_strength=10,
        base_constitution=10,
        base_dexterity=10,
        base_intelligence=10,
        base_wisdom=10,
        base_charisma=10,
        var_bonus_ability_id=2,
    )
    bard.save()
    albs = [
        AbilityLevelBonus(ability_id=6, npc=bard, level=lvl)
        for lvl in LEVELS_WITH_ABILITY_BONUS
    ] + [
        AbilityLevelBonus(ability_id=2, npc=bard, level=lvl)
        for lvl in LEVELS_WITH_ABILITY_BONUS
    ]
    AbilityLevelBonus.objects.bulk_create(albs)
    bard.trained_skills.add(*Skill.objects.filter(id__in=(1, 7, 10, 11)))
    return bard
