import pytest

from base.constants.constants import DiceIntEnum
from base.objects.dice import DiceRoll


def test_str_representation_without_addendant():
    dice_roll = DiceRoll(rolls=2, dice=DiceIntEnum.D6, addendant=0)
    assert str(dice_roll) == '2k6'


def test_str_representation_with_addendant():
    dice_roll = DiceRoll(rolls=1, dice=DiceIntEnum.D8, addendant=5)
    assert str(dice_roll) == '1k8+5'


def test_add_int():
    dice_roll = DiceRoll(rolls=1, dice=DiceIntEnum.D6, addendant=2)
    result = dice_roll + 3
    assert result.rolls == 1
    assert result.dice == DiceIntEnum.D6
    assert result.addendant == 5


def test_radd_int():
    dice_roll = DiceRoll(rolls=1, dice=DiceIntEnum.D6, addendant=2)
    result = 3 + dice_roll
    assert result.rolls == 1
    assert result.dice == DiceIntEnum.D6
    assert result.addendant == 5


def test_add_invalid_type():
    dice_roll = DiceRoll(rolls=1, dice=DiceIntEnum.D6, addendant=0)
    with pytest.raises(TypeError, match='should add only ints to dice rolls'):
        dice_roll + 'invalid'


def test_multiply_int():
    dice_roll = DiceRoll(rolls=2, dice=DiceIntEnum.D6, addendant=3)
    result = dice_roll * 2
    assert result.rolls == 4
    assert result.dice == DiceIntEnum.D6
    assert result.addendant == 3


def test_rmul_int():
    dice_roll = DiceRoll(rolls=2, dice=DiceIntEnum.D6, addendant=3)
    result = 2 * dice_roll
    assert result.rolls == 4
    assert result.dice == DiceIntEnum.D6
    assert result.addendant == 3


def test_imul_int():
    dice_roll = DiceRoll(rolls=2, dice=DiceIntEnum.D6, addendant=3)
    dice_roll *= 2
    assert dice_roll.rolls == 4
    assert dice_roll.dice == DiceIntEnum.D6
    assert dice_roll.addendant == 3


def test_multiply_invalid_type():
    dice_roll = DiceRoll(rolls=1, dice=DiceIntEnum.D6, addendant=0)
    with pytest.raises(TypeError, match='should multiply only by int'):
        dice_roll * 'invalid'


def test_threshold_reduces_addendant():
    dice_roll = DiceRoll(rolls=1, dice=DiceIntEnum.D6, addendant=5)
    result = dice_roll.threshold(3)
    assert result.addendant == 2


def test_threshold_minimum_zero():
    dice_roll = DiceRoll(rolls=1, dice=DiceIntEnum.D6, addendant=2)
    result = dice_roll.threshold(5)
    assert result.addendant == 0


@pytest.mark.parametrize(
    ('input_str', 'expected_rolls', 'expected_dice', 'expected_addendant'),
    (
        ('2d6', 2, DiceIntEnum.D6, 0),
        ('1d8+3', 1, DiceIntEnum.D8, 3),
        ('d20', 0, DiceIntEnum.D20, 0),
        ('3к4+10', 3, DiceIntEnum.D4, 10),
        ('2д12+5', 2, DiceIntEnum.D12, 5),
        ('1k10+1', 1, DiceIntEnum.D10, 1),
    ),
)
def test_from_str_valid_formats(
    input_str, expected_rolls, expected_dice, expected_addendant
):
    result = DiceRoll.from_str(input_str)
    assert result.rolls == expected_rolls
    assert result.dice == expected_dice
    assert result.addendant == expected_addendant


def test_from_str_invalid_format():
    with pytest.raises(ValueError, match='Not valid DiceRoll'):
        DiceRoll.from_str('invalid_format')


def test_roll_returns_int():
    dice_roll = DiceRoll(rolls=1, dice=DiceIntEnum.D6, addendant=5)
    result = dice_roll.roll()
    assert isinstance(result, int)
    assert 6 <= result <= 11  # 1-6 from dice + 5 addendant
