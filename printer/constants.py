from base.constants.base import BaseNameValueDescriptionEnum


class PrintableObjectType(BaseNameValueDescriptionEnum):
    ITEM = 'ITEM', 'Магический предмет'
    AT_WILL = 'AT_WILL', 'Неограниченный талант'
    ENCOUNTER = 'ENCOUNTER', 'Талант на сцену'
    DAYLY = 'DAYLY', 'Талант на день'


class ColorsStyle(BaseNameValueDescriptionEnum):
    RED = 'red', 'Red'
    BLACK = 'black', 'Black'
    WHITE = 'white', 'White'


class Position(BaseNameValueDescriptionEnum):
    BOTTOM_LEFT = 'bottom-left', 'bottom-left'
    TOP_LEFT = 'top-left', 'top-left'
    BOTTOM_RIGHT = 'bottom-right', 'bottom-right'
    TOP_RIGHT = 'top-right', 'top-right'
    CENTER = 'center', 'center'
