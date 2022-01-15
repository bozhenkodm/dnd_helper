import operator
import re


def modifier(value: int) -> int:
    return (value - 10) // 2


class ReversePolishRecord:
    OPERATORS = {
        '+': (operator.add, 0),
        '-': (operator.sub, 0),
        '*': (operator.mul, 1),
        '/': (operator.floordiv, 1),
        '^': (max, 2),
        '_': (min, 2),
    }

    @classmethod
    def polska(cls, srt):
        """
        Проходим постфиксную запись;
        При нахождении числа, парсим его и заносим в стек;
        При нахождении бинарного оператора, берём два последних значения из стека в обратном порядке;
        При нахождении унарного оператора, в данном случае - унарного минуса, берём последнее значение из стека и вычитаем его из нуля, так как унарный минус является правосторонним оператором;
        Последнее значение, после отработки алгоритма, является решением выражения.
        """

    @classmethod
    def rpn(cls, expression: str):
        stack = []
        print(expression)
        for token in expression.split():
            if token in cls.OPERATORS:
                right, left = stack.pop(), stack.pop()
                stack.append(cls.OPERATORS[token][0](left, right))
            else:
                stack.append(int(token))
        return stack.pop()


    @classmethod
    def expression_to_polish_record(cls, string: str) -> str:
        """
    Пока не все токены обработаны:

        Прочитать токен.
        Если токен — число, то добавить его в очередь вывода.
        Если токен — оператор op1, то:
            Пока присутствует на вершине стека токен оператор op2, чей приоритет выше или равен приоритету op1,
                    и при равенстве приоритетов op1 является левоассоциативным:
                Переложить op2 из стека в выходную очередь;
            Положить op1 в стек.

        Если токен — открывающая скобка, то положить его в стек.
        Если токен — закрывающая скобка:
            Пока токен на вершине стека не открывающая скобка
                Переложить оператор из стека в выходную очередь.
                Если стек закончился до того, как был встречен токен открывающая скобка, то в выражении пропущена скобка.
            Выкинуть открывающую скобку из стека, но не добавлять в очередь вывода.
            Если токен на вершине стека — функция, переложить её в выходную очередь.

    Если больше не осталось токенов на входе:
        Пока есть токены операторы в стеке:
            Если токен оператор на вершине стека — открывающая скобка, то в выражении пропущена скобка.
            Переложить оператор из стека в выходную очередь.
    Конец.
        """
        stack = []
        result = []
        operand = []
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
        print(result)
        return ' '.join(result)

    @classmethod
    def evaluate(cls, string):
        return cls.rpn(cls.expression_to_polish_record(string))
        # return cls.polska(cls.expression_to_polish_record(string).split())

# print(ReversePolishRecord.expression_to_polish_record('2+2*3+5'))

# print(ReversePolishRecord.evaluate('2+2*3+5'))
# print(ReversePolishRecord.evaluate('(2+10)*2+30'))
print(ReversePolishRecord.evaluate('(2+10)*2^30'))