import os
from dataclasses import asdict

import pytest
from django.conf import settings

from base.constants.constants import WeaponGroupEnum
from base.models import NPC, Class
from base.models.models import Race, Weapon, WeaponType
from base.objects import npc_klasses, race_classes, weapon_types_classes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }


@pytest.mark.django_db
def test_npcs_are_valid(client):
    npcs = NPC.objects.all()
    for npc in npcs:
        try:
            response = client.get(npc.url)
        except Exception as e:
            pytest.fail(f'npc: {npc}, error: {e}', pytrace=True)
        else:
            assert response.status_code == 200, npc
            assert 'POWER INCONSISTENT' not in response.content.decode()


@pytest.mark.django_db
def test_weapon_type_db_consistency():
    for wt in WeaponType.objects.all():
        assert (
            wt.handedness == weapon_types_classes[wt.slug].handedness
        ), f'{wt} has inconsistent handedness'
        assert (
            wt.category == weapon_types_classes[wt.slug].category
        ), f'{wt} has inconsistent category'
        if obj_group := getattr(weapon_types_classes[wt.slug], 'group', None):
            if isinstance(obj_group, WeaponGroupEnum):
                assert wt.group == [obj_group]
            else:
                assert wt.group == list(obj_group)
        else:
            assert not wt.group


@pytest.mark.django_db
def test_exist_non_enhanced_weapon():
    for wt in WeaponType.objects.all():
        assert Weapon.objects.filter(
            weapon_type=wt, level=0
        ).count(), f'{wt} has no weapon instance'


@pytest.mark.django_db
def test_class_db_consistency():
    for klass in Class.objects.all():
        assert set(klass.trainable_skills.values_list('title', flat=True)) == set(
            key.upper()
            for key, value in asdict(npc_klasses[klass.name].trainable_skills).items()
            if value
        ), f'{klass} has inconsistent trainable skills'


@pytest.mark.django_db
def test_race_db_consistency():
    for race in Race.objects.all():
        assert (
            race.name_display == race_classes[race.name].slug.description
        ), f'{race} has inconsistent name display'
        assert set(race.var_ability_bonus.values_list('title', flat=True)) == set(
            key.upper()
            for key, value in asdict(race_classes[race.name].var_ability_bonus).items()
            if value
        ), f'{race} has inconsistent selective ability bonuses'
        assert set(race.const_ability_bonus.values_list('title', flat=True)) == set(
            key.upper()
            for key, value in asdict(
                race_classes[race.name].const_ability_bonus
            ).items()
            if value
        ), f'{race} has inconsistent constant ability bonuses'
