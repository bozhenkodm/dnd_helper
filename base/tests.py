import pytest
from django.conf import settings
from django.urls import reverse

from base.constants.constants import WeaponGroupEnum
from base.models import NPC, Class
from base.models.models import Weapon, WeaponType
from base.objects import npc_klasses, weapon_types_classes


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db_test.sqlite3',
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
        try:
            response = client.get(
                reverse('admin:base_npc_change', kwargs={'object_id': npc.pk})
            )
        except Exception as e:
            pytest.fail(f'admin site npc: {npc}, error: {e}', pytrace=True)
        else:
            assert response.status_code < 400, f'admin site: {npc}'


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
        assert klass.name_display == npc_klasses[klass.name].slug.description
