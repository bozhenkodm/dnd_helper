import os

import pytest
from django.conf import settings

from base.models import NPC

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
