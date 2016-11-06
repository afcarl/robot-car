# coding: utf-8
import task
from task import grid
import numpy as np
import matplotlib.pyplot as plt

def main():
	x = []
	y = []

	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if grid[i][j] == 1:
				x.append(j)
				y.append(len(grid)-i)

	colors = np.random.rand(len(x))
	area = np.pi * (48.5)**2  

	fig_size = plt.rcParams["figure.figsize"]

	fig_size[0] = 12
	fig_size[1] = 9
	plt.rcParams["figure.figsize"] = fig_size

	plt.scatter(x, y, s=area, c=colors, alpha=0.5)
	plt.gca().set_aspect('equal', adjustable='box')

	result = task.runTask()
	robot_state = result.pop(0)
	
	print result
	rx, ry = zip(*robot_state)
	ry = [len(grid)-y for y in ry]
	
	plt.plot(rx, ry, 'bo')
	plt.show()

if __name__ == "__main__":
	main()
