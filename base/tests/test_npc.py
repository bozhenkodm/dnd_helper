import pytest


@pytest.mark.parametrize(
    ('ability', 'expected_value'),
    (
        ('strength', 12),
        ('constitution', 20),
        ('dexterity', 12),
        ('intelligence', 12),
        ('wisdom', 12),
        ('charisma', 20),
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
        ('endurance', 21),
        ('intimidate', 21),
        ('streetwise', 30),
        ('history', 17),
        ('arcana', 22),
        ('bluff', 32),
        ('diplomacy', 30),
        ('dungeoneering', 17),
        ('nature', 17),
        ('insight', 17),
        ('religion', 17),
        ('stealth', 19),
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
        ('reflex', 27),
        ('will', 31),
    ),
)
def test_dummy_defences(dummy_bard, defence, expected_value):
    assert getattr(dummy_bard, defence) == expected_value


@pytest.mark.parametrize(
    ('property', 'expected_value'),
    (
        ('max_hit_points', 170),
        ('surges', 12),
        ('_level_bonus', 0),
        ('_magic_threshold', 0),
        ('_tier', 2),
    ),
)
def test_dummy_properties(dummy_bard, property, expected_value):
    assert getattr(dummy_bard, property) == expected_value
