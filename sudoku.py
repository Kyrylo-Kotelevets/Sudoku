from random import randint, random
from math import sqrt, log10, ceil
import copy


class sudoku(object):
    '''
    '''

    MIN_LEVEL, MAX_LEVEL = 10, 62  # Минимально и максимально возможные уровни
    UNASSIGNED = 0

    def __init__(self, puzzle: list):
        if not sudoku.is_valid(puzzle):
            raise Exception('Invalid sudoku')

        self.n = int(sqrt(len(puzzle)))
        self.size = self.n ** 2
        self.puzzle = copy.deepcopy(puzzle)

    def __getitem__(self, keys: tuple) -> int:
        ''' Возвращает число в клетке с заданными координатами '''
        if len(keys) != 2:
            raise IndexError(f"Invalid amount of indexes: {len(keys)}, must be 2")

        row, col = keys
        if not isinstance(row, int) or not isinstance(col, int):
            raise IndexError(f"Indexes must be whole numbers {keys}")
        elif col < 0 or col > self.size - 1:
            raise IndexError(f"Index {col} out of range")
        elif row < 0 or row > self.size - 1:
            raise IndexError(f"Index {row} out of range")
        else:
            return self.puzzle[row][col]

    def __setitem__(self, keys: tuple, value: int):
        ''' Заменяет число в клетке с заданными координатами на заданное '''
        if len(keys) != 2:
            raise IndexError(f"Invalid amount of indexes: {len(keys)}, must be 2")

        row, col = keys
        if not isinstance(row, int) or not isinstance(col, int):
            raise IndexError(f"Indexes must be whole numbers {keys}")
        elif col < 0 or col > self.size - 1:
            raise IndexError(f"Index {col} out of range")
        elif row < 0 or row > self.size - 1:
            raise IndexError(f"Index {row} out of range")
        elif not isinstance(value, int) or value < 0 or value > self.size:
            raise ArgumentError(f"Invalid value {value} for sudoku with size {self.size}")
        else:
            self.puzzle[row][col] = value

    def copy(self):
        ''' Возвращает копию судоку '''
        return sudoku(copy.deepcopy(self.puzzle))

    @staticmethod
    def empty(size: int) -> list:
        ''' Возвращает пустое судоку заданного размера '''
        return sudoku([[sudoku.UNASSIGNED] * (size ** 2) for row in range(size ** 2)])

    @staticmethod
    def trivial(size: int) -> list:
        ''' Возвращает тривиально заполненное судоку '''
        base = [num + 1 for num in range(size ** 2)]  # Базовый абор чисел
        puzzle = []

        for i in range(size):
            for j in range(size):
                #  Сдвигаем базовый набор чисел и складываем его части
                puzzle.append(base[i + j * size:] + base[:i + j * size])

        return sudoku(puzzle)

    def is_solved(self) -> bool:
        # Проверяем на факт того, что все клетки заполнены
        return all(num != sudoku.UNASSIGNED for row in self.puzzle for num in row)

    def are_equal(self, initial) -> bool:
        ''' Сравнивает решенное судоку с начальным'''
        if self.size != initial.size:
            return False

        for i in range(self.size):
            for j in range(self.size):
                # Если начальная клетка не была пуста и она не совпадает с решением
                if initial.puzzle[i][j] != sudoku.UNASSIGNED and \
                   self.puzzle[i][j] != initial.puzzle[i][j]:
                    return False
        return True

    @staticmethod
    def is_valid(puzzle: list):
        ''' Валидация судоку '''

        n = int(sqrt(len(puzzle)))  # Размер блока
        if n ** 2 != len(puzzle):  # Если размер блока не корень
            return False

        for i in range(n ** 2):
            # Если длина строки не соответсвует размеру
            if len(puzzle[i]) != n ** 2:
                return False

            for j in range(n ** 2):
                # Если клетка не заполнена
                if puzzle[i][j] == sudoku.UNASSIGNED:
                    continue

                # Если в клетке не число
                if not isinstance(puzzle[i][j], int):
                    return False

                # Если число вне интервала
                if puzzle[i][j] < 1 or puzzle[i][j] > n ** 2:
                    return False

                for k in range(n ** 2):
                    # Если есть повтор в строке
                    if puzzle[i][k] == puzzle[i][j] and k != j:
                        return False
                    # Если есть повтор в столбце
                    if puzzle[k][j] == puzzle[i][j] and k != i:
                        return False

                # Координаты начала блока
                row = n * (i // n)
                col = n * (j // n)
                for r in range(row, row + n):
                    for c in range(col, col + n):
                        # Если есть повтор в блоке
                        if puzzle[r][c] == puzzle[i][j] and (r != i or c != j):
                            return False
        return True

    def solution(self):
        def solveHelper(solution: list, n: int) -> bool:
            ''' Рекурсивная сборочная функция (бектрекинг) '''

            MIN = None  # Индекс минимального множества вставок
            # Пока можем вставлять одиночки
            while True:
                MIN = None
                for row in range(n ** 2):
                    for col in range(n ** 2):
                        # Если клетка пуста, то продолжаем
                        if solution[row][col] != sudoku.UNASSIGNED:
                            continue

                        # Получаем множество вставок для клетки
                        possible = sudoku.get_possible(solution, row, col, n)
                        # Размер множества вставок
                        count = len(possible)

                        if count == 0:  # Вставок нет, текущее состояние нерешаемо
                            return False
                        if count == 1:  # Попалась одиночка
                            solution[row][col] = possible.pop()
                        if not MIN or count < len(MIN[1]):  # Улучшаем минимальное мн-во
                            MIN = ((row, col), possible)

                # Если множество пусто, то судоку собрано
                if not MIN:
                    return True
                # Если больше нет однозначных чисел для вставки
                elif len(MIN[1]) > 1:
                    break

            # Координаты клетки с минимальным мн-вом вставок
            r, c = MIN[0]

            # Перебираем все вставки
            for v in MIN[1]:
                solutionCopy = copy.deepcopy(solution)  # Сохраняем копию текущего состояния
                solutionCopy[r][c] = v
                if solveHelper(solutionCopy, n):  # Если рекурсивный поиск был удачным
                    for r in range(n ** 2):
                        for c in range(n ** 2):
                            solution[r][c] = solutionCopy[r][c]
                    return True
            return False

        # Копируем исходное судоку
        solution = copy.deepcopy(self.puzzle)
        if solveHelper(solution, self.n):
            return sudoku(solution)

    def n_solutions(self) -> int:
        # Мат. аппарат для пересчёта решений
        def num_of_solutions(solution: list, n: int=3) -> int:
            ''' Рекурсивная сборочная функция (бектрекинг) '''

            MIN = None  # Индекс минимального множества вставок
            # Пока можем вставлять одиночки
            while True:
                MIN = None
                for row in range(n ** 2):
                    for col in range(n ** 2):
                        # Если клетка пуста, то продолжаем
                        if solution[row][col] != sudoku.UNASSIGNED:
                            continue

                        # Получаем множество вставок для клетки
                        possible = sudoku.get_possible(solution, row, col, n)
                        # Размер множества вставок
                        size = len(possible)

                        
                        if size == 0:  # Множество пусто, решений нет
                            return 0
                        if size == 1:  # Однозначная вставка
                            solution[row][col] = possible.pop()
                        if not MIN or size < len(MIN[1]):  # Улучшаем минимальное мн-во
                            MIN = ((row, col), possible)

                # Если множество пусто, то судоку собрано
                if MIN is None:
                    return 1

                # Если больше нет однозначных вставок
                elif len(MIN[1]) > 1:
                    break

            # Координаты клетки с минимальным множеством
            r, c = MIN[0]

            # Изначально решений текущего состояния нет
            res = 0

            # Перебираем все вставки
            for v in MIN[1]:
                solutionCopy = copy.deepcopy(solution)  # Сохраняем копию текущего состояния
                solutionCopy[r][c] = v
                res += num_of_solutions(solutionCopy, n)  # Прибавляем решения следующего состояния
            return res

        return num_of_solutions(copy.deepcopy(self.puzzle), self.n)

    def possible_matrix(puzzle: list, row: int, col: int, n: int):
        ''' Возвращает мн-во вставок для позиции в виде блока '''
        block = [[sudoku.UNASSIGNED] * 3 for i in range(3)]

        for num in sudoku.get_possible(puzzle, row, col, n):
            block[(num - 1) // 3][(num - 1) % 3] = num
        return block

    @staticmethod
    def get_possible(puzzle: list, row: int, col: int, n: int) -> set:
        ''' Возвращает мн-во возможных вставок для клетки '''
        if puzzle[row][col] != sudoku.UNASSIGNED:  # Если клетка заполнена
            return None
        else:
            values = {v + 1 for v in range(n ** 2)}
            values -= sudoku.row_possible(puzzle, row, n)
            values -= sudoku.col_possible(puzzle, col, n)
            values -= sudoku.block_possible(puzzle, row, col, n)
            return values

    @staticmethod
    def row_possible(puzzle: list, row: int, n: int) -> dict:
        ''' Возможные вставки относительно строки '''
        return {puzzle[row][c] for c in range(n ** 2)}

    @staticmethod
    def col_possible(puzzle: list, col: int, n: int) -> dict:
        ''' Возможные вставки относительно столбца '''
        return {puzzle[r][col] for r in range(n ** 2)}

    @staticmethod
    def block_possible(puzzle: list, row: int, col: int, n: int) -> dict:
        ''' Возможные вставки относительно блока '''
        col = n * (col // n)  # Столбец начала блока
        row = n * (row // n)  # Строка начала блока
        return {puzzle[row + r][col + c] for r in range(n) for c in range(n)}

    def swap(self, cols: bool=False) -> None:
        ''' Смена двух строк/столбцов из одного блока'''
        first = randint(0, self.size - 1)  # Первый индекс выбираем случайно
        block = (first // self.n) * self.n  # Координаты попавшегося блока
        second = randint(block, block + self.n - 1)  # Второй индекс выбираем уже из блока

        #  Если индексы совпали
        while first == second:
            second = randint(block, block + self.n - 1)

        for ind in range(self.size):
            if cols:
                self.puzzle[ind][first], self.puzzle[ind][second] = \
                self.puzzle[ind][second], self.puzzle[ind][first]
            else:
                self.puzzle[first][ind], self.puzzle[second][ind] = \
                self.puzzle[second][ind], self.puzzle[first][ind]

    def swap_area(self, cols: bool=False) -> None:
        ''' Смена двух различных блоков местами'''
        area_1 = randint(0, self.n - 1)
        area_2 = randint(0, self.n - 1)

        #  Если индексы совпали
        while area_1 == area_2:
            area_2 = randint(0, self.n - 1)

        for i in range(self.n):
            for j in range(self.size):
                if cols:
                    self.puzzle[j][area_1 * self.n + i], self.puzzle[j][area_2 * self.n + i] = \
                    self.puzzle[j][area_2 * self.n + i], self.puzzle[j][area_1 * self.n + i]
                else:
                    self.puzzle[area_1 * self.n + i][j], self.puzzle[area_2 * self.n + i][j] = \
                    self.puzzle[area_2 * self.n + i][j], self.puzzle[area_1 * self.n + i][j]

    def transpose(self, side: bool=False) -> None:
        ''' Транспонирование относительно главной/побочной диагонали '''
        for i in range(self.size):
            for j in range(self.size):
                if side and j > self.size - i - 1:
                    self.puzzle[i][j], self.puzzle[self.size - j - 1][self.size - i - 1] = \
                    self.puzzle[self.size - j - 1][self.size - i - 1], self.puzzle[i][j]
                elif not side and j > i:
                    self.puzzle[i][j], self.puzzle[j][i] = \
                    self.puzzle[j][i], self.puzzle[i][j]

    def mix(self, times: int, p: list=[0.7, 0.25, 0.05]):
        ''' Перемешивание судоку заданное кол-во раз по заданным вероятностям '''
        if abs(sum(p) - 1) >= 1e-4 or len(p) != 3:
            raise ArgumentError(f"Invalid probabilities {p}, sum must be close to 1 and len = 3")

        rowcols, blocks, _ = p
        for _ in range(times):
            #  Выбираем вероятность перестановки и ее инверсию
            shuffle, inverse = random(), randint(0, 1)

            #  Выбираем конкретную перерестановки иисходя из вероятности
            if shuffle <= rowcols:
                self.swap(inverse)
            elif shuffle <= rowcols + blocks:
                self.swap_area(inverse)
            else:
                self.transpose(inverse)

    @staticmethod
    def generate(size: int, n_empty: int):
        ''' Генерирует судоку с заданным размером и кол-вом пустых клеток'''
        result = sudoku.trivial(size)  # Задаем базовую конфигурацию
        result.mix(times=1000)  # Перемешиваем
        back = 0  # Счетчик откатов для избежания зацикливания

        while n_empty and back <= size ** 3:
            x, y = randint(0, (size ** 2) - 1), randint(0, (size ** 2) - 1)  # Выбираем случайную клетку

            # Если выбрали не пустую, то запомним и обнулим
            if result.puzzle[x][y] != sudoku.UNASSIGNED:
                temp, result.puzzle[x][y] = \
                result.puzzle[x][y], sudoku.UNASSIGNED

                # Если решенин не единственно, то откатываем
                if result.n_solutions() != 1:
                    result.puzzle[x][y] = temp
                    back += 1
                else:
                    n_empty -= 1
        return result

    # Построчная печать судоку в другом формате
    def __str__(self, vert_delim: str='|', horz_delim: str='', cent_delim: str='+'):
        ''' Печать судоку в стандартном виде '''
        result = []
        place = ceil(log10(self.size)) + 1  # Занимаемое цифрой место
        formatter = lambda num: str(num).rjust(place - len(str(num)))  # Форматирующая функция

        for i in range(self.n ** 2):
            if i and not i % self.n:
                result.append(cent_delim.join('-' * self.n * (place - 1) for j in range(self.n)))
            result.append(vert_delim.join(''.join(map(formatter, self.puzzle[i][j * self.n:(j + 1) * self.n])) for j in range(self.n)))
        return '\n'.join(result)
