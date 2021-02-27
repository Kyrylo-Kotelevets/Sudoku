import drawing
import sudoku

puzzle = [[1, 0, 0, 0, 0, 0, 0, 0, 6],
		  [0, 5, 0, 9, 0, 2, 0, 8, 0],
		  [8, 0, 3, 0, 0, 0, 5, 0, 1],
		  [0, 0, 0, 8, 4, 5, 0, 0, 0],
		  [0, 0, 4, 0, 0, 0, 8, 0, 0],
		  [0, 0, 0, 2, 3, 6, 0, 0, 0],
		  [3, 0, 9, 0, 0, 0, 4, 0, 8],
		  [0, 6, 0, 4, 0, 7, 0, 5, 0],
		  [4, 0, 0, 0, 0, 0, 0, 0, 7]]

initial = sudoku.sudoku(puzzle)
current = initial.copy()
current[0, 1] = 4
current[1, 0] = 7

drawing.draw(initial, current, initial.solution(), possible=True, theme='paper')
