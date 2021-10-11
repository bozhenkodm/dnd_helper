from base.constants.base import IntDescriptionSubclassEnum
from base.constants.constants import NPCClassIntEnum


class FighterSubclass(IntDescriptionSubclassEnum):
    GREAT_WEAPON = 1, 'Воин с большим оружием'
    GUARDIAN = 2, 'Воин защитник'
    BATTLERAGER = 3, 'Неистовый воин'
    TEMPPEST = 4, 'Воин вихрь'
    BRAWLER = 5, 'Воин задира'


class RogueSubclass(IntDescriptionSubclassEnum):
    DODGER = 1, 'Мастер уклонения'
    SCOUNDREL = 2, 'Жестокий головорез'
    RUFFAIN = 3, 'Верзила'
    SNEAK = 4, 'Скрытник'


class RunePriestSubclass(IntDescriptionSubclassEnum):
    WRATHFUL_HAMMER = 1, 'Мстительный молот'
    DEFIANT_WORD = 2, 'Непокорное слово'


class SorcererSubclass(IntDescriptionSubclassEnum):
    DRAGON_MAGIC = 1, 'Драконья магия'
    WILD_MAGIC = 2, 'Дикая магия'


class SeekerSubclass(IntDescriptionSubclassEnum):
    SPIRITBOND = 1, 'Духовная связь'
    BLOODBOND = 2, 'Кровавая связь'


class WardenSubclass(IntDescriptionSubclassEnum):
    EARTHSTRENGTH = 1, 'Сила земли'
    WILDBLOOD = 2, 'Дикая кровь'


SUBCLASSES = {
    NPCClassIntEnum.FIGHTER: FighterSubclass,
    NPCClassIntEnum.ROGUE: RogueSubclass,
    NPCClassIntEnum.RUNEPRIEST: RunePriestSubclass,
    NPCClassIntEnum.SEEKER: SeekerSubclass,
    NPCClassIntEnum.SORCERER: SorcererSubclass,
    NPCClassIntEnum.WARDEN: WardenSubclass,
}
