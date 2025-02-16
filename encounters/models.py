from django.utils.translation import gettext_lazy as _

from base.models.encounters import (
    Encounter as BaseEncounter,
    Party as BaseParty,
    PlayerCharacter as BasePlayerCharacter,
)


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
