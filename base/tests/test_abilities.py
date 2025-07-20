from unittest.mock import Mock

import pytest

from base.objects.abilities import Abilities


def test_addition():
    abilities1 = Abilities(
        strength=10,
        constitution=12,
        dexterity=8,
        intelligence=14,
        wisdom=13,
        charisma=15,
    )
    abilities2 = Abilities(
        strength=2, constitution=1, dexterity=4, intelligence=3, wisdom=2, charisma=1
    )

    result = abilities1 + abilities2

    assert result.strength == 12
    assert result.constitution == 13
    assert result.dexterity == 12
    assert result.intelligence == 17
    assert result.wisdom == 15
    assert result.charisma == 16


def test_init_with_const():
    # Mock ability objects
    ability1 = Mock()
    ability1.name = 'strength'
    ability2 = Mock()
    ability2.name = 'dexterity'
    ability3 = Mock()
    ability3.name = 'constitution'

    # Mock QuerySet
    mock_queryset = Mock()
    mock_queryset.__iter__ = Mock(return_value=iter([ability1, ability2, ability3]))

    result = Abilities.init_with_const(mock_queryset, 15)

    assert result.strength == 15
    assert result.dexterity == 15
    assert result.constitution == 15
    assert result.intelligence == 0  # Not included in queryset
    assert result.wisdom == 0
    assert result.charisma == 0
