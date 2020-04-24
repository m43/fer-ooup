from __future__ import annotations
from abc import abstractmethod, ABC
import ast
import re


class Sheet:
    def __init__(self, rows, columns):
        if rows > 26:
            raise ValueError("row number limit is 26")

        self._rows = rows
        self._columns = columns
        self._cells = {}
        for i in range(rows):
            for j in range(columns):
                self._cells[self.refAt(i + 1, j + 1)] = Cell(0, self)

    @property
    def rows(self):
        return self.rows

    @property
    def columns(self):
        return self.columns

    @staticmethod
    def refAt(row: int, column: int):
        return chr(ord("A") + row - 1) + str(column)

    def cell(self, ref) -> Cell:
        return self._cells[ref]

    def set(self, ref, content):
        cell = self.cell(ref)
        old_refs = self.getRefsFromCell(cell)
        new_refs = self.getRefsFromExpression(content)

        cells_queue = set([self.cell(ref) for ref in new_refs])
        cells_visited = set()
        while cell not in cells_visited and cells_queue:
            current_cell = cells_queue.pop()
            if current_cell in cells_visited:
                continue

            cells_visited.add(current_cell)

            children = [self.cell(ref) for ref in self.getRefsFromCell(current_cell)]
            cells_queue.update([cell for cell in children if cell not in cells_visited])

        if cell in cells_visited:
            raise ValueError("Circular reference detected. Cannot set given content.")

        for ref in old_refs:
            self.cell(ref).detach(cell)
        for ref in new_refs:
            self.cell(ref).attach(cell)

        cell.expression = content

    @staticmethod
    def getRefsFromCell(cell):
        return Sheet.getRefsFromExpression(cell.expression)

    @staticmethod
    def getRefsFromExpression(expression):
        return re.findall("[A-Z][0-9]+", expression)

    def evaluate(self, cell: Cell):
        return self.eval_expression(cell.expression)

    def eval_expression(self, exp):
        def _eval(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Name):
                return self.cell(node.id).value
            elif isinstance(node, ast.BinOp):
                return _eval(node.left) + _eval(node.right)
            else:
                raise Exception('Unsupported type {}'.format(node))

        ast_node = ast.parse(exp, mode='eval')
        return _eval(ast_node.body)

    def prettyPrint(self):
        for i in range(self._rows):
            for j in range(self._columns):
                ref = self.refAt(i + 1, j + 1)
                print("{}={}={} ".format(ref, self.cell(ref).expression, self.cell(ref).value), end="")
            print()
        print()


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def detachAll(self):
        pass

    @abstractmethod
    def notify(self):
        pass


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


class Cell(Subject, Observer):
    def __init__(self, initial_value, sheet: Sheet):
        self._sheet = sheet
        self._value = initial_value
        self._exp = str(initial_value)
        self._observers = set()

    @property
    def value(self):
        return self._value

    @property
    def expression(self):
        return self._exp

    @expression.setter
    def expression(self, exp):
        self._exp = exp
        self.evaluate()

    def evaluate(self) -> None:
        self._value = self._sheet.evaluate(self)
        self.notify()

    def attach(self, observer: Observer):
        self._observers.add(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def detachAll(self):
        self._observers.clear()

    def notify(self):
        for o in self._observers:
            o.update()

    def update(self):
        self.evaluate()
