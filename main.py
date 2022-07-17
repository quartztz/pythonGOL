import pygame
import pygame.display as display
import pygame.draw as draw
from random import random

import time

# conway's game of life! 
# this starts off a blank page: then, you can use the mouse to set 
# alive cells by left clicking. When you're done, press enter and the 
# logic starts! Alternatively, a parameter can be changed in the "createArray()" 
# function, in "run()": adding a third float parameter p between 0 and 1 will change the 
# probability of any given cell to be alive. 

w, h = 500, 500
scale = 20

win = display.set_mode([w, h], pygame.FULLSCREEN)

white, black, grey = pygame.Color(230, 230, 250), pygame.Color(20, 20, 20), pygame.Color(145, 145, 145)
# global state
state = 'setup'

def createArray(cols, rows, p = 0):

	# creates a two-dimensional array of cells: 
	# cells[x][y], where x is columns and y is rows (0, 0 is top right). 
	# if p = 0: blank canvas
	# if 0 < p < 1: any given cell has a p probability to be alive
	
	arr = []
	for i in range(cols):
		arr.append([])
		for j in range(rows):
			r = random()
			if r < p: a = 1
			else: a = 0
			arr[i].append(a)
	return arr

def render(cells): 
	rects = []

	# draws a square of width 'scale' for every cell:
	# if the cell is alive the square is filled, 
	# if it's dead, the square is empty.

	for i in range(len(cells)): 
		for j in range(len(cells[i])): 
			x = i * scale
			y = j * scale
			r = pygame.Rect(x, y, scale, scale)
			rects.append(r)
			if cells[i][j] == 1:
				draw.rect(win, black, r)
			else: draw.rect(win, grey, r, width = 1)

	return rects

def handleEvents(running): 
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			running = False

def setup(cells, rects): 

	for event in pygame.event.get(): 
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				return 'logic'
		if event.type == pygame.MOUSEBUTTONDOWN: 
			mx, my = pygame.mouse.get_pos()
			for rect in rects: 
				if rect.collidepoint((mx, my)): 
					s = cells[rect.x // scale][rect.y // scale] # gets current state of the cell
					cells[rect.x // scale][rect.y // scale] = int(not s) # toggles from 0 to 1

	return 'setup'

def createNext(cols, rows): 
	return [[0 for j in range(rows)] for n in range(cols)]

def logic(cells): 
	nxt = createNext(w // scale, h // scale)

	for i in range(len(cells)): 
		for j in range(len(cells[i])):
			# uses getLiveNeighbours() to find all live neighbours. 
			
			lcount = getLiveNeighbours(i, j, cells)
			
			# now we have a count of all live cells around, logic can start. 

			n = cells[i][j]

			if n == 1: # if cell is alive
				if lcount not in [2, 3]: 
					n = 0
			elif n == 0: # if cell is dead
				if lcount == 3: 
					n = 1

			nxt[i][j] = n

	return nxt

def getLiveNeighbours(i, j, cells):
	# function that finds all of the live neighbours of any given cell. 

	# code for the wraparound system: if the cell is on an edge the other 
	# side of the field is used for the logic, to avoid the issues of the 
	# "infinite board" the game is supposed to be played on.

	# could use a better implementation using % but not a priority. 

	mini = i - 1 if i != 0 else len(cells) - 1
	plui = i + 1 if i != len(cells) - 1 else 0
	minj = j - 1 if j != 0 else len(cells[i]) - 1 
	pluj = j + 1 if j != len(cells[i]) - 1 else 0

	n = [
		cells[mini][minj], 
		cells[i][minj], 
		cells[plui][minj], 
		cells[mini][j], 
		cells[plui][j], 
		cells[mini][pluj], 
		cells[i][pluj], 
		cells[plui][pluj]
		] # array of length eight 

	return sum(n)

def run():
	pygame.init() 
	cells = createArray(w // scale, h // scale)
	running = True
	state = 'setup'

	while running:
		handleEvents(running)
		win.fill(white)
		rects = render(cells)

		if state == 'setup': 
			state = setup(cells, rects)

		elif state == 'logic': 
			cells = logic(cells)

		display.flip()
		time.sleep(0.150)

	pygame.quit()

run()