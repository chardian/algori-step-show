"""
寻路算法
"""
import threading
from typing import List
import math
from ui_util import *

COL = 15
ROW = 15

CELL = 40
TO_EXIT = False

BLOCK_START = 1
BLOCK_END = 2  # 目标位置
BLOCK_WALL = 3
BLOCK_TEXT = 3  # 显示文本
BLOCK_ROAD = 10


class Board(DisplayObject):
	def __init__(self):
		super(Board, self).__init__()
		self.x = 20
		self.y = 20
		self.blocks = {}

	def add_block(self, x_idx, y_idx, block_type):
		x = round(self.x + (x_idx + 0.5) * CELL)
		y = round(self.y + (y_idx + 0.5) * CELL)
		b = Block(block_type)
		b.x = x
		b.y = y
		self.children.append(b)
		self.blocks[(x_idx, y_idx)] = b
		return b

	def get_block(self, x_idx, y_idx):
		if (x_idx, y_idx) in self.blocks:
			return self.blocks[(x_idx, y_idx)]
		return None

	def remove_block(self, x_idx, y_idx):
		b = self.get_block(x_idx, y_idx)
		if b is not None:
			self.children.remove(b)
			del self.blocks[(x_idx, y_idx)]

	def render(self):
		# 画迷宫本身
		screen.fill([55, 55, 55])
		line_color = [155, 155, 155]
		# 画棋盘
		for i in range(ROW + 1):
			ww = 1
			pygame.draw.line(
				screen, line_color, [self.x, self.y + i * CELL], [self.x + CELL * COL, self.y + i * CELL], ww)
		for i in range(COL + 1):
			ww = 1
			pygame.draw.line(
				screen, line_color, [self.x + i * CELL, self.y], [self.x + i * CELL, self.y + CELL * ROW], ww)
		# 画子节点
		super(Board, self).render()


