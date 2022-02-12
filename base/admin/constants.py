from base.constants.base import BaseNameValueDescriptionEnum


class ResistItemBonusEnum(BaseNameValueDescriptionEnum):
    ACID = 'acid', 'Кислота'
    COLD = 'cold', 'Холод'
    FIRE = 'fire', 'Огонь'
    LIGHTNING = 'lightning', 'Электричество'
    NECROTIC = 'necrotic', 'Некротическая энергия'
    POISON = 'poison', 'Яд'
    PSYCHIC = 'psychic', 'Психическая энергия'
    RADIANT = 'radiant', 'Излучение'
    THUNDER = 'thunder', 'Звук'
    FORCE = 'force', 'Силовое поле'


class SaveItemBonusEnum(BaseNameValueDescriptionEnum):
    CHARM = 'charm', 'Очарование'
    CONJURATION = 'conjuration', 'Иллюзия'
    FEAR = 'fear', 'Страх'
    SLEEP = 'sleep', 'Сон'
    ACID = 'acid', 'Кислота'
    COLS = 'cols', 'Холод'
    FIRE = 'fire', 'Огонь'
    LIGHTNING = 'lightning', 'Электричество'
    NECROTIC = 'necrotic', 'Некротическая энергия'
    POISON = 'poison', 'Яд'
    SLOW = 'slow', 'Замедление'
    IMMOBILIZED = 'immobilized', 'Обездвиживание'
    RESTRAINED = 'restrained', 'Удерживание'
    DAMAGE = 'damage', 'Урон'
