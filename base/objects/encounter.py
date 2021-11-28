from dataclasses import dataclass


@dataclass
class EncounterLine:
    name: str
    initiative: int = 0
    ac: int = 0
    fortitude: int = 0
    reflex: int = 0
    will: int = 0
    is_player: bool = False
    number: int = 0

    @property
    def display_defences(self):
        return self.ac and self.fortitude and self.reflex and self.will

    @property
    def full_name(self):
        if self.number <= 1:
            return self.name
        return f'{self.name} №{self.number}'
