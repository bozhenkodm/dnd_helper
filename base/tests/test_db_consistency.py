import pytest

from base.models.items import Weapon, WeaponType
from base.models.models import NPC
from base.models.powers import PowerProperty


@pytest.mark.django_db
def test_power_properties_are_valid():
    assert not PowerProperty.objects.filter(description__contains='None').exists()


@pytest.mark.skip
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
        # try:
        #     response = client.get(
        #         reverse('admin:base_npc_change', kwargs={'object_id': npc.pk})
        #     )
        # except Exception as e:
        #     pytest.fail(f'admin site npc: {npc}, error: {e}', pytrace=True)
        # else:
        #     assert response.status_code < 400, f'admin site: {npc}'


@pytest.mark.django_db
def test_exist_non_enhanced_weapon():
    for wt in WeaponType.objects.all():
        assert Weapon.objects.filter(
            weapon_type=wt, level=0
        ).exists(), f'{wt} has no weapon instance'