class Block(DisplayObject):
	def __init__(self, block_type):
		super(Block, self).__init__()
		self.block_type = block_type
		self.is_highlight = False

	def render(self):
		if self.block_type == BLOCK_START:
			pygame.draw.circle(screen, [255, 0, 0], [self.x, self.y], CELL // 3)
		elif self.block_type == BLOCK_WALL:
			pygame.draw.rect(screen, [0, 0, 0], [self.x - CELL // 2, self.y - CELL // 2, CELL, CELL])
		elif self.block_type == BLOCK_TEXT:
			pass  # Text('').render()
		elif self.block_type == BLOCK_ROAD:
			color = [200, 200, 200]
			if self.is_highlight:
				color = [200, 100, 100]
			pygame.draw.circle(screen, color, [self.x, self.y], 14)
		elif self.block_type == BLOCK_END:
			pygame.draw.circle(screen, [0, 200, 0], [self.x, self.y], 14)
		super(Block, self).render()


class BlockInfo(DisplayObject):
	pass


class Step(object):
	def __init__(self, x: int, y: int):
		self.g = 0  # 走到这一点的耗费
		self.h = 0  # 到终点的预估
		self.f = 0  # self.g + self.h
		self.x = x
		self.y = y
		self.parent = None

	def update(self, g: float, h: float):
		self.g = g
		self.h = h
		self.f = self.g + self.h

	def __repr__(self):
		return str(self.x) + ',' + str(self.y) + ':' + str(self.f)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y


class Game(object):
	def __init__(self):
		super(Game, self).__init__()
		self.data = [0 for i in range(COL * ROW)]
		self.board = Board()
		self.list_open: List[Step] = []
		self.list_close: List[Step] = []
		self.start_x = 0
		self.start_y = 0
		self.end_x = 0
		self.end_y = 0
		self.best_road = []
		self.desc = Text('点击鼠标添加障碍物,按Enter键开始')
		self.is_over = False

	def func_g(self, delta_x, delta_y) -> float:
		"""评估当前的耗费"""
		# return math.sqrt(delta_x ** 2 + delta_y ** 2)
		if abs(delta_x) == 1 and abs(delta_y) == 1:
			return 14
		else:
			return 10

	def in_open_list(self, x, y):
		for step in self.list_open:
			if step.x == x and step.y == y:
				return True
		return False

	def in_close_list(self, x, y):
		for step in self.list_close:
			if step.x == x and step.y == y:
				return True
		return False

	def get_in_open_list(self, x, y):
		for idx, step in enumerate(self.list_open):
			if step.x == x and step.y == y:
				return self.list_open[idx]

	def del_in_open_list(self, x, y):
		for idx, step in enumerate(self.list_open):
			if step.x == x and step.y == y:
				del self.list_open[idx]
				break

	def func_h(self, delta_x, delta_y) -> float:
		"""评估后面的路"""
		return (abs(delta_x) + abs(delta_y)) * 10

	def func_f(self, delta_x, delta_y) -> float:
		return self.func_g(delta_x, delta_y) + self.func_h(delta_x, delta_y)

	def select_current(self):
		min_f = 9999999
		node = None
		for step in self.list_open:
			if step.f < min_f:
				min_f = step.f
				node = step
		self.list_open.remove(node)
		self.list_close.append(node)
		return node

	def start(self):
		flag = 0
		while flag == 0:
			node = self.select_current()
			flag = self.explorer(node)

	def start_step(self):
		"""一步步显示用来调试"""
		if self.is_over:
			return
		node = self.select_current()
		self.board.add_block(node.x, node.y, BLOCK_ROAD)
		if self.explorer(node) > 0:
			self.is_over = True
		for s in self.list_close:
			b = self.board.get_block(s.x, s.y)
			if b is not None:
				b.is_highlight = False
		temp = node
		while True:
			if temp is None:
				break
			b = self.board.get_block(temp.x, temp.y)
			if b is not None:
				b.is_highlight = True
			temp = temp.parent

	def explorer(self, parent_step) -> int:
		if parent_step.x == self.end_x and parent_step.y == self.end_y:
			return parent_step.f
		x, y = parent_step.x, parent_step.y
		for i, j, val in self.get_near(x, y):
			if val == 0 or val == BLOCK_END:
				g, h = self.func_g(i - x, j - y) + parent_step.g, self.func_h(i - self.end_x, j - self.end_y)
				if self.in_close_list(i, j):
					continue
				if self.in_open_list(i, j):
					step = self.get_in_open_list(i, j)
					if g + h > step.f:
						continue
					else:
						step.update(g, h)
				else:
					step = Step(i, j)
					step.update(g, h)
					step.parent = parent_step
					self.list_open.append(step)
		return 0

	def init_board_with_data(self, data):
		self.data = data
		for idx, value in enumerate(self.data):
			if value != 0:
				x = idx % COL
				y = idx // COL
				self.board.add_block(x, y, value)
				if value == BLOCK_START:
					self.start_x, self.start_y = x, y
					start_node = Step(self.start_x, self.start_y)
					start_node.update(0, self.func_h(self.end_x - self.start_x, self.end_y - self.start_y))
					self.list_open.append(start_node)
				elif value == BLOCK_END:
					self.end_x, self.end_y = x, y

	def get_near(self, x, y):
		# 左上
		idx = y * COL + x
		if x >= 1 and y >= 1:
			yield x - 1, y - 1, self.data[idx - COL - 1]
		# 正上方
		if y >= 1:
			yield x, y - 1, self.data[idx - COL]
		# 右上方
		if x <= COL - 2 and y >= 1:
			yield x + 1, y - 1, self.data[idx - COL + 1]
		# 左方
		if x >= 1:
			yield x - 1, y, self.data[idx - 1]
		# 右方
		if x <= COL - 2:
			yield x + 1, y, self.data[idx + 1]
		# 左下方
		if y <= COL - 2 and x >= 1:
			yield x - 1, y + 1, self.data[idx + COL - 1]
		# 下方
		if y <= COL - 2:
			yield x, y + 1, self.data[idx + COL]
		# 右下方
		if x <= COL - 2 and y <= COL - 2:
			yield x + 1, y + 1, self.data[idx + COL + 1]

	def is_available(self, x, y):
		return self.data[y * COL + x] != BLOCK_WALL

	def render_thread(self):
		while not TO_EXIT:
			clock.tick(1000.0 / 33.0) / 1000.0
			screen.fill((0, 0, 0))
			self.board.render()
			pygame.display.update()

	def update_board_by_data(self):
		for idx, value in enumerate(self.data):
			if value == BLOCK_START:
				pass
			elif value == BLOCK_WALL:
				pass
			elif value == BLOCK_TEXT:
				pass
			elif value == BLOCK_ROAD:
				pass

	def input_thread(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					global TO_EXIT
					TO_EXIT = True
					exit()
				elif event.type == pygame.KEYDOWN:
					print(event.__dict__)
					g.start_step()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mouse_x, mouse_y = pygame.mouse.get_pos()
					x = math.floor((mouse_x - self.board.x) // CELL)
					y = math.floor((mouse_y - self.board.y) // CELL)
					if x < 0 or y < 0 or x >= COL or y >= ROW:
						return
					if self.data[y * COL + x] == BLOCK_WALL:
						self.data[y * COL + x] = 0
						self.board.remove_block(x, y)
					else:
						self.data[y * COL + x] = BLOCK_WALL
						self.board.add_block(x, y, BLOCK_WALL)


g: Game
if __name__ == '__main__':
	g = Game()
	render_thread = threading.Thread(target=g.render_thread, args=())
	render_thread.start()
	data1 = [
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 1, 0, 3, 0, 3, 3, 3, 3, 3, 3, 0,
		0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0,
		0, 0, 3, 3, 3, 3, 3, 0, 3, 2, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	]
	g.init_board_with_data(data1)

	# 如果想直接看结果,就把这段去掉
	# g.start()
	# step = g.list_close[-1].parent
	# while step is not None:
	# 	if step.parent is not None:
	# 		b = g.board.add_block(step.x, step.y, BLOCK_ROAD)
	# 	step = step.parent

	g.input_thread()
