from base.constants.base import IntDescriptionEnum
from base.constants.constants import NPCClassEnum


class RunePriestSubclass(IntDescriptionEnum):
    WRATHFUL_HAMMER = 1, 'Мстительный молот'
    DEFIANT_WORD = 2, 'Непокорное слово'

    @staticmethod
    def npc_class():
        return NPCClassEnum.RUNEPRIEST
