import pygame

pygame.init()
screen = pygame.display.set_mode((640, 700), 0, 32)
clock = pygame.time.Clock()


class DisplayObject(object):
	def __init__(self):
		self.parent = None
		self.children = []
		self.x = 0
		self.y = 0

	def add_child(self, child):
		child.parent = self
		self.children.append(child)

	def remove_child(self, child):
		for idx in range(len(self.children)):
			if self.children[idx] == child:
				del self.children[idx]
				return True
		return False

	def render(self):
		for i in self.children:
			i.render()


class Text(DisplayObject):
	# pygame.font.get_fonts() 查看支持哪些字体
	FNT = pygame.font.SysFont('simhei', 20)

	def __init__(self, content):
		super(Text, self).__init__()
		self.color = [0, 0, 0]
		self.content = content

	def render(self):
		txt = Text.FNT.render(self.content, True, self.color)
		screen.blit(txt, (self.x, self.y))
