from django.utils.translation import gettext_lazy as _

from base.models.encounters import (
    Encounter as BaseEncounter,
    Monster as BaseMonster,
    Party as BaseParty,
    PlayerCharacter as BasePlayerCharacter,
)
from printer.models import Avatar as BaseAvatar, GridMap as BaseGridMap


class Encounter(BaseEncounter):
    class Meta:
        verbose_name = _('Encounter')
        verbose_name_plural = _('Encounters')
        proxy = True


class Party(BaseParty):
    class Meta:
        verbose_name = _('Party')
        verbose_name_plural = _('Parties')
        proxy = True


class PlayerCharacter(BasePlayerCharacter):
    class Meta:
        verbose_name = _('Player character')
        verbose_name_plural = _('Player characters')
        proxy = True


class Monster(BaseMonster):
    class Meta:
        verbose_name = _('Monster')
        verbose_name_plural = _('Monsters')


class Avatar(BaseAvatar):
    class Meta:
        verbose_name = _('Avatar')
        verbose_name_plural = _('Avatars')
        proxy = True


class GridMap(BaseGridMap):
    class Meta:
        verbose_name = _('Map')
        verbose_name_plural = _('Maps')
        proxy = True
