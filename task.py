# coding: utf-8

from math import *
from robot.robot import robot
from planner.planner import plan
from estimation.particle import particles

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

steering_noise    = 0.1
distance_noise    = 0.03
measurement_noise = 0.3

weight_data       = 0.1
weight_smooth     = 0.2
p_gain            = 2.0
d_gain            = 6.0


def computeCTE(spath, currentPos, index):

	dx = spath[index+1][0] - spath[index][0];
	dy = spath[index+1][1] - spath[index][1];
	Rx = currentPos[0] - spath[index][0];
	Ry = currentPos[1] - spath[index][1];
	u = (Rx*dx + Ry*dy) / sqrt(dx**2 + dy**2); 
	cte = (Ry*dx - Rx*dy) / sqrt(dx**2 + dy**2);  
	if u > 1.0:
		index += 1; 
	return cte,index 


def _runTask(grid, goal, spath, params, printflag = False, speed = 0.1, timeout = 1000):

    myrobot = robot()
    myrobot.set(0., 0., 0.)
    myrobot.set_noise(steering_noise, distance_noise, measurement_noise)
    filter = particles(myrobot.x, myrobot.y, myrobot.orientation,
                       steering_noise, distance_noise, measurement_noise)

    cte  = 0.0
    err  = 0.0
    N    = 0

    index = 0 # index into the path
    state = []# store robot status during the entire run  
    while not myrobot.check_goal(goal) and N < timeout:

        diff_cte = - cte

        estimate = filter.get_position()
	
        cte, index = computeCTE(spath, estimate, index)

        diff_cte += cte

        steer = - params[0] * cte - params[1] * diff_cte 

        myrobot = myrobot.move(grid, steer, speed)
        filter.move(grid, steer, speed)

        Z = myrobot.sense()
        filter.sense(Z)

        if not myrobot.check_collision(grid):
            print '##### Collision ####'

        err += (cte ** 2)
        N += 1

        state.append(myrobot.getPos())		
        if printflag:
            print myrobot, cte, index, u

    return [state, myrobot.check_goal(goal), cte, myrobot.num_collisions, myrobot.num_steps]


def runTask():
    path = plan(grid, init, goal)
    path.astar()
    path.smooth(weight_data, weight_smooth)
    return _runTask(grid, goal, path.spath, [p_gain, d_gain])


