from base.constants.base import BaseNameValueDescriptionEnum


class PrintableObjectType(BaseNameValueDescriptionEnum):
    ITEM = 'ITEM', 'Магический предмет'
    AT_WILL = 'AT_WILL', 'Неограниченный талант'
    ENCOUNTER = 'ENCOUNTER', 'Талант на сцену'
    DAYLY = 'DAYLY', 'Талант на день'


class ColorsStyle(BaseNameValueDescriptionEnum):
    RED = 'red', 'Красный'
    BLACK = 'black', 'Чёрный'
    WHITE = 'white', 'Белый'


class Position(BaseNameValueDescriptionEnum):
    BOTTOM_LEFT = 'bottom-left', 'Внизу слева'
    TOP_LEFT = 'top-left', 'Вверху слева'
    BOTTOM_RIGHT = 'bottom-right', 'Внизу справа'
    TOP_RIGHT = 'top-right', 'Вверху справа'
    CENTER = 'center', 'По центру'
