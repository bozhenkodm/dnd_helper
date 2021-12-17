from enum import auto

from base.constants.base import BaseCapitalizedEnum


class PrintableObjectType(BaseCapitalizedEnum):
    ITEM = 'Магический предмет'
    AT_WILL = 'Неограниченный талант'
    ENCOUNTER = 'Талант на сцену'
    DAYLY = 'Талант на день'


class ColorsStyle(BaseCapitalizedEnum):
    RED = auto()
    BLACK = auto()
    WHITE = auto()


class Position(BaseCapitalizedEnum):
    BOTTOM_LEFT = 'bottom-left'
    TOP_LEFT = 'top-left'
    BOTTOM_RIGHT = 'bottom-right'
    TOP_RIGHT = 'top-right'
    CENTER = 'center'
