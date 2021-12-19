from base.constants.base import BaseNameValueDescriptionEnum


class PrintableObjectType(BaseNameValueDescriptionEnum):
    ITEM = 'ITEM', 'Магический предмет'
    AT_WILL = 'AT_WILL', 'Неограниченный талант'
    ENCOUNTER = 'ENCOUNTER', 'Талант на сцену'
    DAYLY = 'DAYLY', 'Талант на день'


class ColorsStyle(BaseNameValueDescriptionEnum):
    RED = 'RED', 'Red'
    BLACK = 'BLACK', 'Black'
    WHITE = 'WHITE', 'White'


class Position(BaseNameValueDescriptionEnum):
    BOTTOM_LEFT = 'BOTTOM_LEFT', 'bottom-left'
    TOP_LEFT = 'TOP_LEFT', 'top-left'
    BOTTOM_RIGHT = 'BOTTOM_RIGHT', 'bottom-right'
    TOP_RIGHT = 'TOP_RIGHT', 'top-right'
    CENTER = 'CENTER', 'center'
