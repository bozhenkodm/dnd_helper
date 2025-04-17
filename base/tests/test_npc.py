import pytest


@pytest.mark.parametrize(
    ('ability', 'expected_value'),
    (
        ('strength', 12),
        ('constitution', 18),
        ('dexterity', 12),
        ('intelligence', 12),
        ('wisdom', 12),
        ('charisma', 18),
    ),
)
def test_dummy_abilities(dummy_bard, ability, expected_value):
    assert getattr(dummy_bard, ability) == expected_value


@pytest.mark.parametrize(
    ('skill', 'expected_value'),
    (
        ('acrobatics', 26),
        ('athletics', 17),
        ('perception', 17),
        ('thievery', 17),
        ('endurance', 20),
        ('intimidate', 20),
        ('streetwise', 29),
        ('history', 17),
        ('arcana', 22),
        ('bluff', 29),
        ('diplomacy', 29),
        ('dungeoneering', 17),
        ('nature', 17),
        ('insight', 17),
        ('religion', 17),
        ('stealth', 17),
        ('heal', 17),
    ),
)
def test_dummy_skills(dummy_bard, skill, expected_value):
    assert getattr(dummy_bard, skill) == expected_value


@pytest.mark.parametrize(
    ('defence', 'expected_value'),
    (
        ('armor_class', 26),
        ('fortitude', 30),
        ('reflex', 28),
        ('will', 31),
    ),
)
def test_dummy_defences(dummy_bard, defence, expected_value):
    assert getattr(dummy_bard, defence) == expected_value
