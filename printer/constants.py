from PIL.Image import Transpose

from base.constants.base import BaseNameValueDescriptionEnum, IntDescriptionEnum


class PrintableObjectType(BaseNameValueDescriptionEnum):
    ITEM = 'ITEM', 'Магический предмет'
    AT_WILL = 'AT_WILL', 'Неограниченный талант'
    ENCOUNTER = 'ENCOUNTER', 'Талант на сцену'
    DAILY = 'DAILY', 'Талант на день'


class ColorStyle(BaseNameValueDescriptionEnum):
    NONE = 'none', 'Пусто'
    RED = 'red', 'Красный'
    BLACK = 'black', 'Чёрный'
    WHITE = 'white', 'Белый'
    GREEN = 'green', 'Зелёный'
    GRAY = 'gray', 'Серый'


class TransponseAction(IntDescriptionEnum):
    FLIP_LEFT_RIGHT = Transpose.FLIP_LEFT_RIGHT, 'Развернуть слева направо'
    FLIP_TOP_BOTTOM = Transpose.FLIP_TOP_BOTTOM, 'Развернуть сверху вниз'
    ROTATE_90 = Transpose.ROTATE_90, 'Повернуть на 90°'
    ROTATE_180 = Transpose.ROTATE_180, 'Повернуть на 180°'
    ROTATE_270 = Transpose.ROTATE_270, 'Повернуть на 270°'
