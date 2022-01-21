import operator
from typing import Union

from base.constants.constants import AccessoryTypeEnum, PowersVariables
from base.objects.dice import DiceRoll
from base.objects.npc_classes import NPCClass


class PowerMixin:
    OPERATORS = {
        '+': (operator.add, 0),
        '-': (operator.sub, 0),
        '*': (operator.mul, 1),
        '/': (operator.floordiv, 1),
        '^': (max, 2),
        '_': (min, 2),
    }

    klass_data_instance: NPCClass

    @property
    def _magic_threshold(self) -> int:
        # form mypy check only
        return 0

    @property
    def _power_attrs(self):
        return {
            PowersVariables.STR: self.str_mod,
            PowersVariables.CON: self.con_mod,
            PowersVariables.DEX: self.dex_mod,
            PowersVariables.INT: self.int_mod,
            PowersVariables.WIS: self.wis_mod,
            PowersVariables.CHA: self.cha_mod,
            PowersVariables.LVL: self.level,
        }

    def calculate_token(
        self, token: str, power, weapon=None, secondary_weapon=None, item=None
    ) -> Union[int, DiceRoll]:
        if token.isdigit():
            return int(token)
        if token == PowersVariables.WPN:
            weapon = weapon or self.primary_hand  # type: ignore
            if not weapon:
                raise ValueError('У данного таланта нет оружия')
            return weapon.damage_roll.treshhold(self._magic_threshold)
        if token == PowersVariables.WPS:
            if not secondary_weapon:
                raise ValueError('У данного таланта нет дополнительного оружия')
            return secondary_weapon.damage_roll.treshhold(self._magic_threshold)
        if token == PowersVariables.ATK:
            return (
                self.klass_data_instance.attack_bonus(
                    weapon,
                    is_implement=power.accessory_type == AccessoryTypeEnum.IMPLEMENT,
                )
                # armament enchantment
                + max(
                    weapon and weapon.enchantment or 0 - self._magic_threshold,
                    0,
                )
                # power attack bonus should be added
                # to string when creating power property
            )
        if token == PowersVariables.DMG:
            # TODO separate damage bonus and enchantment
            return self.klass_data_instance.damage_bonus + max(
                (weapon and weapon.enchantment or 0) - self._magic_threshold, 0
            )
        if token == PowersVariables.EHT:
            return max((weapon and weapon.enchantment or 0) - self._magic_threshold, 0)
        if token == PowersVariables.ITL:
            if not item:
                raise ValueError('У данного таланта нет магического предмета')
            return item.level
        if token in self._power_attrs:
            return self._power_attrs[token]
        return DiceRoll.from_str(token)

    def calculate_reverse_polish_notation(
        self, expression: str, power, weapon=None, secondary_weapon=None, item=None
    ):
        """
        Проходим постфиксную запись;
        При нахождении числа, парсим его и заносим в стек;
        При нахождении бинарного оператора,
        берём два последних значения из стека в обратном порядке;
        Последнее значение, после отработки алгоритма, является решением выражения.
        """
        stack: list[Union[str, int, DiceRoll]] = []
        for token in expression.split():
            if token in self.OPERATORS:
                right, left = stack.pop(), stack.pop()
                stack.append(self.OPERATORS[token][0](left, right))  # type: ignore
            else:
                stack.append(
                    self.calculate_token(token, power, weapon, secondary_weapon, item)
                )
        return stack.pop()

    @classmethod
    def expression_to_reverse_polish_notation(cls, string: str) -> str:
        """
        Пока не все токены обработаны:

        Прочитать токен.
        Если токен — число, то добавить его в очередь вывода.
        Если токен — оператор op1, то:
            Пока присутствует на вершине стека токен оператор op2,
                    чей приоритет выше или равен приоритету op1,
                    и при равенстве приоритетов op1 является левоассоциативным:
                Переложить op2 из стека в выходную очередь;
            Положить op1 в стек.

        Если токен — открывающая скобка, то положить его в стек.
        Если токен — закрывающая скобка:
            Пока токен на вершине стека не открывающая скобка
                Переложить оператор из стека в выходную очередь.
                Если стек закончился до того,
                    как был встречен токен открывающая скобка,
                    то в выражении пропущена скобка.
            Выкинуть открывающую скобку из стека, но не добавлять в очередь вывода.
            Если токен на вершине стека — функция, переложить её в выходную очередь.

        Если больше не осталось токенов на входе:
            Пока есть токены операторы в стеке:
                Если токен оператор на вершине стека — открывающая скобка,
                    то в выражении пропущена скобка.
                Переложить оператор из стека в выходную очередь.
        Конец.
        """
        stack = []
        result = []
        operand: list[str] = []
        for char in string:
            if char in cls.OPERATORS or char in ('(', ')'):
                if operand:
                    result.append(''.join(operand))
                    operand = []
            if char == '(':
                stack.append(char)
            elif char in cls.OPERATORS:
                priority = cls.OPERATORS[char][1]
                while stack and stack[-1] in cls.OPERATORS:
                    if cls.OPERATORS[stack[-1]][1] >= priority:
                        result.append(stack.pop())
                    else:
                        break
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()
            else:
                operand.append(char)
        if operand:
            result.append(''.join(operand))

        while stack:
            result.append(stack.pop())
        return ' '.join(result)

    def evaluate(
        self, string: str, power=None, weapon=None, secondary_weapon=None, item=None
    ):
        return self.calculate_reverse_polish_notation(
            self.expression_to_reverse_polish_notation(string),
            power,
            weapon,
            secondary_weapon,
            item,
        )
