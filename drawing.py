from PIL import Image, ImageDraw, ImageFont
from sudoku import sudoku
from os import sep
import math


ROOT = "files"
b_border = 14
s_border = 4
width = 200
im_size = width * 9 + s_border * 6 + b_border * 4

G = lambda x: b_border * math.ceil(x / 3) + s_border * max(0, x - 1 - math.floor((x - 1) / 3)) + x * width

X = lambda x: b_border * (x // 3 + 1) + s_border * (x - x // 3) + x * width
Y = lambda y: X(y)

R = lambda x, y: [(X(x), Y(y)), (X(x) + width, Y(y) + width)]
C = lambda x, y: [(X(x), Y(y)), (X(x) + width, Y(y) + width)]


THEMES = {
	'classic' : {
		'possible_color': ['#ffffff', '#ff0003', '#ff8a00', '#fff000', '#7dff00', '#00c000', '#00fbf3', '#2447ff', '#000297', '#4e006c'], # Цвета возможных чисел
		'image_color':           '#ffffff', # Цвет основного изображения
		'block_color':           '#f2f2f2', # Цвет нечётных блоков
		'grid_color':            '#000000', # Цвет сетки
		'opened_num_color':      '#000000', # Цвет только что окрытой цифры
		'opened_block_color':    '#80ff80', # Цвет только что окрытой клетки
		'invalid_color':         '#ff0000', # Цвет некорректной цифры
		'start_num_color':       '#000000', # Цвет изначальной цифры
		'filled_num_color':      '#404040', # Цвет заполненной игроком цифры
		'correct_num_color':     '#008000', # Цвет правильно заполненной цифры
		'correct_block_color':   '#80ff80', # Цвет правильно заполненной клетки
		'wrong_num_color':       '#ff0000', # Цвет неправильно заполненной цифры
		'wrong_block_color':     '#ff9999', # Цвет неправильно заполненной клетки
		'possible_border_color': '#000000', # Цвет обводки для возможных чисел

		'grid_type': 'default',   # Тип сетки
		'highlight': 'rectangle', # Тип выделения клеток
		'blocks':     True,       # Другой цвет нечётных блоков

		'grad':         False, # Наличие градиента
		'GR_from':      None,  # Начальный цвет градиента
		'GR_to':        None,  # Конечный цвет градиента
		'grad_padding': None,  # Начало градиента
		'grad_square':  None,  # Конец градиента


		'b_font': ImageFont.truetype(ROOT + sep + 'arial.ttf', 145),        # Шрифт основных чисел
		's_font': ImageFont.truetype(ROOT + sep + 'arial.ttf', 50),         # Шрифт возможных чисел
		't_font': ImageFont.truetype(ROOT + sep + 'arial.ttf', 50 + 2 * 2), # Шрифт для обводки возможных чисел

		'title': 'Классическая'
	},

	'paper' : {
		'possible_color': ['#f2f2f2'] + ['#000000'] * 9, # Цвета возможных чисел
		'image_color':           '#f2f2f2', # Цвет основного изображения
		'block_color':           '#e2e2e2', # Цвет нечётных блоков
		'grid_color':            '#000000', # Цвет сетки
		'opened_num_color':      '#000000', # Цвет только что окрытой цифры
		'opened_block_color':    '#80ff80', # Цвет только что окрытой клетки
		'invalid_color':         '#ff0000', # Цвет некорректной цифры
		'start_num_color':       '#000000', # Цвет изначальной цифры
		'filled_num_color':      '#404040', # Цвет заполненной игроком цифры
		'correct_num_color':     '#008000', # Цвет правильно заполненной цифры
		'correct_block_color':   '#80ff80', # Цвет правильно заполненной клетки
		'wrong_num_color':       '#ff0000', # Цвет неправильно заполненной цифры
		'wrong_block_color':     '#ff9999', # Цвет неправильно заполненной клетки
		'possible_border_color': '#000000', # Цвет обводки для возможных чисел

		'grid_type': 'default',   # Тип сетки
		'highlight': 'rectangle', # Тип выделения клеток
		'blocks':     True,      # Другой цвет нечётных блоков

		'possible_border': False, # Обводка чисел для вставки

		'possible_border_size': 2, # Размер обводки стеков
		'b_font_size': 145,        # Размер основного шрифта
		'b_font_size': 100,        # Размер шрифта заполненных клеток
		's_font_size': 50,         # Размер шрифта стеков
		't_font_size': 50 + 2 * 2, # Размер шрифта обводки стеков

		'b_font_padding': (61, 12), # Костыльный отступ для тескта
		'f_font_padding': (58, 20), # Костыльный отступ для тескта
		's_font_padding': (64, 60), # Костыльный отступ для тескта
		's_font_start': (22, 14),   # Костыльный отступ для тескта

		'b_font': ImageFont.truetype(ROOT + sep + 'ariblk.ttf', 120),           # Шрифт основных чисел
		'f_font': ImageFont.truetype(ROOT + sep + '5thgradecursive-2.ttf', 100), # Шрифт заполненных чисел
		's_font': ImageFont.truetype(ROOT + sep + 'arial.ttf', 50),              # Шрифт возможных чисел
		't_font': ImageFont.truetype(ROOT + sep + 'arial.ttf', 50 + 2 * 2),      # Шрифт для обводки возможных чисел

		'title': 'Газетная бумага' # Название темы
	},
}


def draw_highlight(x, y, theme, color, image):
	''' Рисует подсветку клетки '''
	drawer = ImageDraw.Draw(image)
	if theme['highlight'] == 'rectangle':
		drawer.rectangle(R(x, y), fill=color)
	if theme['highlight'] == 'circle':
		drawer.ellipse(R(x, y), fill=color)


def fill_possible(theme, x0: int, y0: int, puzz, image):
	''' Отображает вставки в клетке '''
	drawer = ImageDraw.Draw(image)
	possible = sudoku.possible_matrix(puzzle=puzz.puzzle,
									  row=y0,
									  col=x0, 
									  n=puzz.n)

	for i in range(3):
		for j in range(3):
			x = X(x0) + theme['s_font_start'][0] + j * theme['s_font_padding'][0]
			y = Y(y0) + theme['s_font_start'][1] + i * theme['s_font_padding'][1]
			num = possible[i][j]

			if num != sudoku.UNASSIGNED:
				if theme['possible_border']:
					drawer.text((x - theme['possible_border_size'], y - theme['possible_border_size']), str(num), font=theme['t_font'], fill=theme['possible_border_color'])
				drawer.text((x, y), str(num), font=theme['s_font'], fill=theme['possible_color'][num])


def color_blocks(theme, image):
	''' Подсвечивает нечетные блоки '''
	drawer = ImageDraw.Draw(image)

	for i in range(3):
		for j in range(3):
			if not (i + j) % 2:
				drawer.rectangle([(X(i * 3), X(j * 3)), (X(i * 3) + 3 * width + 2 * s_border, X(j * 3) + 3 * width + 2 * s_border)], fill=theme['block_color'])


def fill_grid(theme, image):
	''' Рисует сетку '''
	drawer = ImageDraw.Draw(image)
	for i in range(10):
		if i % 3:
			drawer.rectangle([(G(i), 0), (G(i) + s_border, im_size)], fill=theme['grid_color'])
			drawer.rectangle([(0, G(i)), (im_size, G(i) + s_border)], fill=theme['grid_color'])
		else:
			drawer.rectangle([(G(i), 0), (G(i) + b_border, im_size)], fill=theme['grid_color'])
			drawer.rectangle([(0, G(i)), (im_size, G(i) + b_border)], fill=theme['grid_color'])


def fill_partly_grid(theme, image):
	''' Рисует сетку с прорехами '''
	drawer = ImageDraw.Draw(image)
	partly_pad = 20
	for i in range(10):
		if i % 3:
			for j in range(9):
				drawer.rectangle([(G(i), G(j) + 2 * partly_pad), (G(i) + s_border, G(j + 1) - partly_pad)], fill=theme['grid_color'])
				drawer.rectangle([(G(j) + 2 * partly_pad, G(i)), (G(j + 1) - partly_pad, G(i) + s_border)], fill=theme['grid_color'])
		else:
			if i != 0 and i != 9:
				drawer.rectangle([(G(i), 0), (G(i) + b_border, im_size)], fill=theme['grid_color'])
				drawer.rectangle([(0, G(i)), (im_size, G(i) + b_border)], fill=theme['grid_color'])


def fill_ivalid(theme, puzzle, current, image):
	''' Подсвечивает неверные цифры '''
	drawer = ImageDraw.Draw(image)
	for i in range(9):
		for j in range(9):
			if current[i, j] == sudoku.UNASSIGNED:
				continue

			for k in range(9):
				if current[i, k] == current[i, j] and k != j:
					if current[i, j] != puzzle[i, j]:
						draw_highlight(j, i, theme=theme, color=theme['invalid_color'], image=image)
					if current[i, k] != puzzle[i, k]:
						draw_highlight(k, i, theme=theme, color=theme['invalid_color'], image=image)
				if current[k, j] == current[i, j] and k != i:
					if current[i, j] != puzzle[i, j]:
						draw_highlight(j, i, theme=theme, color=theme['invalid_color'], image=image)
					if current[k, j] != puzzle[k, j]:
						draw_highlight(j, k, theme=theme, color=theme['invalid_color'], image=image)

			row = 3 * (i // 3)
			col = 3 * (j // 3)
			for r in range(row, row + 3):
				for c in range(col, col + 3):
					if current[r, c] == current[i, j] and (r != i or c != j):
						if current[i, j] != puzzle[i, j]:
							draw_highlight(j, i, theme=theme, color=theme['invalid_color'], image=image)
						if current[r, c] != puzzle[r, c]:
							draw_highlight(c, r, theme=theme, color=theme['invalid_color'], image=image)


def fill_numbers(theme, puzzle, current, solution, image):
	''' Заполняет цифры '''
	drawer = ImageDraw.Draw(image)
	for i in range(puzzle.size):
		for j in range(puzzle.size):
			x, y = X(j), Y(i)

			if puzzle[i, j] != sudoku.UNASSIGNED:
				x, y = x + theme['b_font_padding'][0], y + theme['b_font_padding'][1]
				drawer.text((x, y), str(puzzle[i, j]), font=theme['b_font'], fill=theme['start_num_color'])
			elif puzzle[i, j] == sudoku.UNASSIGNED and current[i, j] != 0:
				x, y = x + theme['f_font_padding'][0], y + theme['f_font_padding'][1]
				if solution is None:
					drawer.text((x, y), str(current[i, j]), font=theme['f_font'], fill=theme['filled_num_color'])
				elif current[i, j] == solution[i, j]:
					draw_highlight(j, i, theme=theme, color=theme['correct_block_color'], image=image)
					drawer.text((x, y), str(current[i, j]), font=theme['f_font'], fill=theme['correct_num_color'])
				elif current[i, j] != sudoku.UNASSIGNED:
					draw_highlight(j, i, theme=theme, color=theme['wrong_block_color'], image=image)
					drawer.text((x, y), str(current[i, j]), font=theme['f_font'], fill=theme['wrong_num_color'])
				else:
					pass


def fill_all_possible(theme, puzzle, current, image):
	''' Рисует все вставки '''
	drawer = ImageDraw.Draw(image)
	for i in range(9):
		for j in range(9):
			if puzzle[i, j] == sudoku.UNASSIGNED and current[i, j] == sudoku.UNASSIGNED:
				fill_possible(theme, j, i, current, image)


def draw(puzzle: list=None,  # Исходное судоку
		 current: list=None,  # Заполняемое судоку
		 solution: list=None,  # Решенное судоку
		 possible: bool=False,  # Отображать ли вставки
		 correct: bool=False,  # Подсвечивать ли правильные
		 solved: bool=False,  # ОТображать сразу решенное
		 theme='classic'  # Название темы
		 ):
	''' Главная отрисовочная функция '''
	theme = THEMES[theme]
	image = Image.new('RGB', (im_size, im_size), theme['image_color'])

	if theme['blocks']:
		color_blocks(theme, image=image)

	if not sudoku.is_valid(current.puzzle):
		fill_ivalid(theme, puzzle=puzzle, current=current, image=image)
	
	if possible:
		fill_all_possible(theme, puzzle=puzzle, current=current, image=image)
	
	if correct:
		fill_numbers(theme, puzzle=puzzle, current=current,  solution=solution, image=image)
	elif solved or (current.is_solved() and current.are_equal(solution)):
		fill_numbers(theme, puzzle=puzzle, current=solution, solution=None, image=image)
	else:
		fill_numbers(theme, puzzle=puzzle, current=current,  solution=None, image=image)
	
	if theme['grid_type'] == 'partly':
		fill_partly_grid(theme, image=image)
	else:
		fill_grid(theme, image=image)

	image.show()
	image.save(ROOT + sep + 'sudoku.png')
