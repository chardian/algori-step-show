from bar_chart import BarChart
import copy

all_step = []
idx = 0


def on_key_down():
	global idx
	print('on key down hehe da', idx, len(all_step))
	if idx >= len(all_step):
		bc.show_title('OVER')
		return
	bc.update_with_arr(all_step[idx])
	bc.show_title('step:' + str(idx))
	idx += 1


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
		all_step.append(copy.copy(arr))
	# arr[first] 这个值, 刚好比标兵指向的值大一些,两者交换
	arr[p_idx], arr[first] = arr[first], arr[p_idx]
	all_step.append(copy.copy(arr))
	swap_quick_sort(arr, low, first - 1)
	swap_quick_sort(arr, first + 1, high)


if __name__ == '__main__':
	test_arr = [19, 24, 18, 23, 13, 15, 20, 22, 30, 27]
	bc.init_with_arr(test_arr)
	swap_quick_sort(test_arr, 0, len(test_arr) - 1)
	bc.render()
