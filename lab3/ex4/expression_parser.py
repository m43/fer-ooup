# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Component(ABC):
    def __str__(self):
        return self.__repr__()

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def evaluate(self, symbols) -> int:
        pass


class Composit(Component):
    def __init__(self, left: Component, operation: str, right: Component):
        self._left = left
        self._right = right
        self._op = operation

    def __repr__(self):
        return "({}){}({})".format(self._left, self._op, self._right)

    def evaluate(self, symbols):
        return eval(str(self._left.evaluate(symbols)) + self._op + str(self._right.evaluate(symbols)))


class Leaf(Component):

    def __init__(self, value: str):
        self._value = value

    def __repr__(self):
        return self._value

    def evaluate(self, symbols):
        try:
            return float(self._value)
        except:
            return symbols.get(self._value)


def parse_expression(expression) -> Component:
    # adapted from  http://news.ycombinator.com/item?id=284842
    for operator in ["+-", "*/"]:
        depth = 0
        for p in range(len(expression) - 1, -1, -1):
            if expression[p] == ')':
                depth += 1
            elif expression[p] == '(':
                depth -= 1
            elif depth == 0 and expression[p] in operator:
                # strinput is a compound expression
                return Composit(parse_expression(expression[:p]), expression[p], parse_expression(expression[p + 1:]))
    expression = expression.strip()
    if expression[0] == '(':
        # strinput is a parenthesized expression?
        return parse_expression(expression[1:-1])
    # strinput is an atom!
    return Leaf(expression)


if __name__ == '__main__':
    symbols_dict = {}
    tree = parse_expression("6*(x+4)/2-3-x")
    print(tree)
    # ((((6.0 * (x + 4.0)) / 2.0) - 3.0) - x)

    # print(tree.evaluate(symbols_dict))  # should not work cause x is unknown!

    symbols_dict['x'] = 5
    print(tree.evaluate(symbols_dict))
    # 19.0

    symbols_dict['x'] = 4
    print(tree.evaluate(symbols_dict))
    # 17.0
