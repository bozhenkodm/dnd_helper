from unittest.mock import Mock

from base.objects.skills import Skills


def test_default_initialization():
    skills = Skills()
    assert skills.acrobatics == 0
    assert skills.athletics == 0
    assert skills.perception == 0
    assert skills.thievery == 0
    assert skills.endurance == 0
    assert skills.intimidate == 0
    assert skills.streetwise == 0
    assert skills.history == 0
    assert skills.arcana == 0
    assert skills.bluff == 0
    assert skills.diplomacy == 0
    assert skills.dungeoneering == 0
    assert skills.nature == 0
    assert skills.insight == 0
    assert skills.religion == 0
    assert skills.stealth == 0
    assert skills.heal == 0


def test_custom_initialization():
    skills = Skills(
        acrobatics=15,
        athletics=12,
        perception=18,
        thievery=10,
        endurance=14,
        intimidate=16,
    )
    assert skills.acrobatics == 15
    assert skills.athletics == 12
    assert skills.perception == 18
    assert skills.thievery == 10
    assert skills.endurance == 14
    assert skills.intimidate == 16


def test_addition():
    skills1 = Skills(acrobatics=10, athletics=12, perception=8)
    skills2 = Skills(acrobatics=5, athletics=3, perception=7)

    result = skills1 + skills2

    assert result.acrobatics == 15
    assert result.athletics == 15
    assert result.perception == 15


def test_subtraction():
    skills1 = Skills(acrobatics=15, athletics=12, perception=20)
    skills2 = Skills(acrobatics=5, athletics=2, perception=5)

    result = skills1 - skills2

    assert result.acrobatics == 10
    assert result.athletics == 10
    assert result.perception == 15


def test_max_classmethod():
    skills1 = Skills(acrobatics=10, athletics=15, perception=8)
    skills2 = Skills(acrobatics=12, athletics=10, perception=20)
    skills3 = Skills(acrobatics=8, athletics=20, perception=15)

    result = Skills.max(skills1, skills2, skills3)

    assert result.acrobatics == 12  # max from skills2
    assert result.athletics == 20  # max from skills3
    assert result.perception == 20  # max from skills2


def test_init_with_const():
    # Mock skill objects
    skill1 = Mock()
    skill1.name = 'acrobatics'
    skill2 = Mock()
    skill2.name = 'athletics'
    skill3 = Mock()
    skill3.name = 'perception'

    # Mock QuerySet
    mock_queryset = Mock()
    mock_queryset.__iter__ = Mock(return_value=iter([skill1, skill2, skill3]))

    result = Skills.init_with_const(mock_queryset, 15)

    assert result.acrobatics == 15
    assert result.athletics == 15
    assert result.perception == 15
    assert result.thievery == 0  # Not included in queryset
