from random import randint, random
import copy

# Минимально и максимально возможные уровни
MIN_LEVEL, MAX_LEVEL = 10, 62
UNASSIGNED = 0


# Получение судоку, заполненного нулями
def get_empty(n: int=3) -> list:
	return [[UNASSIGNED] * (n ** 2) for row in range(n ** 2)]


# Получение примера заполненного судоку
def get_example(n: int=3) -> list:
	# Базовый набор чисел
	base = [num + 1 for num in range(n ** 2)]
	puzzle = []

	for i in range(n):
		for j in range(n):
			#  Сдвигаем базовый набор чисел и складываем
			puzzle.append(base[i + j * n:] + base[:i + j * n])

	return puzzle


# Начальное состояние для перемешивания
def getBasePuzzle(n: int=3) -> list:
	if n == 3:
		return [[2, 9, 3, 4, 5, 7, 6, 8, 1], [4, 7, 5, 1, 8, 6, 3, 9, 2], [1, 6, 8, 3, 9, 2, 7, 4, 5], [9, 4, 2, 5, 7, 1, 8, 6, 3], [3, 8, 1, 6, 2, 9, 5, 7, 4], [6, 5, 7, 8, 3, 4, 1, 2, 9], [7, 2, 6, 9, 1, 3, 4, 5, 8], [5, 1, 4, 2, 6, 8, 9, 3, 7], [8, 3, 9, 7, 4, 5, 2, 1, 6]]
	else:
		return get_example(n)


# Проверка судоку на решенность
def is_solved(puzzle: list) -> bool:
	# Проверяем на факт того, что все клетки заполнены
	return all(num != UNASSIGNED for row in puzzle for num in row)


# Подсчет пустых клеток в головоломке
def valuation(puzzle: list) -> int:
	return sum(row.count(UNASSIGNED) for row in puzzle)


# Подсчет пустых клеток в головоломке
def are_equal(user_puzzle: list, initial_puzzle: list, n: int=3) -> bool:
	for i in range(n ** 2):
		for j in range(n ** 2):
			if initial_puzzle[i][j] != UNASSIGNED and user_puzzle[i][j] != initial_puzzle[i][j]:
				return False
	return True


