from bar_chart import BarChart
import copy

all_step = []
idx = 0


def on_key_down():
	global idx
	if idx >= len(all_step):
		bc.show_title('OVER')
		return
	bc.update_with_step(all_step[idx])
	# bc.show_title('step:' + str(idx))
	idx += 1


class QuickStep(object):
	"""记录快速排序的某一步替换"""

	def __init__(self, arr, left_idx, right_idx, p, low, high):
		"""
		:param arr: 数组数据
		:param left_idx: 左侧游标位置
		:param right_idx: 右侧游标位置
		:param p: 标兵
		:param low: 当前递归最小下标
		:param high:  当前递归最大下标
		"""
		super(QuickStep, self).__init__()
		self.arr = copy.copy(arr)
		self.left_idx = left_idx
		self.right_idx = right_idx
		self.p = p
		self.low = low
		self.high = high

	def __repr__(self):
		return '下标范围{}-{},左侧游标:{},右侧游标:{},标兵值{}'.format(
			self.low, self.high, self.arr[self.left_idx],
			self.arr[self.right_idx], self.p)


bc = BarChart(on_key_down)


def swap_quick_sort(arr, low, high):
	if low >= high:
		return
	first = low
	last = high
	key = arr[last]
	p_idx = last
	while first < last:
		while first < last and key >= arr[first]:
			first += 1
		left_idx = first  # 找到一个大于标兵的
		while first < last and key <= arr[last]:
			last -= 1
		right_dx = last  # 找到一个小于标兵的
		arr[left_idx], arr[right_dx] = arr[right_dx], arr[left_idx]  # 两者交换位置
		all_step.append(QuickStep(arr, first, last, key, low, high))
	# arr[first] 这个值, 刚好比标兵指向的值大一些,两者交换
	arr[p_idx], arr[first] = arr[first], arr[p_idx]
	all_step.append(QuickStep(arr, first, last, key, low, high))
	swap_quick_sort(arr, low, first - 1)
	swap_quick_sort(arr, first + 1, high)


if __name__ == '__main__':
	test_arr = [19, 24, 18, 23, 17, 30, 13, 15, 20, 22]
	bc.init_with_arr(test_arr)
	all_step.append(QuickStep(test_arr, 0, len(test_arr) - 1, test_arr[-1], 0, len(test_arr) - 1))
	swap_quick_sort(test_arr, 0, len(test_arr) - 1)

	bc.render()
