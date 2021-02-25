import sudoku
import os

ROOT = 'C:\\Users\\HP_650\\Desktop\\Судоку\\files'


# Считывание определённой головоломки
def get(file: str, n: int=3) -> list:
	with open(ROOT + os.sep + file + '.txt', 'rt') as file:
		puzzle = list(filter(lambda x: x.isdigit(), file.read()))
		return [[int(puzzle[i * (n ** 2) + j]) for j in range(n ** 2)] for i in range(n ** 2)]



# Загрузка определённой головоломки
def set(puzzle: list, n: int, file: str) -> None:
	with open(ROOT + os.sep + file + '.txt', 'wt') as file:
		file.write(sudoku.to_str_2(puzzle, n))


# Загрузка головоломки
def upload(puzzle: list, n: int=3) -> None:
	if not sudoku.is_correct(puzzle, n):
		raise Exception('Некорректное судоку')
	if sudoku.solutions(puzzle, n) != 1:
		raise Exception(f'Множественность решения {sudoku.solutions(puzzle, n)}')

	set(puzzle, n, 'start')
	set(puzzle, n, 'current')
	set(sudoku.solve(puzzle, n), n, 'solution')


# Выгрузка трёх судоку
def load(n: int=3) -> tuple:
	return get('start', n), get('current', n), get('solution', n)


# python C:\Users\HP_650\Desktop\Судоку\DBMS.py
