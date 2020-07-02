# 柱状表，用来显示排序相关的
import pygame
import sys
import random
import math

MOVE_SPEED = 300  # 每秒的移动速度想慢慢看就调低一点

pygame.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()


def random_color():
	return [random.randint(55, 200), random.randint(55, 200), random.randint(55, 200)]


class DisplayObject(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.to_x = 0
		self.speed = 0
		self.parent = None
		self.inited = False
		self.ui = None

	def update(self, delta):
		"""更新显示相关的数据"""
		pass

	def render(self):
		"""每帧调用一次"""
		pass

	def move_x(self, to_x, speed=100):
		self.to_x = to_x
		self.speed = speed


class Bar(DisplayObject):
	def __init__(self, value):
		super(Bar, self).__init__()
		self.value = value
		self.width = 10
		self.height = self.value * 10
		self.color = random_color()
		self.txt = Text(str(value))
		self.is_arrow = False  # 是否是箭头
		self.is_p = False  # 是否是标兵
		self.txt_arrow = Text('')
		self.txt_p = Text('')
		self.is_low = False
		self.is_high = False

	def update(self, delta):
		if self.to_x != self.x and self.speed > 0:
			one = 1 if self.to_x - self.x > 0 else -1
			self.x = self.x + one * self.speed * delta
			if math.fabs(self.to_x - self.x) < 10:
				self.x = self.to_x
		else:
			self.speed = 0

	def render(self):
		cc = self.color
		if self.is_low or self.is_high:
			cc = [255, 255, 255]
			ww = self.width + 10

		self.ui = pygame.draw.rect(screen, cc, [self.x, self.y, self.width, self.height], 0)
		# 画数字
		self.txt.x = self.x + 5
		self.txt.y = self.y - 50
		self.txt.render()
		if self.is_arrow:
			self.txt_arrow.content = '↑'
			self.txt_arrow.x = self.x
			self.txt_arrow.y = SCREEN_HEIGHT - 40
			self.txt_arrow.render()
		if self.is_p:
			self.txt_p.content = 'P'
			self.txt_p.x = self.x
			self.txt_p.y = SCREEN_HEIGHT - 120
			self.txt_p.render()


class Text(DisplayObject):
	FNT = pygame.font.SysFont('arial', 25)

	def __init__(self, content):
		super(Text, self).__init__()
		self.color = [255, 255, 255]
		self.content = content

	def render(self):
		self.ui = Text.FNT.render(self.content, True, self.color, [0, 0, 0])
		screen.blit(self.ui, (self.x, self.y))


class BarChart(DisplayObject):

	def __init__(self, on_next):
		super(BarChart, self).__init__()
		self.bars = []
		self.max_value = -sys.maxsize
		self.on_next = on_next
		self.base_bottom = 50  # 下面多出50个像素
		self.base_left = 100
		self.bar_gap = 40
		self.title = ''
		self.txt = Text('')
		self.txt.x = SCREEN_WIDTH * 0.5 - 100
		self.txt.y = SCREEN_HEIGHT - 50

	def init_with_arr(self, arr):
		for value in arr:
			self.add_bar(value)

	def update_with_step(self, step):
		print(step)
		arr = step.arr
		for idx, v in enumerate(arr):
			b = self.get_bar_by_val(v)
			b.move_x(self.base_left + idx * self.bar_gap, 400)
			b.is_arrow = False
			b.is_p = False
			b.is_low = False
			b.is_high = False
		self.get_bar_by_val(arr[step.left_idx]).is_arrow = True
		self.get_bar_by_val(arr[step.right_idx]).is_arrow = True
		self.get_bar_by_val(arr[step.low]).is_low = True
		self.get_bar_by_val(arr[step.high]).is_low = True
		self.get_bar_by_val(step.p).is_p = True

	def show_title(self, title):
		self.txt.content = title

	def add_bar(self, value):
		b = Bar(value)
		b.x = self.base_left + len(self.bars) * self.bar_gap
		b.y = SCREEN_HEIGHT - b.height - self.base_bottom
		self.bars.append(b)

	def get_bar_by_val(self, value):
		for i in self.bars:
			if i.value == value:
				return i
		return None

	def render(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				elif event.type == pygame.KEYUP:
					if self.on_next is not None:
						self.on_next()

			delta = clock.tick(1000.0 / 30.0) / 1000.0
			screen.fill((0, 0, 0))
			self.txt.render()
			for i in self.bars:
				i.update(delta)
				i.render()
			pygame.display.update()


if __name__ == '__main__':
	bc = BarChart(None)
	bc.init_with_arr([19, 24, 18, 23, 13, 15, 20, 22, 30, 27])
	bc.render()
	a = input('kkk')