# Проверка наличия повторов
def is_correct(puzzle: list, n: int=3) -> bool:
	for i in range(n ** 2):
		for j in range(n ** 2):
			# Если клетка не заполнена
			if puzzle[i][j] == UNASSIGNED:
				continue
			# Цифра некорректна
			if puzzle[i][j] < 1 or puzzle[i][j] > n ** 2:
				return False

			for k in range(n ** 2):
				# Если есть повтор в строке
				if puzzle[i][k] == puzzle[i][j] and k != j:
					return False
				# Если есть повтор в столбце
				if puzzle[k][j] == puzzle[i][j] and k != i:
					return False

			row = n * (i // n)
			col = n * (j // n)
			for r in range(row, row + n):
				for c in range(col, col + n):
					# Если есть повтор в квадрате
					if puzzle[r][c] == puzzle[i][j] and (r != i or c != j):
						return False
	return True


# Главная сборочная функция
def solve(puzzle: list, n: int) -> list:
	# Копируем исходное судоку
	solution = copy.deepcopy(puzzle)
	# Если решение существует
	if solveHelper(solution, n):
		return solution
	# Решения не существует
	return None


#  Математический аппарат
def solveHelper(solution: list, n: int) -> bool:
	# Минимальное множество возможных чисел
	MIN = None
	while True:
		MIN = None
		for row in range(n ** 2):
			for col in range(n ** 2):
				# Если клетка пуста, то продолжаем
				if solution[row][col] != UNASSIGNED:
					continue

				# Получаем  множество чисел для клетки
				possible = get_possible(row, col, solution)
				# Размер множества чисел
				count = len(possible)

				# Множество пусто, текущее состояние нерешаемо
				if count == 0:
					return False
				# Если возможно только одно число, то вставим
				if count == 1:
					solution[row][col] = possible.pop()
				# Если минимальное множество пусто или больше
				if not MIN or count < len(MIN[1]):
					MIN = ((row, col), possible)

		# Если множество пусто, то судоку собрано
		if not MIN:
			return True
		# Если больше нет однозначных чисел для вставки
		elif len(MIN[1]) > 1:
			break

	# Координаты клетки с минимальным множеством
	r, c = MIN[0]

	# Перебираем все числа из множества
	for v in MIN[1]:
		# Сохраняем копию текущего состояния
		solutionCopy = copy.deepcopy(solution)
		# Запоняем клетку теекущим числом из множества
		solutionCopy[r][c] = v
		# Если рекурсивный поиск был удачным
		if solveHelper(solutionCopy, n):
			for r in range(n ** 2):
				for c in range(n ** 2):
					solution[r][c] = solutionCopy[r][c]
			return True
	return False


# Число возможных решений судоку
def solutions(puzzle: list, n: int=3) -> int:
	return num_of_solutions(copy.deepcopy(puzzle), n)


# Мат. аппарат для пересчёта решений
def num_of_solutions(solution: list, n: int=3) -> int:
	MIN = None
	while True:
		MIN = None
		for row in range(n ** 2):
			for col in range(n ** 2):
				# Если клетка пуста, то продолжаем
				if solution[row][col] != UNASSIGNED:
					continue

				# Получаем  множество чисел для клетки
				possible = get_possible(row, col, solution, n)
				# Размер множества чисел
				size = len(possible)

				# Множество пусто, решений нет
				if size == 0:
					return 0
				# Если возможно только одно число, то вставим
				if size == 1:
					solution[row][col] = possible.pop()
				# Если минимальное множество пусто или больше
				if not MIN or size < len(MIN[1]):
					MIN = ((row, col), possible)
		# Если множество пусто, то судоку собрано
		if MIN is None:
			return 1
		# Если больше нет однозначных чисел для вставки
		elif len(MIN[1]) > 1:
			break

	# Координаты клетки с минимальным множеством
	r, c = MIN[0]

	# Изначально решений текущего состояния нет
	res = 0

	# Перебираем все числа из множества
	for v in MIN[1]:
		# Сохраняем копию текущего состояния
		solutionCopy = copy.deepcopy(solution)
		# Запоняем клетку теекущим числом из множества
		solutionCopy[r][c] = v
		# Прибавляем решения следующего состояния
		res += num_of_solutions(solutionCopy, n)
	return res


# Получение множества возможных чисел для позиции в виде блока
def get_block_possible(row: int, col: int, puzzle: list) -> dict:
	block = [[UNASSIGNED] * 3 for i in range(3)]

	for num in get_possible(row, col, puzzle):
		block[(num - 1) // 3][(num - 1) % 3] = num
	return block


# Получение всех множеств для вставки
def get_all_possible(puzzle: list):
	return [[find_pos(i, j, puzzle) for j in range(9)] for i in range(9)]


# Получение множества возможных чисел для позиции
def get_possible(row: int, col: int, puzzle: list, n: int=3, diagonal: bool=False) -> dict:
	if puzzle[row][col] != UNASSIGNED:
		return None
	else:
		values = {v + 1 for v in range(n ** 2)}
		values -= get_row_values(puzzle, row, n)
		values -= get_col_values(puzzle, col, n)
		values -= get_block_values(puzzle, row, col, n)
		if diagonal:
			values -= get_diag_values(puzzle, row, col, n)
		return values


# Получение возможных чисел для row-той строки
def get_row_values(puzzle: list, row: int, n: int) -> dict:
	return {puzzle[row][c] for c in range(n ** 2)}


# Получение возможных чисел для col-того столбца
def get_col_values(puzzle: list, col: int, n: int) -> dict:
	return {puzzle[r][col] for r in range(n ** 2)}


# Получение возможных чисел квадрата
def get_block_values(puzzle: list, row: int, col: int, n: int) -> dict:
	# Координаты начала блока
	col = n * (col // n)
	row = n * (row // n)
	return {puzzle[row + r][col + c] for r in range(n) for c in range(n)}


# Получение возможных чисел для диагональных элементов
def get_diag_values(puzzle: list, row: int, col: int, n: int) -> dict:
	values = set()
	if row == col:
		values += {puzzle[i][i] for i in range(n ** 2)}
	if row == n - col - 1:
		values += {puzzle[j][n - j - 1] for j in range(n ** 2)}
	return values


# Свап двух разных строк в одном квадранте
def swap_rows(puzzle: list, n: int) -> None:
	R1 = randint(0, (n ** 2) - 1)
	R2 = randint((R1 // n) * n, (R1 // n) * n + (n - 1))
	while R1 == R2:
		R2 = randint((R1 // n) * n, (R1 // n) * n + (n - 1))

	for j in range(n ** 2):
		puzzle[R1][j], puzzle[R2][j] = puzzle[R2][j], puzzle[R1][j]


# Свап двух разных столбцов в одном квадранте
def swap_cols(puzzle: list, n: int) -> None:
	С1 = randint(0, (n ** 2) - 1)
	С2 = randint((С1 // n) * n, (С1 // n) * n + (n - 1))
	while С1 == С2:
		С2 = randint((С1 // n) * n, (С1 // n) * n + (n - 1))

	for i in range(n ** 2):
		puzzle[i][С1], puzzle[i][С2] = puzzle[i][С2], puzzle[i][С1]


# Свап двух разных блочных строк в одном квадранте
def swap_rows_area(puzzle: list, n: int) -> None:
	area1 = randint(0, n - 1)
	area2 = randint(0, n - 1)
	while area1 == area2:
		area2 = randint(0, n - 1)

	for i in range(n):
		for j in range(n ** 2):
			puzzle[area1 * n + i][j], puzzle[area2 * n + i][j] = puzzle[area2 * n + i][j], puzzle[area1 * n + i][j]


# Свап двух разных блочных столбцов в одном квадранте
def swap_cols_area(puzzle: list, n: int) -> None:
	area1 = randint(0, n - 1)
	area2 = randint(0, n - 1)
	while area1 == area2:
		area2 = randint(0, n - 1)

	for j in range(n):
		for i in range(n ** 2):
			puzzle[i][area1 * n + j], puzzle[i][area2 * n + j] = puzzle[i][area2 * n + j], puzzle[i][area1 * n + j]


# Транспонирование судоку относительно главной диагонали
def main_transpose(puzzle: list, n: int) -> None:
	for i in range(n ** 2):
		for j in range(i + 1, n ** 2):
			puzzle[i][j], puzzle[j][i] = puzzle[j][i], puzzle[i][j]


# Транспонирование судоку относительно побочной диагонали
def side_transpose(puzzle: list, n: int) -> None:
	for i in range(n ** 2):
		for j in range(i + 1, n ** 2):
			puzzle[i][j], puzzle[j][i] = puzzle[j][i], puzzle[i][j]


# Набор вероятностей: [0.35/0.35, 0.125/0.125, 0.025/0.025]
# Запутывание/перемешивание судоку
def mix_puzzle(puzzle: list, times: int = 200, n: int=3) -> None:
	# Пока не выполним все нужные перестановки
	for _ in range(times):
		# Выбираем случайное число, соответсвующее некоторому изменению
		shuffle = random()

		if shuffle <= 0.7:
			if randint(0, 1) & 1:
				swap_rows(puzzle, n)
			else:
				swap_cols(puzzle, n)
		elif shuffle <= 0.95:
			if randint(0, 1) & 1:
				swap_rows_area(puzzle, n)
			else:
				swap_cols_area(puzzle, n)
		else:
			if randint(0, 1) & 1:
				main_transpose(puzzle, n)
			else:
				side_transpose(puzzle, n)


# Случайная перетасовка судоку
def getMixedPuzzle(times: int = 200) -> list:
	puzzle = getExample()
	mix_puzzle(puzzle, times)
	return puzzle


# Получение судоку для заданного уровня
def get_level_puzzle(level: int, n: int=3) -> list:
	# Начнём базового состояния
	puzzle = getBasePuzzle(n)
	# Перемешаем судоку
	mix_puzzle(puzzle, n)
	# Введем счетчик откатов во избежание зацикливания
	back = 0

	# Пока нужный уровень сложности не достигнут
	while level and back <= n ** 3:
		# Выберем случайную клетку
		x, y = randint(0, (n ** 2) - 1), randint(0, (n ** 2) - 1)

		# Если выбрали не пустую, то запомним и обнулим
		if puzzle[x][y] != UNASSIGNED:
			temp, puzzle[x][y] = puzzle[x][y], UNASSIGNED

			# Если решенин не единственно, то откат +1
			if solutions(puzzle) != 1:
				puzzle[x][y] = temp
				back += 1
			# Иначе понижаем целевой уровень
			else:
				level -= 1
	return puzzle


# Построчная печать судоку в другом формате
def to_str_2(puzzle: list, n: int) -> str:
	result = []
	for i in range(n ** 2):
		if i and not i % n:
			result.append('+'.join('-' * n for j in range(n)))
		result.append('|'.join(''.join(map(str, puzzle[i][j * n:(j + 1) * n])) for j in range(n)))
	return '\n'.join(result)


# Построчная печать судоку
def to_str(puzzle: list) -> str:
	return '\n'.join(map(str, puzzle))


# python C:\Users\HP_650\Desktop\Судоку\sudoku.py
