import pytest

_ABILITY_EXPECTATIONS = (
    ('strength', 12),
    ('constitution', 20),
    ('dexterity', 12),
    ('intelligence', 12),
    ('wisdom', 12),
    ('charisma', 20),
)

_SKILL_EXPECTATIONS = (
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
)

_DEFENCE_EXPECTATIONS = (
    ('armor_class', 26),
    ('fortitude', 30),
    ('reflex', 27),
    ('will', 31),
)

_PROPERTY_EXPECTATIONS = (
    ('max_hit_points', 170),
    ('surges', 12),
    ('_level_bonus', 0),
    ('_magic_threshold', 0),
    ('_tier', 2),
)


def _params(category, expectations):
    return [
        pytest.param(attr, value, id=f'{category}-{attr}')
        for attr, value in expectations
    ]


@pytest.mark.parametrize(
    ('attr', 'expected_value'),
    [
        *_params('ability', _ABILITY_EXPECTATIONS),
        *_params('skill', _SKILL_EXPECTATIONS),
        *_params('defence', _DEFENCE_EXPECTATIONS),
        *_params('property', _PROPERTY_EXPECTATIONS),
    ],
)
def test_dummy_attributes(dummy_tiefling_bard, attr, expected_value):
    assert getattr(dummy_tiefling_bard, attr) == expected_value
