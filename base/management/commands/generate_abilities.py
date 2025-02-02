from enum import Enum
from random import randint

from django.core.management import BaseCommand


def d6():
    return randint(1, 6)


def roll():
    r = [d6() for _ in range(4)]
    return sum(r) - min(r)


class Kind(str, Enum):
    DUMMY = 'dummy'
    AVERAGE = 'average'
    GENIUS = 'genius'
    MINIMAX = 'minimax'


def average_exit(rolls: list[int]) -> bool:
    return True


def dummy_exit(rolls: list[int]) -> bool:
    return min(rolls) <= 7 and max(rolls) <= 15


def genious_exit(rolls: list[int]) -> bool:
    return max(rolls) == 18 and min(rolls) > 8


def minimax_exit(rolls: list[int]) -> bool:
    return max(rolls) == 18 and min(rolls) <= 8


class Command(BaseCommand):
    help = 'Generate random abilities'

    def add_arguments(self, parser):
        parser.add_argument('--kind', type=Kind)

    def handle(self, *args, **options):
        kind = options.get('kind', Kind.AVERAGE)
        if kind == Kind.GENIUS:
            exit_func = genious_exit
        elif kind == Kind.DUMMY:
            exit_func = dummy_exit
        elif kind == Kind.MINIMAX:
            exit_func = minimax_exit
        else:
            exit_func = average_exit
        while True:
            rolls = [roll() for _ in range(6)]
            if exit_func(rolls):
                break

        self.stdout.write(self.style.SUCCESS(', '.join(str(r) for r in sorted(rolls))))
